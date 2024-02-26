from ..views import Activity, Account

import json
from functools import reduce

from django.core.serializers import serialize

from rest_framework.decorators import api_view, renderer_classes
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from django.http import JsonResponse


def getAccountDividendsFn (request):
    print(request)
    serializedActivities= json.loads(serialize("json",Activity.objects.filter(type="Dividends")))
    dividendsList = list(map(lambda n : abs(float(n["fields"]["netAmount"])), serializedActivities))
    totalDividendAmount = round(reduce(lambda x, y: y + x, dividendsList),2)
    print(totalDividendAmount)
    return JsonResponse({'totalAmount': totalDividendAmount}, status=status.HTTP_200_OK)  

def getAccountCommissions (request):
    serializedActivities= json.loads(serialize("json",Activity.objects.filter(commission__lt=0)))
    commissionList = list(map(lambda n : abs(float(n["fields"]["commission"])), serializedActivities))
    totalCommissionAmount = round(reduce(lambda x, y: y + x, commissionList),2)
    return JsonResponse({'totalAmount': totalCommissionAmount,'activities': serializedActivities}, status=status.HTTP_200_OK) 
    

def getAccountDividends (request):
    serializedActivities= json.loads(serialize("json",Activity.objects.filter(type="Dividends")))
    dividendsList = list(map(lambda n : abs(float(n["fields"]["netAmount"])), serializedActivities))
    totalDividendAmount = round(reduce(lambda x, y: y + x, dividendsList),2)
    print(totalDividendAmount)
    return JsonResponse({'totalAmount': totalDividendAmount}, status=status.HTTP_200_OK)  
    
def getAccountTradesCount (request):
    accountActivities= json.loads(serialize("json",Activity.objects.filter(type="Trades")))
    resultsLength = len(accountActivities)
    print(resultsLength)
    return JsonResponse({'tradesCount': len(accountActivities)}, status=status.HTTP_200_OK) 