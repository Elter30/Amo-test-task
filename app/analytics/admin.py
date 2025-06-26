from django.contrib import admin
from .models import Machine, Metric, Incident

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')

@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ('machine', 'cpu', 'memory', 'disk', 'created_at')

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('machine', 'type', 'created_at', 'resolved_at')
    list_filter = ('type', 'machine')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'resolved_at')
    actions = ['close_incidents']
    
    def close_incidents(self, request, queryset):
        for incident in queryset:
            incident.close()
        self.message_user(request, f"{queryset.count()} инцидентов закрыто")
    close_incidents.short_description = "Закрыть выбранные инциденты"
