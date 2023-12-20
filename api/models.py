from django.db import models


generate_unique_code=20


class Activity (models.Model):
    action = models.CharField(default='', max_length=20)
    symbol = models.CharField(default='', max_length=20)
    symbolId = models.CharField(default='', max_length=20)
    currency = models.CharField(default='', max_length=20)
    type = models.CharField(default='', max_length=20)

    accountNumber = models.DecimalField(default=0, max_digits=20, decimal_places=0)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    quantity = models.DecimalField(default=0,max_digits=10, decimal_places=0)
    grossAmount = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    netAmount = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    commission = models.DecimalField(default=0,max_digits=10, decimal_places=2)

    tradeDate = models.DateTimeField(null=True, blank=True)
    settlementDate = models.DateTimeField(null=True, blank=True)
    createdAt = models.DateTimeField(null=True, blank=True, auto_now_add = True)
    lastModified= models.DateTimeField(null=True, blank=True, auto_now_add = True)



class Account (models.Model):
    accountNumber = models.DecimalField(default=0, max_digits=20, decimal_places=0,unique=True)
    type = models.CharField(default='', max_length=20)
    isPrimary = models.BooleanField(default=False)
    
    