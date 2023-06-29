from django.urls import path
from django.contrib import admin
from . import views
urlpatterns = [
    path('monthly-report/', views.monthly_report_api, name='monthly_report_api'),
]