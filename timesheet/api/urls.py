from django.urls import path
from .views import GetSheetAPIView, EnterTimeSheetAPIView, ExitTimeSheetAPIView

urlpatterns = [
    path('gettimesheet/', GetSheetAPIView.as_view(), name="get_timesheet"),
    path('entertimesheet/', EnterTimeSheetAPIView.as_view(), name="enter_timesheet"),
    path('exittimesheet/', ExitTimeSheetAPIView.as_view(), name="exit_timesheet"),
]