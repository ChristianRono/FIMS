from django.db import models

# Create your models here.
class Invoice(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    city_address = models.CharField(max_length=100)
    tax_rate = models.FloatField(blank=True,null=True)
    discount_rate = models.FloatField(blank=True,null=True)
    total = models.FloatField(blank=True,null=True)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}'s invoice No# {str(self.id)} created on {str(self.created_on)}"
    
class Item(models.Model):
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    price_per_lbs = models.FloatField()
    weight = models.FloatField()
    amount = models.FloatField()

    def __str__(self):
        return f"Invoice No# {str(self.invoice.id)}'s Item --> {self.description}"