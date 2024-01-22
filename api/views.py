from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import requests 
from django.db.models import Q
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

        allActivities = []
        requestParams = dict(request.GET)
        requestKeys = list(requestParams.keys())
        doesItHaveAccount = "account" in requestKeys
        doesItHaveActivity = "activityType" in requestKeys
        doesItHaveCommission = "commissionFilter" in requestKeys
        query = Q()
        
        if doesItHaveAccount:
            accountsParameter = [int(val) for val in requestParams.get("account")[0].split(",")]
            if len(accountsParameter) > 0: 
                query = Q(accountNumber__in=accountsParameter)
        if doesItHaveActivity:
            activityTypeParameter = requestParams.get("activityType")[0].split(",")
            if len(activityTypeParameter) > 0: 
                query &= Q(type__in=activityTypeParameter)
                if "Commission" in activityTypeParameter:
                    query &= Q(commission__lt=0)

        print(query)
        allActivities =  Activity.objects.filter(query)
        serializedActivities= json.loads(serialize("json",allActivities))
        count = len(allActivities)
        print(count)
        return Response({'count': count,'activities': serializedActivities}, status=status.HTTP_200_OK)
    
class deleteActivity(APIView):
    def delete (self,request):
        deleteAction = Activity.objects.all().delete()
        return Response(deleteAction, status=status.HTTP_200_OK)

     