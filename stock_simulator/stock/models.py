from django.db import models

class stock(models.Model):
    sname = models.CharField(max_length=50)
    number = models.CharField(max_length=50, primary_key=True, unique=True)
    overamt = models.IntegerField()
    
class quotations(models.Model):
    snum = models.IntegerField(primary_key=True, unique=True)
    Buyamt = models.IntegerField()
    sellamt = models.IntegerField()
    tstmp = models.TimeField(max_length=50, unique=True)
    sprice = models.FloatField(max_length=50)
    
    
class inventory(models.Model):
    cid = models.CharField(max_length=50, primary_key=True, unique=True)
    num = models.IntegerField()
    amount = models.IntegerField()
    price = models.FloatField(max_length=50)
    stmp = models.TimeField(max_length=50, unique=True)
    
   