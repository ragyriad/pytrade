from rest_framework import serializers 
from .models import Activity,Account, Security, SecurityGroup, Deposit

def serialize_datetime(val):
    """
    Serialize a datetime value to ISO 8601 format,
    or return an empty string if the value is None.
    """
    return "" if val is None else val.isoformat()


class ActivitySerializer (serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            'id',
            'currency',
            'type',
            'sub_type',
            'action',
            'stop_price',
            'price',
            'quantity',
            'amount',
            'commission',
            'option_multiplier',
            'symbol',
            'market_currency',
            'status',
            'cancelled_at',
            'rejected_at',
            'submitted_at',
            'filled_at',
            'created_at',
            'last_updated',
            'last_synced',
            'security',
            'account'
        ]

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = [
            'account_number',
            'type',
            'current_balance',
            'net_deposits',
            'currency',
            'status',
            'is_primary',
            'created_at',
            'updated_at',
            'last_synced',
            'linked_account_id',
            'account_broker_id'
        ]


class SecuritySerializer(serializers.ModelSerializer):

    class Meta:
        model = Security
        fields = [
            'id',
            'symbol',
            'name',
            'description',
            'type',
            'currency',
            'status',
            'exchange',
            'option_details',
            'order_subtypes',
            'trade_eligible',
            'options_eligible',
            'buyable',
            'sellable',
            'active_date',
            'created_at',
            'last_synced',
            'accounts'
        ]



class SecurityGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = SecurityGroup
        fields = [
            'id',
            'name',
            'description',
            'created_at',
            'securities'
        ]


class BrokerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Security
        fields = [
            'id',
            'name'
        ]

class AccountPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Security
        fields = [
            'id',
            'quantity',
            'amount',
            'is_active',
            'created_at',
            'updated_at',
            'security',
            'account'
        ]

class DepositSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deposit
        fields = [
            'id',
            'bank_account_id',
            'status',
            'currency',
            'amount',
            'cancelled_at',
            'rejected_at',
            'accepted_at',
            'created_at',
            'last_synced'
        ]