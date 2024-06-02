from django.db import models

class Stock(models.Model):
    sname = models.CharField(max_length=50)
    number = models.CharField(max_length=50, primary_key=True, unique=True)
    overamt = models.IntegerField()

class Quotations(models.Model):
    snum = models.ForeignKey(Stock, on_delete=models.CASCADE, primary_key=True)  
    buyamt = models.IntegerField()
    sellamt = models.IntegerField()
    tstmp = models.DateTimeField()  
    sprice = models.FloatField()

class Inventory(models.Model):
    cid = models.CharField(max_length=50, primary_key=True, unique=True)
    num = models.IntegerField()
    amount = models.IntegerField()
    price = models.FloatField()
    stmp = models.DateTimeField()  
