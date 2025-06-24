from django.contrib import admin
from .models import Machine, Metric

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')

@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ('machine', 'cpu', 'memory', 'disk', 'created_at')
