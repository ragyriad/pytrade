
from django.urls import path
from .views import brokerApiView, activityApiView , accountApiView, securityApiView, securityGroupApiView, AccountPositionApiView
from .api.brokers.questrade import syncQestradeAccounts, syncQuestradeActivities
from .api.brokers.wsimple import getToken, syncSecurities, syncDeposits, syncSecurityGroups, syncAccounts,syncActivities, syncPositions
from .api.helpers.data import getAccountDividendsFn, getAccountCommissions,getAccountDividends, getAccountTradesCount
from .api.auth import fetchCSRFToken
urlpatterns = [
    path('/questrade/account', syncQestradeAccounts),
    path('/questrade/activity', syncQuestradeActivities),
    path('/wealthsimple/account', syncAccounts),
    path('/wealthsimple/activity', syncActivities),
    path('/wealthsimple/position', syncPositions),
    path('/wealthsimple/security', syncSecurities),
    path('/wealthsimple/deposit', syncDeposits),
    path('/wealthsimple/securitygroup', syncSecurityGroups),
    path('/wealthsimple/auth', getToken),
    path('/wealthsimple/auth/csrf', fetchCSRFToken),
    path('/broker', brokerApiView.as_view()),
    path('/security', securityApiView.as_view()),
    path('/securitygroup', securityGroupApiView.as_view()),
    path('/account', accountApiView.as_view()),
    path('/activity', activityApiView.as_view()),
    path('/position', AccountPositionApiView.as_view()),
    path('/account/commission', getAccountDividendsFn),
    path('/overview/commission', getAccountCommissions),
    path('/overview/dividends', getAccountDividends),
    path('/overview/trades', getAccountTradesCount)
]
