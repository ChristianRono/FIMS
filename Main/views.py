import os
from pathlib import Path

from django.shortcuts import render,redirect
from django.core.mail import EmailMessage

from .models import Invoice,Item,Profile
from .forms import CustomerForm,ItemsForm,TaxForm,EmailForm,ProfileForm

from Main.pdfprint import pdf_print
# Create your views here.

def homepage(request):
    invoices = Invoice.objects.all()
    return render(request,"homepage.html",{"invoices":invoices})

def profile(request):
    if request.method == "POST":
        instance = Profile.objects.get(id=1)
        form = ProfileForm(request.POST,instance=instance)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile')
    else:
        instance = Profile.objects.get(id=1)
        form = ProfileForm(instance=instance)
        return render(request,"profile.html",{'form':form})

def customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            company = form.cleaned_data['company']
            street_address = form.cleaned_data['street_address']
            city_address = form.cleaned_data['city_address']
            invoice = Invoice(name=name,company=company,street_address=street_address,city_address=city_address)
            invoice.save()
            id = invoice.pk
            request.session['id'] = id
            return redirect("/items/")
    else:
        form = CustomerForm()
    return render(request,"add_customer.html",{"form":form})

def items(request):
    if request.method == "POST":
        form = ItemsForm(request.POST)
        if form.is_valid():
            invoice = request.POST['invoice']
            description = form.cleaned_data['description']
            price_per_lbs = form.cleaned_data['price_per_lbs']
            weight = form.cleaned_data['weight']
            amount = float(price_per_lbs) * float(weight)
            invoice = Invoice.objects.get(id=invoice)
            item = Item(invoice=invoice,description=description,price_per_lbs=price_per_lbs,weight=weight,amount=amount)
            item.save()

            form = ItemsForm()
            invoice_id = request.session['id']
            items_list = Item.objects.filter(invoice=invoice)
            return render(request,"add_items.html",{"form":form,"invoice":invoice_id,'items':items_list})
    else:
        form = ItemsForm()
        invoice = request.session['id']
    return render(request,"add_items.html",{"form":form,'invoice':invoice,'items':None})

def tax(request):
    if request.method == "POST":
        form = TaxForm(request.POST)
        if form.is_valid():
            tax_rate = form.cleaned_data['tax']
            discount_rate = form.cleaned_data['discount']
            comments = form.cleaned_data['comments']
            invoice_id = request.session['id']
            invoice = Invoice.objects.get(id=invoice_id)
            invoice.tax_rate =tax_rate
            invoice.discount_rate = discount_rate
            invoice.comments = comments
            items = Item.objects.filter(invoice=invoice)
            total = 0
            for item in items:
                total += item.amount

            if discount_rate > 0:
                total = total - ((float(discount_rate) * total)/100)
            
            if tax_rate > 0:
                total = total + ((float(tax_rate) * total)/100)

            invoice.total = total
            invoice.save()
            
            id = invoice.pk
            request.session['id'] = id
            return redirect(f"/print/{invoice.id}")
    else:
        form = TaxForm()
    return render(request,"add_tax_discount.html",{'form':form})

def delete_invoice(request,id):
    Invoice.objects.get(id=id).delete()
    return redirect("/")

def delete_item(request,id):
    item = Item.objects.get(id=id)
    invoice = Invoice.objects.get(id=item.invoice.id)
    total = invoice.total
    invoice.total = float(total) - float(item.amount)
    invoice.save()
    item.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def pdfprint(request,id):
    invoice = Invoice.objects.get(id=id)
    profiles = Profile.objects.get(id=id)
    items = Item.objects.filter(invoice=invoice)
    pdf_print(invoice,profiles,items)
    return redirect('/')

def edit(request,id):
    if request.method == "POST":
        pass
    else:
        invoice = Invoice.objects.get(id=id)
        items = Item.objects.filter(invoice=invoice)
        form1 = CustomerForm(instance=invoice)
        form2 = TaxForm(initial={'tax':invoice.tax_rate,'discount':invoice.discount_rate,'comments':invoice.comments})
        form3 = ItemsForm()
    return render(request,"edit.html",{"form1":form1,
                                       "form2":form2,
                                       'forms':form3,
                                       'items':items,
                                       'id':id})

def edit_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            company = request.POST['company']
            street_address = request.POST['street_address']
            city_address = request.POST['city_address']
            id = request.POST['id']
            invoice = Invoice.objects.get(id=id)
            invoice.name = name
            invoice.company = company
            invoice.street_address = street_address
            invoice.city_address = city_address
            invoice.save()
            return redirect(f'/edit/invoice/{id}/')
        
def edit_tax(request):
    if request.method == "POST":
        form = TaxForm(request.POST)
        if form.is_valid():
            tax = form.cleaned_data['tax']
            discount = form.cleaned_data['discount']
            comments = form.cleaned_data['comments']
            id = request.POST['id']
            invoice = Invoice.objects.get(id=id)
            invoice.tax_rate = tax
            invoice.discount_rate = discount
            invoice.comments = comments
            invoice.save()
            return redirect(f'/edit/invoice/{id}/')

def edit_item(request,invoiceid,itemid):
    if request.method == "POST":
        form = ItemsForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            ppu = form.cleaned_data['price_per_lbs']
            weight = form.cleaned_data['weight']
            item = Item.objects.get(id=itemid)
            item.description = description
            item.price_per_lbs = ppu
            item.weight = weight
            amount = float(ppu) * float(weight)
            item.amount = amount
            item.save()

            invoice = Invoice.objects.get(id=invoiceid)
            items = Item.objects.filter(invoice=invoice)
            total = 0
            for item in items:
                total += item.amount

            if invoice.discount_rate > 0:
                total = total - ((float(invoice.discount_rate) * total)/100)
            
            if invoice.tax_rate > 0:
                total = total + ((float(invoice.tax_rate) * total)/100)

            invoice.total = total
            invoice.save()
            return redirect(f'/edit/invoice/{invoiceid}/')
    else:
        item = Item.objects.get(id=itemid)
        form =ItemsForm(initial={'description':item.description,
                                'price_per_lbs':item.price_per_lbs,
                                'weight':item.weight})
        return render(request,"edit_item.html",{'form':form,'itemid':itemid,'invoiceid':invoiceid})
    
def add_item(request):
     if request.method == "POST":
        form = ItemsForm(request.POST)
        if form.is_valid():
            invoiceid = request.POST['invoice']
            description = form.cleaned_data['description']
            price_per_lbs = form.cleaned_data['price_per_lbs']
            weight = form.cleaned_data['weight']
            amount = float(price_per_lbs) * float(weight)
            invoice = Invoice.objects.get(id=invoiceid)
            invoice.total = invoice.total + amount
            item = Item(invoice=invoice,description=description,price_per_lbs=price_per_lbs,weight=weight,amount=amount)
            item.save()

            invoice = Invoice.objects.get(id=invoiceid)
            items = Item.objects.filter(invoice=invoice)
            total = 0
            for item in items:
                total += item.amount

            if invoice.discount_rate > 0:
                total = total - ((float(invoice.discount_rate) * total)/100)
            
            if invoice.tax_rate > 0:
                total = total + ((float(invoice.tax_rate) * total)/100)

            invoice.total = total
            invoice.save()
            return redirect(request.META.get('HTTP_REFERER'))
        
def send_mail(request,id):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            to = form.cleaned_data['to']
            re = form.cleaned_data['re']
            message = form.cleaned_data['message']
            email = EmailMessage(
                subject=re,
                body=message,
                to=[to],
            )
            invoice = Invoice.objects.get(id=id)
            pdf_file = f"{str(invoice.id)}_{str(invoice.name)}.pdf"
            desktop = os.path.join(Path.home(),'Desktop')
            desktop = os.path.join(desktop,'Invoices')
            path = os.path.join(desktop,pdf_file)
            content = open(path, 'rb')
            email.attach(pdf_file,content.read(),'application/pdf')
            email.send()
            return redirect('homepage')
    else:
        form = EmailForm()
        return render(request,"email.html",{'form':form})
