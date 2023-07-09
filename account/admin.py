from django.contrib import admin
from account.models import Account, Freelancer, Client,Order,UpcomingOrder,Portfolio
# from django.contrib.auth.admin import UserAdmin


# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'name',  'last_login')
    search_fields = ('email',  'name', 'id')
    readonly_fields = ()
    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ()


class FreelancerAdmin(admin.ModelAdmin):
    list_display = ('freelancer', 'email')
    search_fields = ('freelancer', 'email')
    readonly_fields = ()
    ordering = ()
    filter_horizontal = ()
    list_filter = ()


admin.site.register(Account, AccountAdmin)
admin.site.register(Freelancer, FreelancerAdmin)
admin.site.register(Client)
admin.site.register(Order)
admin.site.register(UpcomingOrder)
admin.site.register(Portfolio)

# admin.site.register(Account)
# admin.site.register(VendorAccount)
