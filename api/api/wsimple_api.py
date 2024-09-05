import datetime
from datetime import timezone
import json
from pathlib import Path
import traceback
import asyncio
from requests.exceptions import ConnectionError, Timeout
from functools import wraps
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.http import require_http_methods

from .errors import LoginError, WSOTPError, AppError
from .wealthsimple.redis_cache import get_instance_cache, set_instance_cache, del_instance_cache
from .wealthsimple.wealthSimple import wealthSimple
from ..models import Account, Activity, Security, SecurityGroup, AccountPosition, Deposit
from ..serializers import ActivitySerializer, SecuritySerializer, AccountSerializer, DepositSerializer

from .helpers.helpers import safeBulkCreate, writeFile, openFile, append_to_file
from .helpers.helperFunctions import clean_fetch_activities_data
from .data.constants import SECURITY_UPDATE_FIELDS , SECURITYGROUP_UPDATE_FIELDS,  SECURITYGROUP_UNIQUE_FIELD, SECURITY_UNIQUE_FIELD
from .data.constants import ACTIVITY_UPDATE_FIELDS, DEPOSIT_UPDATE_FIELDS, ACTIVITY_UNIQUE_FIELD
from .data.constants import ACCOUNTPOSITION_UNIQUE_FIELD, ACCOUNTPOSITION_UPDATE_FIELDS, DEPOSIT_UNIQUE_FIELD
from .data.constants import WEALTHSIMPLE_ACITIVITIES_TYPES

config_base_path = Path(__file__).parent
data_path = Path(__file__).parent.parent.parent.parent
yaml_file_path = (config_base_path / "data/wsimple.yaml").resolve()
data_file_path = (data_path / "jsonData/wealthsimple").resolve()

def getOTP():
    # Obtain user input and ensure it is not empty
    MFACode = input("Enter 2FA code: ")
    return MFACode

def handle_errors(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except (ConnectionError, Timeout) as e:
            error = LoginError(message="Connection error or timeout occurred.")
            error.traceback = traceback.format_exc()
            print(error.traceback)
            return JsonResponse(
                {"error_message": error.message, "error_traceback": error.traceback},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except WSOTPError as e:
            e.traceback = traceback.format_exc()
            print(e.traceback)
            return JsonResponse(
                {"error_message": e.message, "error_traceback": e.traceback},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except AppError as e:
            e.traceback = traceback.format_exc()
            print(e.traceback)
            return JsonResponse(
                {"error_message": e.message, "error_traceback": e.traceback},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            error_message = str(e)
            error_traceback = traceback.format_exc()
            print(error_traceback)
            return JsonResponse(
                {"error_message": error_message, "error_traceback": error_traceback},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return _wrapped_view


def getWsConnection(mfaCode=None):
    del_instance_cache('ws_instance')
    ws_instance = get_instance_cache()
    if ws_instance is None:
        wsimpleFile = openFile(yaml_file_path)
        email = wsimpleFile['email']
        password = wsimpleFile['password']
        new_instance = wealthSimple(email=email, password=password, mfa_code=mfaCode)
        expiry_datetime = new_instance.box.access_expires
        print(f"expiry date {expiry_datetime}")
        del new_instance.logger
        print("New Instance WS Connection")
        print(new_instance.__dict__)
        set_instance_cache(new_instance,expiry_datetime)
        return new_instance
    else:
        return ws_instance

@handle_errors 
def login(request):
    print("Login Body MFA")
    
    mfaCode = int(request.body)
    print(mfaCode)
    ws_instance = getWsConnection(mfaCode)
    print("login completed wsimple.py")
    refresh_token = ws_instance.box.refresh_token
    access_expiry = ws_instance.box.access_expires
    if refresh_token:
        fileContent = openFile(yaml_file_path)
        fileContent['refresh_token'] = refresh_token
        writeFile(yaml_file_path, fileContent)
        return JsonResponse({"access_expiry": access_expiry, "ws_refresh_token": refresh_token}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"error": LoginError}, status=status.HTTP_401_UNAUTHORIZED)

@handle_errors
def syncSecurities (request):

    ws_instance = getWsConnection()
    fetchedSecurity = ws_instance.get_security('sec-s-eee8666b01044614b809e47e72fc3c1f')
    return JsonResponse({"securityGroup": fetchedSecurity}, status=status.HTTP_200_OK)

def syncSecurityGroups (request):
    try:
        ws_instance =  getWsConnection()
        fetchedData = ws_instance.get_security_groups()
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

@handle_errors
def syncAccounts (request):
    try:
        ws_instance = getWsConnection()
        fetchedData = ws_instance.get_accounts()
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
        return JsonResponse({"count": len(objAccountList),"accounts": objAccountList}, status=status.HTTP_200_OK)
    except Exception as error:
        print(traceback.format_exc())
        return JsonResponse({"error": str(error)}, status=status.HTTP_406_NOT_ACCEPTABLE)

@handle_errors
async def fetch_data_async(ws_instance, params_list):
    # tasks = [wsObject.get_activities(params) for params in params_list]
    # results = await asyncio.gather(*tasks)
    results = []

    #for params in params_list:
    result = ws_instance.get_activities(params_list)["results"]
    print(result)
    if "error" in result:
        print("fetch_data_async")
        print(result)
        return result
    append_to_file('./api/api/testData/data.txt', result["results"])
    results.append(results.append(result["results"]))
        
    return {"results": result, "status": 200}
    
@require_http_methods(["POST"])
@handle_errors
def syncActivities(request):
    data = json.loads(request.body)
    ws_instance = getWsConnection()
    print("Tokens before activities call")
    print(ws_instance.box.tokens)
    refresh_token = data.get('refreshToken')
    instance = None
    if ws_instance is None:
        instance = getWsConnection()
    else:
        instance = get_instance_cache()
    params_list = [
        {"limit": 99, "type": type_} 
        for type_ in WEALTHSIMPLE_ACITIVITIES_TYPES
        if type_ != "all"
    ]
    
    fetched_results = asyncio.run(fetch_data_async(instance, params_list))
    if "error" in fetched_results:
        return JsonResponse({"error": fetched_results["error"]}, status=fetched_results["status"])
    
    # Process results
    activities = [activity for result in fetched_results for activity in result]
    activitiesObjList, securitiesObjList = clean_fetch_activities_data(activities)
    
    # Log and save activities and securities
    print(f"Saving {len(securitiesObjList)} Securities.....")
    securityRecords = safeBulkCreate(Security, securitiesObjList, uniqueField=SECURITY_UNIQUE_FIELD, updateFields=SECURITY_UPDATE_FIELDS)
    print(f"{len(securityRecords)} RECORDS \n")
    print(f"Saving {len(activitiesObjList)} Activities.....")
    activitiesRecords = safeBulkCreate(Activity, activitiesObjList, uniqueField=ACTIVITY_UNIQUE_FIELD, updateFields=ACTIVITY_UPDATE_FIELDS)
    
    # Serialize data for response
    serializedActivities = ActivitySerializer(activitiesRecords, many=True).data
    serializedSecurities = SecuritySerializer(securitiesObjList, many=True).data

    return JsonResponse({
        "count": len(activities), 
        "activities": serializedActivities, 
        "securities": serializedSecurities
    }, status=status.HTTP_200_OK)

@handle_errors
def syncPositions(request):

    accountIds = Account.objects.values_list('account_number', flat=True).exclude(account_broker_id="Questrade")
    wsObject = getWsConnection()
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

@handle_errors
def syncDeposits(request):
    wsObject = getWsConnection()
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

