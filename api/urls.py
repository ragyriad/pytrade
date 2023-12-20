
from django.urls import path
from .views import main, updateActivity, getActivity

urlpatterns = [
    path('/account/activity_update', updateActivity.as_view()),
    path('/account/activity_all', getActivity.as_view())
]
