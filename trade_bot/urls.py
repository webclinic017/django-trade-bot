"""trade_bot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import settings 

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from home import views as home
from accounts import views as accounts

import django.contrib.auth.urls as auth_urls

from rest_framework import permissions
from rest_framework.decorators import api_view

from drf_yasg.views import get_schema_view

SchemaView = get_schema_view(
    validators=['ssv', 'flex'],
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),


    #api
    url(r'^api(?P<format>\.json|\.yaml)$', SchemaView.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^api/$', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('api/users/', include('accounts.urls')),
    path('api/coins/', include('coins.urls')),
    path('api/trade/', include('crypto.urls')),


    #front
    path('', home.index, name='index'),
    path('accounts/profile', accounts.profile, name="profile"),
    path('accounts/profile/orders', accounts.orders, name="orders"),
    path('accounts/profile/withdraws', accounts.withdraws, name="withdraws"),

    path('accounts/profile/team/delete', accounts.delete_team, name="profile_delete_team"),
    path('accounts/profile/team/create', accounts.create_team, name="profile_create_team"),
    path('accounts/profile/team/join/<int:pk>', accounts.join_team, name="profile_join_team"),
    
    path('login/', accounts.login, name="login"),
    path('register/', accounts.register, name='register'),
    path('logout/', accounts.logout, name='logout'),

    path('teams', home.teams, name="teams"),
    path('markets', home.markets, name="markets"),

] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()