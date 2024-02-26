from rest_framework import serializers 
from .models import Activity,Account,Position

def serialize_datetime(val):
    """
    Serialize a datetime value to ISO 8601 format,
    or return an empty string if the value is None.
    """
    return "" if val is None else val.isoformat()

class ActivitySerializers (serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['action','symbol','symbolId','currency','type','account_number','price','quantity','grossAmount','netAmount','commission','tradeDate','settlementDate','createdAt','lastModified']

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['account_number', 'type', 'current_balance', 'net_deposits', 'currency', 'last_synced', 'is_primary', 'linked_account_id', 'linked_account_fk', 'created_at', 'updated_at', 'status']

    last_synced = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_last_synced(self, obj):
        return serialize_datetime(obj.last_synced)

    def get_created_at(self, obj):
        return serialize_datetime(obj.created_at)

    def get_updated_at(self, obj):
        return serialize_datetime(obj.updated_at)

    class Meta:
        model = Account
        fields = '__all__'


class PositionSerializer (serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['action','symbol','symbolId','currency','type','account_number','price','quantity','grossAmount','netAmount','commission','tradeDate','settlementDate','createdAt','lastModified']
