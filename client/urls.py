from django.urls import path
from django.contrib import admin
from . import views
urlpatterns = [
    path('home/',views.home,name='home'),
    path('profile/<int:id>',views.profile,name='profile'),
    path('upcoming-projects/',views.upcoming_order,name='upcoming_projects'),
    path('invoice',views.invoices,name="client_invoices"),
    path('settings',views.settings,name="client_settings")
]

