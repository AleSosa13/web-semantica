"""
URL configuration for semantic_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from db_researchers.views import db_researcher_view, researcher_type, researcher_types

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', db_researcher_view, name='dbresearcher-list'),
    path('types', researcher_types, name='researcher-types'),
    path('types/<str:type>', researcher_type, name='researcher-type'),
]
