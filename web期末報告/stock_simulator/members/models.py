from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100, null=False)
    identity = models.CharField(max_length=20, primary_key=True, unique=True, null=False)
    account = models.CharField(max_length=30, unique=True, null=False)
    ctfc = models.CharField(max_length=30, unique=True, null=False)

    def __str__(self):
        return self.name
