from django.contrib import admin
from .models import AvailableProjects,Application

# Register your models here.
admin.site.register(AvailableProjects)
admin.site.register(Application)