from django.contrib import admin
from .models import MomoData, Transaction, Missed, Report


class MomoDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'momo_name', 'momo_number', 'updated', 'timestamp', )

class TransAdmin(admin.ModelAdmin):
    list_display = ('user', 'to', 'amount', 'state', 'timestamp', )

class MissedAdmin(admin.ModelAdmin):
    list_display = ('user', 'was_to', 'missed_to', 'amount', 'trans_id', 'timestamp', )

class ReportAdmin(admin.ModelAdmin):
    list_display = ('by', 'against', 'trans_id', 'timestamp', )

admin.site.register(MomoData, MomoDataAdmin)
admin.site.register(Transaction, TransAdmin)
admin.site.register(Missed, MissedAdmin)
admin.site.register(Report, ReportAdmin)
# Register your models here.
