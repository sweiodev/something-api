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
from api import views_api

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
    path('image-manipulation/triggered', views_api.Triggered.as_view(), name='triggered'),
    path('image-manipulation/blur', views_api.Blur.as_view(), name='blur'),
    path('image-manipulation/pixelate', views_api.Pixelate.as_view(), name='pixelate'),
    path('image-manipulation/flip', views_api.Flip.as_view(), name='flip'),
    path('image-manipulation/rotate', views_api.Rotate.as_view(), name='rotate'),
    path('image-manipulation/grayscale', views_api.Grayscale.as_view(), name='grayscale'),
    path('image-manipulation/blend', views_api.Blend.as_view(), name='blend'),
    path('image-manipulation/enhance', views_api.Enhance.as_view(), name='enhance'),
]
