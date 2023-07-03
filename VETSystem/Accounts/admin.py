from django.contrib import admin
from .models import UserAdmin,Client,Report,AnalysisPrices
# Register your models here.


admin.site.register(UserAdmin)
admin.site.register(Client)
admin.site.register(Report)
admin.site.register(AnalysisPrices)
# admin.site.register(DynamicForm)
# admin.site.register(DynamicField)