from django.db import models

class Machine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(help_text="URL для сбора информации")

    def __str__(self):
        return self.name
    
class Metric(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    cpu = models.IntegerField(help_text="Загрузка CPU")
    memory = models.CharField(max_length=10, help_text="Использование память")
    disk = models.CharField(max_length=10, help_text="Использование диска")
    uptime = models.CharField(max_length=20, help_text="Время работы")
    created_at = models.DateTimeField(auto_now_add=True)
