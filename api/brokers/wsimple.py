import json
import yaml
from pathlib import Path
from django.utils.dateparse import parse_datetime
from django.core.serializers import serialize
import wealthsimple

from django.http import JsonResponse
from rest_framework import status
from ..models import Account, Activity

base_path = Path(__file__).parent
file_path = (base_path / "info/wsimple.yaml").resolve()


def syncAccounts (request):
    try:
        wsObject = authenticateWS()
        print("Accounts")
        keysToExtract = ["id","status","last_synced_at","created_at", "updated_at","current_balance","net_deposits","linked_account_id", "base_currency", "account_type"]
        
        accounts = extractData(wsObject.get_accounts(), keysToExtract)
        print(accounts)
        account_objects = [Account(**data) for data in accounts]
        #print(account_objects)
        print("Saving Accounts...")
        Account.objects.bulk_create(account_objects)
        return JsonResponse({"accounts": serialize('json', account_objects)}, status=status.HTTP_200_OK)
    except Exception as error:
        return JsonResponse({"error": str(error)}, status=status.HTTP_406_NOT_ACCEPTABLE)

def syncActivities (request):
    try:
        wsObject = authenticateWS()
        print("GET Activities")
        activities = wsObject.get_activities()
        print()
        return JsonResponse({"activities": activities}, status=status.HTTP_200_OK)
    except Exception as error:
        #errorJson = json.dumps(error)
        return JsonResponse({"error": str(error)}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
def deleteAccounts (request):
    try:
        accountsToDelete = Account.objects.exclude(type=['TFSA', "RRSP"])
        return JsonResponse({"Accounts": accountsToDelete}, status=status.HTTP_200_OK)
    except Exception as error:
        print(error)
        return JsonResponse({"error": str(error)}, status=status.HTTP_406_NOT_ACCEPTABLE)
    

def syncPositions (request):
    account_id="rrsp-pkpsgfn"
    try:
        wsObject = authenticateWS()
        positions = wsObject.get_positions(account_id)
        print("GET Positions")
        print(positions)
        return JsonResponse({"positions": positions}, status=status.HTTP_200_OK)
    except Exception as error:
        #errorJson = json.dumps(error)
        return JsonResponse({"error": str(error)}, status=status.HTTP_406_NOT_ACCEPTABLE)


def openFile():
    fileContent = ''
    with open(file_path,'r') as file:
        try:
            fileContent = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)
    return fileContent

def getOTP():

    # Obtain user input and ensure it is not empty
    MFACode = input("Enter 2FA code: ")
    return MFACode


def authenticateWS():
    print("Opening File...")
    wsimpleFile = openFile()
    email = wsimpleFile['email']
    password = wsimpleFile['password']
    try:
        print("Authenticating...")
        ws = wealthsimple.WSTrade(
        email=email,
        password=password,
        two_factor_callback=getOTP,
        )
        return ws
    except Exception as e:
        print("Error Response")
        print(e)
        return e


def extractData (dataList, keyList):
    filteredList = list(map(lambda dataDict: {key: dataDict[key] for key in keyList}, dataList))
    objList = []
    for data in filteredList:
        account_data = {
            'account_number': data['id'],
            'status': data['status'],
            'last_synced': parse_datetime(data['last_synced_at']),
            'created_at': parse_datetime(data['created_at']),
            'updated_at': parse_datetime(data['updated_at']),
            'current_balance': data['current_balance']['amount'],
            'net_deposits': data['net_deposits']['amount'],
            'linked_account_id': data['linked_account_id'],
            'currency': data['base_currency'],
            'type': data['account_type'],
        }
        objList.append(account_data)
    return objList