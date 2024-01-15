
from django.urls import path
from .views import main, getActivity, deleteActivity ,deleteAccount, getAccount
from .questrade_api.questrade_fetch import fetchQestradeAccounts, fetchQuestradeActivities
from .dataMethods.dataCrunch import getAccountCommissions,getAccountDividends, getAccountTradesCount
urlpatterns = [
    path('/questrade/account/get_all', fetchQestradeAccounts.as_view()),
    path('/questrade/activity/get_all', fetchQuestradeActivities.as_view()),
    path('/account/get_all', getAccount.as_view()),
    path('/account/delete_all', deleteAccount.as_view()),
    path('/overview/commission', getAccountCommissions.as_view()),
    path('/overview/dividends', getAccountDividends.as_view()),
    path('/overview/trades', getAccountTradesCount.as_view()),
    path('/activity', getActivity.as_view()),
    path('/activity/delete_all', deleteActivity.as_view())
    
]
