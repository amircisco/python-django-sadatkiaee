from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from django.conf.urls.static import static
from django.conf import settings
from account.views import install
from django.contrib import admin


admin.site.site_header = 'پرتال بیمه کوثر نمایندگی سادات کیایی'
admin.site.index_title = 'صفحه اصلی'
admin.site.site_title = 'سادات کیایی'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('install/', install,name="install"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/bazdidkhodro/', include('bazdidkhodro.api.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
