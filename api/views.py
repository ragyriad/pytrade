from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import requests 
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.serializers import serialize

from .serializers import ActivitySerializers, AccountSerializer,PositionSerializer
from .models import Activity, Account, Position

from pathlib import Path
import calendar, datetime,time
from datetime import timezone
import json

base_path = Path(__file__).parent
file_path = (base_path / "questrade_info/info.yaml").resolve()




class accountApiView(APIView):
    serializer_class = AccountSerializer

    def get(self,request):
        fetchedAccounts = AccountSerializer(Account.objects.all(), many=True).data
        #serializedAccounts= json.loads(serialize("json",fetchedAccounts))
        count = len(fetchedAccounts)
        return Response({'count': count,'accounts': fetchedAccounts}, status=status.HTTP_200_OK)
    
    def delete(self,request):
        try:
            accountsToDelete = Account.objects.exclude(type__in=['TFSA', "RRSP"])
            accountsToDeleteSerialized = AccountSerializer(accountsToDelete, many=True).data
            response = accountsToDelete.delete()
            return Response({"response":  response, "data": accountsToDeleteSerialized}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return JsonResponse({"error": str(error)}, status=status.HTTP_406_NOT_ACCEPTABLE)
        

class activityApiView(APIView):
    serializer_class = ActivitySerializers

    def get(self,request):
        allActivities = []
        requestParams = dict(request.GET)
        requestKeys = list(requestParams.keys())
        doesItHaveAccount = "account" in requestKeys
        doesItHaveActivity = "activityType" in requestKeys
        query = Q()
        
        if doesItHaveAccount:
            accountsParameter = [int(val) for val in requestParams.get("account")[0].split(",")]
            if len(accountsParameter) > 0: 
                query = Q(account_number__in=accountsParameter)
        if doesItHaveActivity:
            activityTypeParameter = requestParams.get("activityType")[0].split(",")
            print(activityTypeParameter)
            if len(activityTypeParameter) > 0: 
                query &= Q(type__in=activityTypeParameter)

        print(query)
        allActivities =  ActivitySerializers(Activity.objects.filter(query),many=True).data
        count = len(allActivities)
        print(count)
        return Response({'count': count,'activities': allActivities}, status=status.HTTP_200_OK)
    
    ## Method should delete the data however there is no longer access to this data 
    ## and it needs to be preserved. The method was previously used is preserved to maintain design
    def delete (self,request):
        activitiesToDelete = Activity.objects.all()
        serializedActivities= json.loads(serialize("json",activitiesToDelete))
        return Response({"action": "toDelete", "data": serializedActivities}, status=status.HTTP_200_OK)

class positionApiView(APIView):
    serializer_class = PositionSerializer

    def get(self,request):
        fetchedAccounts = PositionSerializer(Position.objects.all(), many=True).data
        count = len(fetchedAccounts)
        return Response({'count': count,'accounts': fetchedAccounts}, status=status.HTTP_200_OK)