from typing import Iterable
import uuid
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

generate_unique_code=20


class Broker (models.Model):
    id =  models.UUIDField(default=uuid.uuid4, max_length=30, editable=False)
    name = models.CharField(default=0, max_length=20,primary_key=True)
    created_at = models.DateTimeField(auto_now=True, editable=False)


class Account (models.Model):
    account_number = models.CharField(default=0, max_length=20,primary_key=True)
    type = models.CharField(default=None, max_length=20)
    current_balance = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    net_deposits = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    currency = models.CharField(default=None, max_length=10)
    status = models.CharField(default=None, max_length=10)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)
    last_synced = models.DateTimeField(default=timezone.now)

    linked_account = models.ForeignKey('self',to_field="account_number", on_delete=models.SET_NULL, null=True, default=None)
    account_broker = models.ForeignKey(Broker, to_field="name", default="None", on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.type + " " + self.account_broker.name

    def set_linked_account(self, other_account_number):
        try:
            related_account = Account.objects.get(account_number=other_account_number)
            self.linked_account = related_account
            self.save()
        except Account.DoesNotExist:
            print("The related account does not exist.")

    def get_all_linked_activities(self):
        if self.linked_account:
            return Activity.objects.filter(models.Q(account=self) | models.Q(account=self.linked_account))
        else:
            return Activity.objects.filter(account=self)

class Security (models.Model):
    id = models.CharField(default=None, max_length=255,primary_key=True)
    symbol = models.CharField(default=None, max_length=20, unique=True)
    name = models.CharField(default=None, max_length=255, null=True)
    description = models.CharField(default=None, max_length=255, null=True)
    type = models.CharField(default=None, max_length=50, null=True)
    currency = models.CharField(default=None, max_length=50, null=True)
    status= models.CharField(default=None, max_length=50, null=True)
    exchange = models.CharField(default=None, max_length=50, null=True)
    option_details = models.TextField(default=None, null=True)
    order_subtypes = models.TextField(default=None, null=True)
    
    trade_eligible = models.BooleanField(default=False)
    options_eligible = models.BooleanField(default=False)
    buyable= models.BooleanField(default=False)
    sellable= models.BooleanField(default=False)

    active_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now=True, editable=False)
    last_synced = models.DateTimeField(default=timezone.now)
    accounts = models.ManyToManyField(Account, through='AccountPosition')

class AccountPosition (models.Model):
    id =  models.UUIDField(default=uuid.uuid4, max_length=30, editable=False, primary_key=True)
    quantity = models.DecimalField(default=0, max_digits=20, decimal_places=2, null=True)
    amount = models.DecimalField(default=0, max_digits=20, decimal_places=2, null=True)

    is_active = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    security = models.ForeignKey(Security, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['security_id', 'account_id'], name='account_security_key')
        ]
    

class SecurityGroup (models.Model):
    id = models.CharField(default=None, max_length=255, primary_key=True)
    name = models.CharField(default=None, max_length=255, null=True)
    description = models.CharField(default=None, max_length=255, null=True)
    created_at = models.DateTimeField(auto_now=True, editable=False)
    securities = models.ManyToManyField(Security, related_name='groups')

class Activity (models.Model):
    id = models.CharField(default=None, max_length=255, primary_key=True)
    currency = models.CharField(default=None, max_length=30, null=True)
    type = models.CharField(default=None, max_length=30)
    sub_type = models.CharField(default=None, max_length=30, null=True)
    action = models.CharField(default=None, max_length=30, null=True)
    stop_price = models.DecimalField(default=0,max_digits=10, decimal_places=2, null=True)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    quantity = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    amount = models.DecimalField(default=0,max_digits=10, decimal_places=2, null=True)
    commission = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    option_multiplier = models.CharField(default=None, max_length=255, null=True)

    symbol = models.CharField(default=None, max_length=255, null=True)
    market_currency = models.CharField(default=None, max_length=20, null=True)
    status = models.CharField(default=None, max_length=20, null=True)
    
    cancelled_at = models.DateTimeField(default=None, null=True)
    rejected_at = models.DateTimeField(default=None, null=True)
    submitted_at = models.DateTimeField(default=None, null=True)
    filled_at = models.DateTimeField(default=None, null=True)
    created_at = models.DateTimeField(auto_now=True, editable=False)
    last_updated= models.DateTimeField(default=timezone.now)
    last_synced= models.DateTimeField(default=timezone.now)

    security = models.ForeignKey(Security,null=True, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)


class Deposit (models.Model):
    id = models.CharField(default=None, max_length=255, primary_key=True)
    bank_account_id = models.CharField(default=None, max_length=255, null=True)
    status = models.CharField(default=None, max_length=255, null=True)
    currency = models.CharField(default=None, max_length=30)
    amount= models.DecimalField(default=0,max_digits=10, decimal_places=2, null=True)
    cancelled_at = models.DateTimeField(default=None, null=True)
    rejected_at = models.DateTimeField(default=None, null=True)
    accepted_at = models.DateTimeField(default=None, null=True)
    accepted_at = models.DateTimeField(default=None, null=True)
    created_at = models.DateTimeField(default=None, editable=False)
    last_synced= models.DateTimeField(default=None, null=True)

    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)

