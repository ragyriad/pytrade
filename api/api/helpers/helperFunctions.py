from .helperData import WSIMPLE_ACTIVITY_TYPE_DICT
from .helpers import getActivityAction, setActivityAmountValue, setActivityPrice, setActivityCurrency
from ...models import Activity, Security
def clean_fetch_activities_data(activities):
    activitiesObjList = []
    securitiesObjList = []

    for activity in activities:
        print(activity)
        actionFnData = {'object': activity['object'], 'orderType': activity['order_type'] if 'order_type' in activity else None, 'autoOrderType' : activity['auto_order_type'] if 'auto_order_type' in activity else None}
        amountValue = setActivityAmountValue(activity)
        symbolVal = activity["symbol"] if 'symbol' in activity else None
        
        accountIdVal = ''
        if 'internal_transfer' in activity:
            accountIdVal = activity['destination_account_id']
        if 'account_id' in activity:
            accountIdVal = activity['account_id']    
        marketCurrency = ''
        if 'market_currency' in activity:
            marketCurrency = activity['market_currency'] 
        elif 'net_cash' in  activity:
            marketCurrency = activity ['net_cash']['currency']
        else:
            marketCurrency =  None
        activityObj = Activity(
            id= activity['id'],
            currency= setActivityCurrency(activity),
            type= WSIMPLE_ACTIVITY_TYPE_DICT[activity['object']],
            sub_type = activity['order_sub_type'] if 'order_sub_type' in activity else None,
            action= getActivityAction(actionFnData) ,
            stop_price = activity['stop_price'] if 'stop_price' in activity else 0,
            price = setActivityPrice(activity),
            quantity= activity['quantity'] if 'quantity' in activity else 0,
            symbol = symbolVal,
            amount= amountValue,
            commission= activity['filledTotalTransactionFee']['amount'] if 'filledTotalTransactionFee' in activity else 0,
            option_multiplier= activity['option_multiplier'] if 'option_multiplier' in activity else None,
            market_currency = marketCurrency,
            status= activity["status"] if 'status' in activity else None,
            cancelled_at = activity["cancelled_at"] if 'cancelled_at' in activity else None,
            rejected_at = activity['rejected_at'] if 'rejected_at' in activity else None,
            submitted_at = activity['submitted_at'] if 'submitted_at' in activity else None,
            filled_at=  activity['filled_at'] if 'filled_at' in activity else None,
            account_id= accountIdVal,
            security_id= activity['security_id']  if 'security_id' in activity else None
        )
        activitiesObjList.append(activityObj)
        if 'security_id' in activity and activity['security_id'] not in (getattr(security, "id") for security in securitiesObjList):
            securityObj = Security(
                id= activity['security_id'],
                symbol=symbolVal,
                name= activity['security_name'],
                currency=setActivityCurrency(activity)
            )
            securitiesObjList.append(securityObj)
    return activitiesObjList, securitiesObjList