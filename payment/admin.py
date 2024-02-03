from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from payment.models import SessionTokens


# Register your models here.
class SessionTokensAdmin(ImportExportModelAdmin):
    list_filter = ['user']
    search_fields = ['user']
    list_display = ['user', 'token', 'active']
    pass
admin.site.register(SessionTokens, SessionTokensAdmin)