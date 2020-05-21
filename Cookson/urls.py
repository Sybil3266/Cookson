"""Cookson URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from User.views import index
from Recipe.views import RecipeListView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('Stream/', include('Stream.urls')),
    path('user/', include('User.urls')),
    path('admin/', admin.site.urls),
    path('receipe/', RecipeListView.as_view(), name='recipe-list'),
    path('', index), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 