from django.db import models
from django.utils import timezone

class Machine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(help_text="URL для сбора информации")

    def __str__(self):
        return self.name
    
class Metric(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    cpu = models.FloatField(help_text="Загрузка CPU")
    memory = models.FloatField(help_text="Использование память")
    disk = models.FloatField(help_text="Использование диска")
    uptime = models.CharField(max_length=20, help_text="Время работы")
    created_at = models.DateTimeField(auto_now_add=True)

class Incident(models.Model):
    class IncidenType(models.TextChoices):
        CPU = "cpu"
        MEMORY = "mem"
        DISK = "disk"
    
    type = models.CharField(max_length=10, choices=IncidenType.choices)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def close(self):
        self.resolved = True
        self.resolved_at = timezone.now()
        self.save()

