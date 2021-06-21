from django.urls import path
from bazdidkhodro.api.views import (
    VisitCreateAPIView,
    VisitListAPIView,
    InsurerListAPIView,
    InsurerCreateAPIView,
)
urlpatterns = [
    path('insurer_list/', InsurerListAPIView.as_view(), name='insurer_list_view'),
    path('insurer_create/', InsurerCreateAPIView.as_view(), name='insurer_create_view'),
    path('visit_create/', VisitCreateAPIView.as_view(), name='visit_create_view'),
    path('visit_list/', VisitListAPIView.as_view(), name='visit_list_view'),
    #path('image_update/<pk>/',ImageUpdateAPIView.as_view(), name='image_update_view'),
    #path('image_delete/<pk>/',ImageDeleteAPIView.as_view(), name='image_delete_view'),
    #path('show_images_by_year/',ImageGetByYearAPIView.as_view(), name='image_list_by_year_view'),
    #path('show_images_by_mobile/',ImageGetByMobileAPIView.as_view(), name='image_list_by_mobile_view'),
]
