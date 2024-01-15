import yaml
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import requests 
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.serializers import serialize

from ..serializers import getActivitySerializers, updateActivitySerializers, updateAccountsSerializers
from ..models import Activity, Account

from pathlib import Path
import calendar, datetime,time
from datetime import timezone
import json
from questrade_api import Questrade

base_path = Path(__file__).parent
file_path = (base_path / "questrade_info/info.yaml").resolve()

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
    
    fileContent = openFile()
    questObject= Questrade(refresh_token=fileContent['refresh_token'])

    modifiedQuestradeInfo = fileContent
    modifiedQuestradeInfo['refresh_token'] = questObject.auth.token['refresh_token']
    modifiedQuestradeInfo['access_token'] = questObject.auth.token['access_token']
    modifiedQuestradeInfo['api_server'] = questObject.auth.token['api_server']
    writeFile(modifiedQuestradeInfo)
    return questObject


class fetchQestradeAccounts(APIView):
    serializer_class = updateAccountsSerializers
    def get(self, request):
        questradeObject = authentication()
        accounts = questradeObject.accounts
        accounts = accounts['accounts']
        
        for account in accounts:
            accounToBeSaved = Account(type=account['type'],accountNumber=account['number'],)
            accounToBeSaved.save()
        fetchedAccounts = json.loads(serialize("json",Account.objects.all()))
        return Response({"count": len(fetchedAccounts), "accounts": fetchedAccounts}, status=status.HTTP_200_OK)
    
class   fetchQuestradeActivities (APIView):
    serializer_class = updateActivitySerializers
    def get(self, request):
        questradeObject = authentication()
        fetchedAccounts = json.loads(serialize("json",Account.objects.all()))
        all_activities = []
        for account in fetchedAccounts:
            accountNumber = account["fields"]["accountNumber"]
            print("Updating " + account["fields"]["type"] + " Account# " + 
                  account["fields"]["accountNumber"])  
            startingYear = 2019
            for year in range(startingYear, 2024):
                for month in range(1,13):
                    lastDayOfMonth = calendar.monthrange(year, month)[1]
                    queryStartTime = datetime.datetime(year, month, 1,tzinfo=timezone.utc)
                    queryEndTime = datetime.datetime(year, month, lastDayOfMonth,tzinfo=timezone.utc)
                    print(queryStartTime)
                    print(queryEndTime)
                    response = questradeObject.account_activities(accountNumber,startTime=queryStartTime,endTime=queryEndTime)
                    activities = response['activities']
                    print(activities[0])
                    print(len(activities))
                    if (len(activities) > 0):
                        for activity in activities:
                            newActivity = {'tradeDate' : activity['tradeDate'],'settlementDate':activity['settlementDate'],
                                    'currency':activity['currency'], 'quantity':activity['quantity'],"commission":activity['commission'],'type':activity['type'],
                                    'netAmount':activity['netAmount'],'grossAmount':activity['grossAmount'],'symbol':activity['symbol'], 'price':activity['price'],
                                    'symbolId':activity['symbolId'],'accountNumber':accountNumber}
                            
                            activityToSave = Activity(tradeDate=activity['tradeDate'],settlementDate=activity['settlementDate'],
                                    currency=activity['currency'], quantity=activity['quantity'],commission=activity['commission'],type=activity['type'],
                                    netAmount=activity['netAmount'],grossAmount=activity['grossAmount'],symbol=activity['symbol'], price=activity['price'],
                                    symbolId=activity['symbolId'],accountNumber=accountNumber)
                            activityToSave.save()
                            all_activities.append(newActivity)
                                
        print("TOTAL ACTIVITIES")
        print(len(all_activities))
        #activitiesObj = Activity.objects.bulk_create(updateActivitySerializers(all_activities), batch_size=(len(all_activities)/2))
        return Response(all_activities, status=status.HTTP_200_OK)