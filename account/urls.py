from django.urls import path
from django.contrib import admin
from . import views
urlpatterns = [
    path('',views.register,name='register'),
    path('register/',views.userregister,name='user_register'),
    path('client-register/',views.clientregister,name='client_register'),
    path('login/',views.userlogin,name='login'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('my-portfolio/',views.myportfolio,name='myportfolio'),
    path('edit_portfolio/',views.edit_portfolio,name='edit_portfolio'),
    path('my-projects/',views.myprojects,name='myprojects'),
    path('report/',views.report,name='crew_report'),
    path('logout/',views.logoutuser,name='logout'),
    path('account/',views.account_view,name='account'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('check/',views.check,name='check'),
    path('upload/', views.upload_file, name='upload_file'),
    path('update-dp/', views.update_dp, name='update_dp'),
    path('unauthorized/',views.unauthorized,name='unauthorized'),
    path('settings',views.settings,name="freelancer_settings"),
    path('explore/',views.explore,name='explore'),


]

