from django.urls import path
from bazdidkhodro.api.views import (
    VisitCreateAPIView,
    DocumentCreateAPIView,
    VisitListAPIView,
    InsurerListAPIView,
    InsurerCreateAPIView,
)
urlpatterns = [
    path('insurer_list/', InsurerListAPIView.as_view(), name='insurer_list_view'),
    path('insurer_create/', InsurerCreateAPIView.as_view(), name='insurer_create_view'),
    path('visit_create/', VisitCreateAPIView.as_view(), name='visit_create_view'),
    path('document_create/', DocumentCreateAPIView.as_view(), name='document_create_view'),
    path('visit_list/', VisitListAPIView.as_view(), name='visit_list_view'),
]
