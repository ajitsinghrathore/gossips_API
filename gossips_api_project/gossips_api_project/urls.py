from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt  import views as jwt_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/',include('Accounts.urls')),
    path('',include('Accounts.urls')),
    path('refresh_my_token/',jwt_views.TokenRefreshView.as_view())
]
