from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import requests 
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.serializers import serialize

from .serializers import getActivitySerializers, updateActivitySerializers, updateAccountsSerializers
from .models import Activity, Account

from pathlib import Path
import calendar, datetime,time
from datetime import timezone
import json

base_path = Path(__file__).parent
file_path = (base_path / "questrade_info/info.yaml").resolve()


def main (request):
    return HttpResponse("Hello")

class getAccount(APIView):
    serializer_class = getActivitySerializers
    def get(self,request):
        fetchedAccounts = Account.objects.all()
        serializedAccounts= json.loads(serialize("json",fetchedAccounts))
        count = len(serializedAccounts)
        return Response({'count': count,'accounts': serializedAccounts}, status=status.HTTP_200_OK)

class deleteAccount(APIView):
    def delete (self,request):
        records = Account.objects.all()
        return Response(Account.objects.all().delete(), status=status.HTTP_200_OK)
    
class getActivity(APIView):
    serializer_class = getActivitySerializers
    def get(self,request):
        requestAccountNumber = request.GET.get('accountNumber')
        allActivities = []
        if requestAccountNumber!= None:
            allActivities = Activity.objects.filter(accountNumber=int(requestAccountNumber))
        else:
            allActivities =  Activity.objects.all()
        serializedActivities= json.loads(serialize("json",allActivities))
        count = len(allActivities)
        return Response({'count': count,'activities': serializedActivities}, status=status.HTTP_200_OK)
    
class deleteActivity(APIView):
    def delete (self,request):
        deleteAction = Activity.objects.all().delete()
        return Response(deleteAction, status=status.HTTP_200_OK)

     