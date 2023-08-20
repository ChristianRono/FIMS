from reportlab.pdfgen import canvas
from django.utils import formats
from pathlib import Path
import os

from Main.pdf_water_mark import watermark_file

def pdf_print(invoice,items):
        invoice_number = invoice.id
        name = invoice.name
        street_address = invoice.street_address
        company = invoice.company
        city_address = invoice.city_address
        invoice_date = formats.date_format(invoice.created_on, "SHORT_DATETIME_FORMAT")
        total = round(invoice.total,2)
        tax = invoice.tax_rate
        discount = invoice.discount_rate
        invoice_type = "Profoma Invoice"
        desktop = os.path.join(Path.home(),'Desktop')
        desktop = os.path.join(desktop,'Invoices')
        pdf_file_name = os.path.join(desktop,f"{str(invoice_number)}_{str(name)}.pdf")
        generate_invoice(str(name), str(invoice_number),items,str(total),str(company), str(street_address), str(city_address),str(invoice_date), str(tax),
            str(discount), str(invoice_type), pdf_file_name)
        #watermark_file('watermark.pdf',pdf_file_name)
        #os.remove('watermark.pdf')

def generate_water_mark(c):
     x = 0
     y = 0
     for i in range(5):
        c.drawImage("image/watermark.png", x+100*i, y+120*i, 160, 160,mask='auto')

def generate_invoice(name, invoice_number, items,
        total, company, street_address, city_address,invoice_date, tax, discount, invoice_type, pdf_file_name):
    c = canvas.Canvas(pdf_file_name)

    # image of seal
    logo = 'image/logo.jpeg'
    c.drawImage(logo, 250, 720, width=120, height=120)
    generate_water_mark(c)
    c.setFont('Helvetica-Bold', 16, leading=None)
    c.drawCentredString(310, 700, 'Framalaundromat Invoice')

    c.setFont('Helvetica', 12, leading=None)
    # if invoice_type == 'Receipt':
    # 	c.drawCentredString(400, 660, "Receipt Number #:")
    # elif invoice_type == 'Proforma Invoice':
    # 	c.drawCentredString(400, 660, "Proforma Invoice #:")
    # else:
    c.drawCentredString(400, 660, str(invoice_type) + ':')
    c.setFont('Helvetica', 12, leading=None)
    invoice_number_string = str('0000' + invoice_number)
    c.drawCentredString(490, 660, invoice_number_string)


    c.setFont('Helvetica', 12, leading=None)
    c.drawCentredString(409, 640, "Date:")
    c.setFont('Helvetica', 12, leading=None)
    c.drawCentredString(492, 641, invoice_date)


    c.setFont('Helvetica', 12, leading=None)
    c.drawCentredString(397, 620, "Amount:")
    c.setFont('Helvetica-Bold', 12, leading=None)
    c.drawCentredString(484, 622, '$'+total)


    c.setFont('Helvetica', 12, leading=None)
    c.drawCentredString(60, 660, "To:")
    c.setFont('Helvetica', 12, leading=None)
    c.drawCentredString(200, 660, name)

    c.setFont('Helvetica', 12, leading=None)
    c.drawCentredString(60, 640, "Company:")
    c.setFont('Helvetica', 12, leading=None)
    c.drawCentredString(200, 640, company)

    c.setFont('Helvetica', 12, leading=None)
    c.drawCentredString(60, 620, "Street:")
    c.setFont('Helvetica', 12, leading=None)
    c.drawCentredString(200, 620, street_address) 

    c.setFont('Helvetica', 12, leading=None)
    c.drawCentredString(60, 600, "City:")
    c.setFont('Helvetica', 12, leading=None)
    c.drawCentredString(200, 600, city_address)     

    c.setFont('Helvetica-Bold', 14, leading=None)
    c.drawCentredString(310, 580, str(invoice_type))
    c.drawCentredString(110, 560, "Particulars:")
    if len(items) <= 7: 
        j = 510
        for i in range(len(items)):
            c.drawCentredString(295, j, "__________________________________________________________")
            j -= 30
        c.drawCentredString(295, j, "__________________________________________________________")

        c.setFont('Helvetica-Bold', 12, leading=None)
        c.drawCentredString(110, 520, 'ITEMS')     
        c.drawCentredString(220, 520, 'UNITS')     
        c.drawCentredString(330, 520, 'UNIT PRICE')     
        c.drawCentredString(450, 520, 'LINE TOTAL')  

        i =490
        for item in items:
            c.setFont('Helvetica', 12, leading=None)
            c.drawCentredString(110, i, item.description)     
            c.drawCentredString(220, i, str(item.weight))     
            c.drawCentredString(330, i, str(item.price_per_lbs))     
            c.drawCentredString(450, i, str(item.amount))
            i -= 30         

        
        c.setFont('Helvetica-Bold', 12,leading=None)
        c.drawCentredString(150, 260, 'Comments')
        j = 240
        for i in range(3):
            c.drawCentredString(295, j, "__________________________________________________________")
            j -= 30
        
        c.setFont('Helvetica-Bold', 12, leading=None)
        c.drawCentredString(400, 140, "Tax:")
        c.setFont('Helvetica', 20, leading=None)
        c.drawCentredString(484, 140, tax+'%') 

        c.setFont('Helvetica-Bold', 12, leading=None)
        c.drawCentredString(400, 110, "Discount:")
        c.setFont('Helvetica', 20, leading=None)
        c.drawCentredString(484, 110, discount+'%')

        # TOTAL
        c.setFont('Helvetica-Bold', 20, leading=None)
        c.drawCentredString(340, 80, "TOTAL:")
        c.setFont('Helvetica-Bold', 20, leading=None)
        c.drawCentredString(484, 80, '$'+total) 


        # SIGN
        c.setFont('Helvetica-Bold', 12, leading=None)
        c.drawCentredString(150, 80, "Signed:__________________")
        c.setFont('Helvetica-Bold', 12, leading=None)
        c.drawCentredString(170, 80, 'Manager')
    else:
        if len(items) > 12:
            j = 510
            for i in range(12):
                c.drawCentredString(295, j, "__________________________________________________________")
                j -= 30
            c.drawCentredString(295, j, "__________________________________________________________")

            c.setFont('Helvetica-Bold', 12, leading=None)
            c.drawCentredString(110, 520, 'ITEMS')     
            c.drawCentredString(220, 520, 'UNITS')     
            c.drawCentredString(330, 520, 'UNIT PRICE')     
            c.drawCentredString(450, 520, 'LINE TOTAL')  

            i =490
            for item in items[:12]:
                c.setFont('Helvetica', 12, leading=None)
                c.drawCentredString(110, i, item.description)     
                c.drawCentredString(220, i, str(item.weight))     
                c.drawCentredString(330, i, str(item.price_per_lbs))     
                c.drawCentredString(450, i, str(item.amount))
                i -= 30         

            ################################################
            ########## Start from Here #####################
            ################################################
            c.showPage()
            generate_water_mark(c)
            j = 700
            for i in range(len(items[12:])):
                c.drawCentredString(295, j, "__________________________________________________________")
                j -= 30
            c.drawCentredString(295, j, "__________________________________________________________")

            c.setFont('Helvetica-Bold', 12, leading=None)
            c.drawCentredString(110, 720, 'ITEMS')     
            c.drawCentredString(220, 720, 'UNITS')     
            c.drawCentredString(330, 720, 'UNIT PRICE')     
            c.drawCentredString(450, 720, 'LINE TOTAL')  

            i =680
            for item in items[12:]:
                c.setFont('Helvetica', 12, leading=None)
                c.drawCentredString(110, i, item.description)     
                c.drawCentredString(220, i, str(item.weight))     
                c.drawCentredString(330, i, str(item.price_per_lbs))     
                c.drawCentredString(450, i, str(item.amount))
                i -= 30

            h = 720
            c.setFont('Helvetica-Bold', 12,leading=None)
            c.drawCentredString(150, 260, 'Comments')
            j = 240
            for i in range(3):
                c.drawCentredString(295, j, "__________________________________________________________")
                j -= 30

            c.setFont('Helvetica-Bold', 12, leading=None)
            c.drawCentredString(400, 140, "Tax:")
            c.setFont('Helvetica', 20, leading=None)
            c.drawCentredString(484, 140, tax+'%') 

            c.setFont('Helvetica-Bold', 12, leading=None)
            c.drawCentredString(400, 110, "Discount:")
            c.setFont('Helvetica', 20, leading=None)
            c.drawCentredString(484, 110, discount+'%')

            # TOTAL
            c.setFont('Helvetica-Bold', 20, leading=None)
            c.drawCentredString(340, 80, "TOTAL:")
            c.setFont('Helvetica-Bold', 20, leading=None)
            c.drawCentredString(484, 80, '$'+total) 


            # SIGN
            c.setFont('Helvetica-Bold', 12, leading=None)
            c.drawCentredString(150, 80, "Signed:__________________")
            c.setFont('Helvetica-Bold', 12, leading=None)
            c.drawCentredString(170, 80, 'Manager')
        else:
            j = 510
            for i in range(len(items)):
                c.drawCentredString(295, j, "__________________________________________________________")
                j -= 30
            c.drawCentredString(295, j, "__________________________________________________________")

            c.setFont('Helvetica-Bold', 12, leading=None)
            c.drawCentredString(110, 520, 'ITEMS')     
            c.drawCentredString(220, 520, 'UNITS')     
            c.drawCentredString(330, 520, 'UNIT PRICE')     
            c.drawCentredString(450, 520, 'LINE TOTAL')  

            i =490
            for item in items:
                c.setFont('Helvetica', 12, leading=None)
                c.drawCentredString(110, i, item.description)     
                c.drawCentredString(220, i, str(item.weight))     
                c.drawCentredString(330, i, str(item.price_per_lbs))     
                c.drawCentredString(450, i, str(item.amount))
                i -= 30         

            ################################################
            ########## Start from Here #####################
            ################################################
            c.showPage()
            generate_water_mark(c)
            c.setFont('Helvetica-Bold', 12,leading=None)
            c.drawCentredString(150, 720, 'Comments')
            j = 700
            for i in range(3):
                c.drawCentredString(295, j, "__________________________________________________________")
                j -= 30

            c.setFont('Helvetica-Bold', 12, leading=None)
            c.drawCentredString(400, 580, "Tax:")
            c.setFont('Helvetica', 20, leading=None)
            c.drawCentredString(484, 580, tax+'%') 

            c.setFont('Helvetica-Bold', 12, leading=None)
            c.drawCentredString(400, 550, "Discount:")
            c.setFont('Helvetica', 20, leading=None)
            c.drawCentredString(484, 550, discount+'%')

            # TOTAL
            c.setFont('Helvetica-Bold', 20, leading=None)
            c.drawCentredString(340, 520, "TOTAL:")
            c.setFont('Helvetica-Bold', 20, leading=None)
            c.drawCentredString(484, 520, '$'+total) 


            # SIGN
            c.setFont('Helvetica-Bold', 12, leading=None)
            c.drawCentredString(150, 520, "Signed:__________________")
            c.setFont('Helvetica-Bold', 12, leading=None)
            c.drawCentredString(170, 520, 'Manager')


    c.showPage()
    c.save()
