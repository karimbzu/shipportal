from django.contrib import admin

from Lollipop_CRM.models import Customer, Sender, Package, UserPermission, Profile, ReturnLabel

admin.site.site_header = "Lollipop Administration"
admin.site.register(Customer)
admin.site.register(Sender)
admin.site.register(Package)
admin.site.register(UserPermission)
admin.site.register(Profile)
admin.site.register(ReturnLabel)


