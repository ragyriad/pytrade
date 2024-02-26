
from django.urls import path
from .views import activityApiView , accountApiView, positionApiView
from .brokers.questrade import syncQestradeAccounts, syncQuestradeActivities
from .brokers.wsimple import syncAccounts,syncActivities, syncPositions
from .dataMethods.dataCrunch import getAccountDividendsFn, getAccountCommissions,getAccountDividends, getAccountTradesCount
urlpatterns = [
    path('/questrade/account', syncQestradeAccounts),
    path('/questrade/activity', syncQuestradeActivities),
    path('/wealthsimple/account', syncAccounts),
    path('/wealthsimple/activity', syncActivities),
    path('/wealthsimple/position', syncPositions),
    path('/account', accountApiView.as_view()),
    path('/activity', activityApiView.as_view()),
    path('/position', positionApiView.as_view()),
    path('/account/commission', getAccountDividendsFn),
    path('/overview/commission', getAccountCommissions),
    path('/overview/dividends', getAccountDividends),
    path('/overview/trades', getAccountTradesCount)
]
