"""
URL configuration for crm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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

from . import views

urlpatterns = [
    path("", views.user_home, name="user_home"),
    path("customer/", views.customer_list, name="customer_list"),
    path("lead/", views.lead_list, name="lead_list"),
    path("opportunity/", views.opportunity_list, name="opportunity_list"),
    path("activity/", views.activity_list, name="activity_list"),
    path("task/", views.task_list, name="task_list"),
    
]

