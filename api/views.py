from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import requests 

from .serializers import getActivitySerializers, updateActivitySerializers
from .models import Activity
import yaml
from pathlib import Path

from questrade_api import Questrade

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.serializers import serialize
import json

def main (request):
    return HttpResponse("Hello")

questrade_info = ''
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

class updateActivity(APIView):
    serializer_class = updateActivitySerializers
    def get(self, request):
        questradeObject = authentication()
        infoFile = openFile()
        accountNumber = infoFile['accounts']['tfsa']
        ##numberOfYears = 5
        ##numberofMonths = 12
        ##for index in numberOfYears:
        ##    for index in 
        response = questradeObject.account_activities(accountNumber,startTime='2020-05-01T00:00:00-0',endTime='2020-05-30T00:00:00-0')
        activities = response['activities']
        
        for activity in activities:
            existingActivity = Activity.objects.filter(tradeDate=activity['tradeDate']).exists()
            if existingActivity is False:
                newActivity = Activity(tradeDate=activity['tradeDate'],settlementDate=activity['settlementDate'],
                        currency=activity['currency'], quantity=activity['quantity'],commission=activity['commission'],type=activity['type'],
                        netAmount=activity['netAmount'],grossAmount=activity['grossAmount'],symbol=activity['symbol'], price=activity['price'],
                        symbolId=activity['symbolId'],accountNumber=accountNumber)
                newActivity.save()

        return Response(response['activities'], status=status.HTTP_200_OK)
    
class getActivity(APIView):
    serializer_class = getActivitySerializers
    def get(self,request):
        allActivities = Activity.objects.all()
        serializedActivities= json.loads(serialize("json", allActivities))
        print(len(serializedActivities))
        return Response(serializedActivities, status=status.HTTP_200_OK)
        