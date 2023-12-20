from rest_framework import serializers 
from .models import Activity

class getActivitySerializers (serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['activity_id','action','symbol','price','tradeDate','Type','netAmount','commission', 'quantity','transactionDate','currency','symbolId']

class updateActivitySerializers (serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['activity_id','action','symbol','price','tradeDate','Type','netAmount','commission', 'quantity','transactionDate','currency','symbolId']