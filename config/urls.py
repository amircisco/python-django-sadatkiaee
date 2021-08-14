from django.contrib import admin
from django.urls import path, include
# from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from rest_framework_simplejwt.views import TokenVerifyView
from account.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings
from account.views import home_to_admin
from django.contrib import admin


admin.site.site_header = 'پرتال بیمه کوثر نمایندگی سادات کیایی'
admin.site.index_title = 'صفحه اصلی'
admin.site.site_title = 'سادات کیایی'


urlpatterns = [
    path('', home_to_admin,name="home_to_admin"),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/bazdidkhodro/', include('bazdidkhodro.api.urls')),
    path('api/timesheet/', include('timesheet.api.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
