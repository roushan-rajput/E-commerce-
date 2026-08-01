"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from app import views
import project.settings as settings
import django.conf.urls.static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('admindash/', views.admindash, name='admindash'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('forgetpass/', views.forgetpass, name='forgetpass'),
    path('send_otp/', views.forgetpass, name='send_otp'),
    path('verifyotp/', views.verifyotp, name='verifyotp'),
    # path('passwordreset/', views.passwordreset, name='passwordreset'),


#product urls
    path('addpro/', views.addpro, name='addpro'),                 
    path('allpro/', views.allpro, name='allpro'),                  
    path("editpro/<int:product_id>/", views.editpro, name="editpro"),    
    path('deletepro/<int:product_id>/', views.deletepro, name='deletepro'),   
]


if settings.DEBUG:

    urlpatterns += django.conf.urls.static.static(

        settings.MEDIA_URL,

        document_root=settings.MEDIA_ROOT

    )