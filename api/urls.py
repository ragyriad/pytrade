
from django.urls import path
from .views import activityApiView , accountApiView
from .questrade_api.questrade_fetch import fetchQestradeAccounts, fetchQuestradeActivities
from .dataMethods.dataCrunch import getAccountDividendsFn, getAccountCommissions,getAccountDividends, getAccountTradesCount
urlpatterns = [
    path('/questrade/account', fetchQestradeAccounts),
    path('/questrade/activity', fetchQuestradeActivities),
    path('/account', accountApiView.as_view()),
    path('/activity', activityApiView.as_view()),
    path('/account/commission', getAccountDividendsFn),
    path('/overview/commission', getAccountCommissions),
    path('/overview/dividends', getAccountDividends),
    path('/overview/trades', getAccountTradesCount)
    
]
