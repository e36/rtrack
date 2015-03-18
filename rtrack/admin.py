from django.contrib import admin
from rtrack.models import *


class ReportAdmin(admin.ModelAdmin):
    fields = ['title', 'description']
    readonly_fields = ('created', 'last_updated')
    list_display = ('title', 'created', 'last_updated')


class UserReportLinkAdmin(admin.ModelAdmin):
    fields = ['name', 'report']
    readonly_fields = ('timestamp',)
    list_display = ('name', 'report', 'timestamp')

# Register your models here.
admin.site.register(Username)
admin.site.register(Report, ReportAdmin)
admin.site.register(UserReportLink, UserReportLinkAdmin)
