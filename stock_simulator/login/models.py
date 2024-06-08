from django.db import models
class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100) 
  
class Customer(models.Model):
    name = models.CharField(max_length=50)
    identity = models.CharField(max_length=50, primary_key=True, unique=True)
    account = models.CharField(max_length=50, unique=True)
    ctfc = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name