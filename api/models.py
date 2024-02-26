from django.db import models
from django.utils import timezone
from django.core.serializers import serialize

generate_unique_code=20


class Account (models.Model):
    account_number = models.CharField(default=0, max_length=20,primary_key=True)
    type = models.CharField(default='', max_length=20)
    current_balance = models.DecimalField(default=0, max_digits=20, decimal_places=0)
    net_deposits = models.DecimalField(default=0, max_digits=20, decimal_places=0)
    currency = models.CharField(default='', max_length=10)
    status = models.CharField(default='', max_length=10)
    is_primary = models.BooleanField(default=False)
    linked_account = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField( default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    last_synced = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.type

    def set_linked_account(self, other_account_number):
        try:
            related_account = Account.objects.get(account_number=other_account_number)
            self.linked_account = related_account
            self.save()
        except Account.DoesNotExist:
            print("The related account does not exist.")

    def get_all_linked_activities(self):
        if self.linked_account_id:
            return Activity.objects.filter(models.Q(account=self) | models.Q(account=self.linked_account_id))
        else:
            return Activity.objects.filter(account=self)
        
class Activity (models.Model):
    action = models.CharField(default='', max_length=20)
    symbol = models.CharField(default='', max_length=20)
    symbolId = models.CharField(default='', max_length=20)
    currency = models.CharField(default='', max_length=20)
    type = models.CharField(default='', max_length=20)

    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    quantity = models.DecimalField(default=0,max_digits=10, decimal_places=0)
    grossAmount = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    netAmount = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    commission = models.DecimalField(default=0,max_digits=10, decimal_places=2)

    tradeDate = models.DateTimeField(blank=True)
    settlementDate = models.DateTimeField(blank=True)
    createdAt = models.DateTimeField(auto_now_add = True)
    lastModified= models.DateTimeField(auto_now_add = True)
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)

class Position (models.Model):
    type = models.CharField(default='', max_length=20)
    name = models.CharField(default='', max_length=20)
    primary_exchange = models.CharField(default='', max_length=20)
    quantity = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    amount = models.DecimalField(default=0, max_digits=20, decimal_places=0)
    currency = models.CharField(default='', max_length=10)
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField( default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    last_synced = models.DateTimeField(default=timezone.now)