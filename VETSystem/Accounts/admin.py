from django.contrib import admin
from .models import UserAdmin,Client,Report
# Register your models here.


admin.site.register(UserAdmin)
admin.site.register(Client)
admin.site.register(Report)