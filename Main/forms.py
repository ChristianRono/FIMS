from django import forms
from Main.models import Invoice,Item

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['name','company','street_address','city_address']

class ItemsForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['description','price_per_lbs','weight']
        
class TaxForm(forms.Form):
    tax = forms.FloatField(max_value=100,min_value=0,initial=0)
    discount = forms.FloatField(max_value=100,min_value=0,initial=0)

class EmailForm(forms.Form):
    to = forms.EmailField(label="To:")
    re = forms.CharField(label="Subject:",initial="Framalaundromat Invoice")
    message = forms.CharField(widget=forms.Textarea,initial="This is an automatic email. Please do not reply.")