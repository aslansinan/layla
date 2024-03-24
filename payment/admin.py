from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from payment.models import SessionTokens, CallbackHashTokens


# Register your models here.
class SessionTokensAdmin(ImportExportModelAdmin):
    list_filter = ['user']
    search_fields = ['user']
    list_display = ['user', 'token', 'active']
    pass
admin.site.register(SessionTokens, SessionTokensAdmin)

class CallbackHashTokensAdmin(ImportExportModelAdmin):
    list_filter = ['total_amount']
    search_fields = ['total_amount']
    list_display = ['total_amount', 'status']
    pass
admin.site.register(CallbackHashTokens, CallbackHashTokensAdmin)