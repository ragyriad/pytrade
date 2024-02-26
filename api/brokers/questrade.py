import yaml
from pathlib import Path
import calendar, datetime
from datetime import timezone
import json
from questrade_api import Questrade
from ..models import Account

from django.core.serializers import serialize
from django.http import JsonResponse

from rest_framework import status

base_path = Path(__file__).parent
file_path = (base_path / "info/questrade.yaml").resolve()

def openFile():
    fileContent = ''
    with open(file_path,'r') as file:
        try:
            fileContent = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)
    return fileContent

def writeFile(newFileContent):
    with open(file_path, 'w') as file:
        documents = yaml.dump(newFileContent, file)
    return None

def authentication():
    print("Authenticating Questrade")
    fileContent = openFile()
    questObject = Questrade()
    
    try:
        questObject= Questrade(refresh_token=fileContent['refresh_token'])
    except Exception as e:
        print("Response")
        print(e)
        print("Most likely you will need a new refresh token")
    
    modifiedQuestradeInfo = fileContent
    modifiedQuestradeInfo['refresh_token'] = questObject.auth.token['refresh_token']
    modifiedQuestradeInfo['access_token'] = questObject.auth.token['access_token']
    modifiedQuestradeInfo['api_server'] = questObject.auth.token['api_server']
    writeFile(modifiedQuestradeInfo)
    return questObject


def syncQestradeAccounts(request):
    questradeObject = authentication()
    try:
        accounts = questradeObject.accounts
    except Exception as e:
        print (e)
    accounts = accounts['accounts']
    return JsonResponse({"count": len(accounts), "accounts": accounts}, status=status.HTTP_200_OK)
    #for account in accounts:
    #    accounToBeSaved = Account(type=account['type'],account_number=account['number'],)
    #    accounToBeSaved.save()
    #fetchedAccounts = json.loads(serialize("json",Account.objects.all()))
    #return Response({"count": len(fetchedAccounts), "accounts": fetchedAccounts}, status=status.HTTP_200_OK)
    
def syncQuestradeActivities (request):
        questradeObject = authentication()
        fetchedAccounts = json.loads(serialize("json",Account.objects.all()))
        all_activities = []
        for account in fetchedAccounts:
            account_number = account["fields"]["account_number"]
            print("Updating " + account["fields"]["type"] + " Account# " + 
                  account["fields"]["account_number"])  
            startingYear = 2019
            for year in range(startingYear, 2024):
                for month in range(1,13):
                    lastDayOfMonth = calendar.monthrange(year, month)[1]
                    queryStartTime = datetime.datetime(year, month, 1,tzinfo=timezone.utc)
                    queryEndTime = datetime.datetime(year, month, lastDayOfMonth,tzinfo=timezone.utc)
                    print(queryStartTime)
                    print(queryEndTime)
                    response = questradeObject.account_activities(account_number,startTime=queryStartTime,endTime=queryEndTime)
                    activities = response['activities']
                    if (len(activities) > 0):
                        for activity in activities:
                            newActivity = {'tradeDate' : activity['tradeDate'],'settlementDate':activity['settlementDate'],
                                    'currency':activity['currency'], 'quantity':activity['quantity'],"commission":activity['commission'],'type':activity['type'],
                                    'netAmount':activity['netAmount'],'grossAmount':activity['grossAmount'],'symbol':activity['symbol'], 'price':activity['price'],
                                    'symbolId':activity['symbolId'],'account_number':account_number}
                            all_activities.append(newActivity)
        print(all_activities)
        return JsonResponse(all_activities, status=status.HTTP_200_OK)