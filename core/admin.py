from django.contrib import admin

# Register your models here.
from core.models import IdMapping, Report, Login

admin.site.register(IdMapping)
admin.site.register(Report)
admin.site.register(Login)
