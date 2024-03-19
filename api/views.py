from django.http import JsonResponse
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.serializers import serialize

from .serializers import BrokerSerializer, ActivitySerializer, AccountSerializer, AccountPositionSerializer, SecuritySerializer, SecurityGroupSerializer, DepositSerializer
from .models import Broker, Activity, Account, Security,SecurityGroup, AccountPosition, Deposit

from pathlib import Path

base_path = Path(__file__).parent
file_path = (base_path / "questrade_info/info.yaml").resolve()

class accountApiView(APIView):
    serializer_class = AccountSerializer

    def get(self,request):
        dataObjects = Account.objects.all()
        fetchedAccounts = AccountSerializer(dataObjects, many=True).data
        count = len(fetchedAccounts)

        return Response({'count': count,'accounts': fetchedAccounts}, status=status.HTTP_200_OK)
    
    def delete(self,request):
        try:
            accountsToDelete = Account.objects.all()
            accountsToDeleteSerialized = AccountSerializer(accountsToDelete, many=True).data
            response = accountsToDelete.delete()
            return Response({"response":  response, "data": accountsToDeleteSerialized}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return JsonResponse({"error": str(error)}, status=status.HTTP_406_NOT_ACCEPTABLE)
        

class activityApiView(APIView):
    serializer_class = ActivitySerializer

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
        allActivities =  ActivitySerializer(Activity.objects.filter(query),many=True).data
        count = len(allActivities)
        print(count)
        return Response({'count': count,'activities': allActivities}, status=status.HTTP_200_OK)
    
    ## Method should delete the data however there is no longer access to this data 
    ## and it needs to be preserved. The method was previously used is preserved to maintain design
    def delete (self,request):
        activitiesToDelete = Activity.objects.all()
        serializedActivities= ActivitySerializer(activitiesToDelete, many=True).data
        activitiesToDelete.delete()
        return Response({"action": "Deleted", "data": serializedActivities}, status=status.HTTP_200_OK)

# class positionApiView(APIView):
#     serializer_class = PositionSerializer

#     def get(self,request):
#         fetchedPositions = PositionSerializer(Position.objects.all(), many=True).data
#         count = len(fetchedPositions)
#         return Response({'count': count,'Positions': fetchedPositions}, status=status.HTTP_200_OK)
    

class securityApiView(APIView):
    serializer_class = SecuritySerializer

    def get(self,request):
        securities = SecuritySerializer(Security.objects.all(), many=True).data
        count = len(securities)
        return Response({'count': count,'securities': securities}, status=status.HTTP_200_OK)
    
class brokerApiView(APIView):
    serializer_class = BrokerSerializer

    def get(self,request):
        securities = BrokerSerializer(Broker.objects.all(), many=True).data
        count = len(securities)
        return Response({'count': count,'brokers': securities}, status=status.HTTP_200_OK)
    
class securityGroupApiView(APIView):

    def get(self,request):
        securityGroups = SecurityGroupSerializer(SecurityGroup.objects.all(), many=True).data
        print(securityGroups)
        count = len(securityGroups)
        return Response({'count': count,'security Groups': securityGroups}, status=status.HTTP_200_OK)
    
class AccountPositionApiView(APIView):

    def get(self,request):
        accountPositions = AccountPositionSerializer(AccountPosition.objects.all(), many=True).data
        count = len(accountPositions)
        return Response({'Count': count,'Positions': accountPositions}, status=status.HTTP_200_OK)
    
class DepositApiView(APIView):

    def get(self,request):
        deposits = DepositSerializer(Deposit.objects.all(), many=True).data
        count = len(deposits)
        return Response({'Count': count,'Positions': deposits}, status=status.HTTP_200_OK)