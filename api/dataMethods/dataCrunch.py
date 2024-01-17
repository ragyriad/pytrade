from ..views import Activity, Account
from django.db.models import Sum

import json
from functools import reduce

from rest_framework import status
from rest_framework.response import Response
from django.core.serializers import serialize
from rest_framework.views import APIView


class getAccountCommissions (APIView):
    def get (self,request):
        serializedActivities= json.loads(serialize("json",Activity.objects.filter(commission__lt=0)))
        commissionList = list(map(lambda n : abs(float(n["fields"]["commission"])), serializedActivities))
        totalCommissionAmount = round(reduce(lambda x, y: y + x, commissionList),2)
        return Response({'totalAmount': totalCommissionAmount,'activities': serializedActivities}, status=status.HTTP_200_OK) 
    

class getAccountDividends (APIView):
    def get (self, request):
        serializedActivities= json.loads(serialize("json",Activity.objects.filter(type="Dividends")))
        dividendsList = list(map(lambda n : abs(float(n["fields"]["netAmount"])), serializedActivities))
        totalDividendAmount = round(reduce(lambda x, y: y + x, dividendsList),2)
        print(totalDividendAmount)
        return Response({'totalAmount': totalDividendAmount}, status=status.HTTP_200_OK)  
    
class getAccountTradesCount (APIView):
    def get (self, request):
        accountActivities= json.loads(serialize("json",Activity.objects.filter(type="Trades")))
        resultsLength = len(accountActivities)
        print(resultsLength)
        return Response({'tradesCount': resultsLength}, status=status.HTTP_200_OK) 