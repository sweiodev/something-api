"""something_api URL Configuration

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
from django.urls import path
from api import views

urlpatterns = [
    # front-end
    path('admin/', admin.site.urls),
    path('', views.home, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('documentation/', views.documentation, name='documentation'),

    # user register login logout
    path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    # endpoints
    path('image-manipulation/triggered', views.Triggered.as_view(), name='triggered'),
    path('image-manipulation/blur', views.Blur.as_view(), name='blur'),
    path('image-manipulation/pixelate', views.Pixelate.as_view(), name='pixelate'),
    path('image-manipulation/flip', views.Flip.as_view(), name='flip'),
    path('image-manipulation/rotate', views.Rotate.as_view(), name='rotate'),
]
