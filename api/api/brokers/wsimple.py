import json
import yaml
import datetime
from datetime import timezone
from pathlib import Path
import traceback

from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
from rest_framework import status
from django.db import IntegrityError

from ...wsConnector.wealthSimple import wealthSimple
from ...models import Account, Activity, Security, SecurityGroup, AccountPosition, Deposit
from ...serializers import ActivitySerializer, SecuritySerializer, AccountSerializer, DepositSerializer

from ..helpers import safeBulkCreate, openFile, getActivityAction, setActivityAmountValue, setActivityPrice, setActivityCurrency
from.helperData import SECURITY_UPDATE_FIELDS , SECURITYGROUP_UPDATE_FIELDS,  ACCOUNTPOSITION_UPDATE_FIELDS,  ACTIVITY_UPDATE_FIELDS, DEPOSIT_UPDATE_FIELDS
from .helperData import WSIMPLE_ACTIVITY_TYPE_DICT
from .helperData import DEPOSIT_UNIQUE_FIELD, SECURITY_UNIQUE_FIELD, SECURITYGROUP_UNIQUE_FIELD, ACCOUNTPOSITION_UNIQUE_FIELD, ACTIVITY_UNIQUE_FIELD

config_base_path = Path(__file__).parent
data_path = Path(__file__).parent.parent.parent.parent
yaml_file_path = (config_base_path / "info/wsimple.yaml").resolve()
data_file_path = (data_path / "jsonData/wealthsimple").resolve()


def getToken(request):
    try:
        ws = getWSObject()
        token= ws.session.headers["Authorization"]
        return JsonResponse({"Token": token}, status=status.HTTP_200_OK)
    except Exception as error:
        print(traceback.format_exc())
        return JsonResponse({"error": str(error)}, status=status.HTTP_406_NOT_ACCEPTABLE)
    

def getOTP():
    # Obtain user input and ensure it is not empty
    MFACode = input("Enter 2FA code: ")
    return MFACode

def getWSObject ():
    try:
        wsimpleFile = openFile(yaml_file_path)
        email = wsimpleFile['email']
        password = wsimpleFile['password']
        wsOb = wealthSimple(
            email=email,
            password=password,
            two_factor_callback=getOTP
        )
        return wsOb
    except Exception as error:
        print(traceback.format_exc())
        return error

def syncSecurities (request):
    try:
        wsObject = getWSObject()
        fetchedSecurity = wsObject.get_security('sec-s-eee8666b01044614b809e47e72fc3c1f')
        return JsonResponse({"securityGroup": fetchedSecurity}, status=status.HTTP_200_OK)
    except Exception as error:
        print(error)
        print(traceback.format_exc())
        return JsonResponse({"error": str(error)}, status=status.HTTP_406_NOT_ACCEPTABLE) 

def syncSecurityGroups (request):
    try:
        wsObject = getWSObject()
        fetchedData = wsObject.get_security_groups()
        objSecurityGrouptList = [ SecurityGroup(
            id= data['external_security_group_id'],
            description= data['description'],
            name= data['name']
        ) for data in fetchedData]
        print("Saving " + str(len(objSecurityGrouptList)) + " Security Groups")
        safeBulkCreate(SecurityGroup, objSecurityGrouptList, uniqueField=SECURITYGROUP_UNIQUE_FIELD,updateFields=SECURITYGROUP_UPDATE_FIELDS)
        
        return JsonResponse({"count":len(fetchedData),"securityGroups": fetchedData}, status=status.HTTP_200_OK)
    except Exception as error:
        print(traceback.format_exc())
        return JsonResponse({"error": str(error)}, status=status.HTTP_406_NOT_ACCEPTABLE)    

def syncAccounts (request):
    try:
        wsObject = getWSObject()
        fetchedData = wsObject.get_accounts()
        objAccountList = [ Account(
            account_number= data['id'],
            status= data['status'],
            current_balance= data['current_balance']['amount'],
            net_deposits= data['net_deposits']['amount'],
            currency= data['base_currency'],
            type= data['account_type'].split('_')[1].capitalize() + "-" + data['base_currency'],
            created_at= data['opened_at'],
            updated_at= parse_datetime(data['updated_at']),
            account_broker_id= 'Wealthsimple',
            linked_account_id= data['linked_account_id']
        ) for data in fetchedData]
        
        print("Saving Accounts ...")
        safeBulkCreate(Account, objAccountList, [], [])

        objAccountList = AccountSerializer(objAccountList, many=True).data
        return JsonResponse({"count":len(objAccountList),"accounts": objAccountList}, status=status.HTTP_200_OK)
    except Exception as error:
        print(traceback.format_exc())
        return JsonResponse({"error": str(error)}, status=status.HTTP_406_NOT_ACCEPTABLE)



def syncActivities (request):
    try:
        wsObject = getWSObject()
        activities = wsObject.get_activities(limit=99)
        activitiesObjList = []
        securitiesObjList = []

        for activity in activities:
            
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

        print("Saving " + str(len(securitiesObjList)) + " Securities.....")
        securityRecords = safeBulkCreate(Security, securitiesObjList,uniqueField=SECURITY_UNIQUE_FIELD,updateFields=SECURITY_UPDATE_FIELDS)
        print(str(len(securityRecords)) + " RECORDS \n")
        print("Saving " + str(len(activitiesObjList)) + " Activities.....")
        activitiesRecords = safeBulkCreate(Activity, activitiesObjList, uniqueField=ACTIVITY_UNIQUE_FIELD, updateFields=ACTIVITY_UPDATE_FIELDS)
        

        serializedActivities = ActivitySerializer(activitiesRecords, many=True).data
        serializedSecurities = SecuritySerializer(securitiesObjList, many=True).data

        return JsonResponse({"count": len(activities), "activities": serializedActivities, "securities": serializedSecurities }, status=status.HTTP_200_OK)
    except Exception as error:
        print(traceback.format_exc())
        return JsonResponse({"error": str(error)}, status=status.HTTP_406_NOT_ACCEPTABLE)

def syncPositions (request):
    try:
        accountIds = Account.objects.values_list('account_number', flat=True).exclude(account_broker_id="Questrade")
        wsObject = getWSObject()
        positions = []
        for id in accountIds:
            accountPositions = wsObject.get_positions(id)
            print("Account "+ id + " has " + str(len(accountPositions)) + " Positions \n")
            positions.append(accountPositions)
        
        positionsSecurities = [item for row in positions for item in row]
        objPositionsList = []
        objSecurityList = []
        securityGroupsObjList = []

        for security in positionsSecurities:

            objSecurityList.append(Security(
                id= security['id'],
                symbol= security['stock']['symbol'],
                name= security['stock']['name'],
                description = security['stock']['description'],
                type= "ETF" if security['security_type'] == "exchange_traded_fund" else security['security_type'],
                status= security['status'],
                
                currency= security['currency'],
                exchange = security['stock']['primary_exchange'],
                option_details = security['option_details'],
                order_subtypes= security['allowed_order_subtypes'],

                buyable= security['buyable'],
                sellable= security['sellable'],
                options_eligible = security['options_eligible'],
                trade_eligible = security['ws_trade_eligible'],

                active_date = parse_datetime(security['active_date'])
            ))

            objPositionsList.append(AccountPosition(
                amount = security['start_of_day_book_value']['amount'],
                quantity = security['start_of_day_quantity'],
                is_active = True,
                security_id = security['id'],
                account_id = security['account_id']
            ))

            for group in security['groups']:
                securityGroupsObjList.append(SecurityGroup(id=group['id'],name=group['name_en']))


        safeBulkCreate(Security, objSecurityList,uniqueField=SECURITY_UNIQUE_FIELD, updateFields=SECURITY_UPDATE_FIELDS)
        safeBulkCreate(AccountPosition, objPositionsList, uniqueField=ACCOUNTPOSITION_UNIQUE_FIELD, updateFields=ACCOUNTPOSITION_UPDATE_FIELDS)
        safeBulkCreate(SecurityGroup, securityGroupsObjList, uniqueField=SECURITYGROUP_UNIQUE_FIELD, updateFields=SECURITYGROUP_UPDATE_FIELDS)
        
        return JsonResponse({"count": len(positions),"positions": positionsSecurities}, status=status.HTTP_200_OK)
    except Exception as error:
        print(traceback.format_exc())
        return JsonResponse({"error": str(error)}, status=status.HTTP_406_NOT_ACCEPTABLE)
    

def syncDeposits(request):
    try:
        wsObject = getWSObject()
        fetchedDeposits = wsObject.get_deposits()
        depositsObj = [Deposit(
                id= deposit['id'],
                currency= deposit['value']['currency'],
                amount= deposit['value']['amount'],
                status= deposit["status"],
                cancelled_at = deposit["cancelled_at"],
                rejected_at = deposit['rejected_at'],
                accepted_at=  deposit['accepted_at'],
                created_at=  deposit['created_at'],
                last_synced=  datetime.datetime.now(timezone.utc) ,
                account_id= deposit['account_id']
            ) for deposit in fetchedDeposits]
        depositRecords = safeBulkCreate(Deposit,depositsObj, DEPOSIT_UNIQUE_FIELD, DEPOSIT_UPDATE_FIELDS)
        serializedSavedRecords = DepositSerializer(depositRecords,many=True).data
        return JsonResponse({"count": len(serializedSavedRecords) , "deposits": serializedSavedRecords}, status=status.HTTP_200_OK)
    except Exception as error:
        print(error)
        print(traceback.format_exc())
        return JsonResponse({"error": str(error)}, status=status.HTTP_406_NOT_ACCEPTABLE) 