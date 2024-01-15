from rest_framework import serializers 
from .models import Activity,Account

class getActivitySerializers (serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['action','symbol','symbolId','currency','type','accountNumber','price','quantity','grossAmount','netAmount','commission','tradeDate','settlementDate','createdAt','lastModified']

class updateActivitySerializers (serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['action','symbol','symbolId','currency','type','accountNumber','price','quantity','grossAmount','netAmount','commission','tradeDate','settlementDate','createdAt','lastModified']

class updateAccountsSerializers (serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['type','accountNumber','isPrimary']