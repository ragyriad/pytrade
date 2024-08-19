from ...models import Activity, Broker, Account

import json
from functools import reduce

from django.core.serializers import serialize
from django.http import JsonResponse
from rest_framework import status

                  
def getAccountDividendsFn (request):
    serializedActivities= json.loads(serialize("json",Activity.objects.filter(type="Dividends")))
    dividendsList = list(map(lambda n : abs(float(n["fields"]["netAmount"])), serializedActivities))
    totalDividendAmount = round(reduce(lambda x, y: y + x, dividendsList),2)
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
    return JsonResponse({'totalAmount': totalDividendAmount}, status=status.HTTP_200_OK)  
    
def getAccountTradesCount (request):
    accountActivities= json.loads(serialize("json",Activity.objects.filter(type="Trades")))
    resultsLength = len(accountActivities)
    return JsonResponse({'tradesCount': len(accountActivities)}, status=status.HTTP_200_OK) 