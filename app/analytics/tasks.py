import requests

from config.celery import app
from .models import Machine, Metric

@app.task
def fetch_machine_metric(machine_id: int):
    try:
        machine = Machine.objects.filter(id=machine_id).first()
        response = requests.get(machine.url)
        response.raise_for_status()

        data = response.json()
        Metric.objects.create(
            machine=machine,
            cpu=data['cpu'],
            memory=data['mem'],
            disk=data['disk'],
            uptime=data['uptime'],
        )
        print("Запрос отправлен")
        return f"Success: {machine.name}"
    except Machine.DoesNotExist:
        return "Machine not found"
    except requests.RequestException as e:
        return f"Request error: {str(e)}"
    except (ValueError, KeyError) as e:
        return f"Parsing error: {str(e)}"
    
@app.task
def poll_machines():
    machines = Machine.objects.all()
    for machine in machines:
        fetch_machine_metric.delay(machine.id)

