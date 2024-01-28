from django.contrib import admin
from django.urls import path,include
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler400
from django.conf.urls import handler403
from django.conf.urls import handler404
from django.conf.urls import handler500
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView
handler400=handler="Huerto.views.mi_error_400"
handlar403=handler="Huerto.views.mi_error_403"
handler404 = handler="Huerto.views.mi_error_404"#esto en la diapositiva aparece como handler404="app.views.view"
handler500=handler="Huerto.views.mi_error_500"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Huerto.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('api/v1/',include('Huerto.api_urls')),#en api se puede poner lo que queramos pero v1 es importante 
    path('oauth2/',include('oauth2_provider.urls',namespace='oauth2_provider')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
