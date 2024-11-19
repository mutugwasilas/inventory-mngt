from django.db import models

# Create your models here.

class Unit(models.Model):
    unit = models.CharField(max_length=255)

    def __str__(self):
        return self.unit
    
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Inventory(models.Model): 
    name = models.CharField(max_length=255, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    quantity_sold = models.PositiveIntegerField(default=0) 
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit_loss = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity_remaining = models.PositiveBigIntegerField( default=0)
    date_bought = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    stock_alert = models.PositiveBigIntegerField(default=15) 


    def __str__(self):
        return self.name