import requests
from datetime import timedelta
from django.utils import timezone

from config.celery import app
from .models import Machine, Metric, Incident


def check_cpu_incident(machine: Machine, metric: Metric) -> None:
    cpu_threshold = 85.0

    active_incedent = Incident.objects.filter(
        machine=machine,
        type='cpu',
        resolved=False
    ).first()

    if metric.cpu > cpu_threshold:
        if not active_incedent:
            Incident.objects.create(
                type='cpu',
                machine=machine
            )
    elif active_incedent:
        active_incedent.close()

def check_mem_incident(machine: Machine) -> None:
    mem_threshold = 90.0
    duration_treshold = timedelta(minutes=30)
    start_time = timezone.now() - duration_treshold

    metrics = Metric.objects.filter(
        machine=machine,
        created_at__gte=start_time
    )

    if not metrics:
        return
    
    all_above_threshold = all(metric.memory > mem_threshold for metric in metrics)

    active_incident = Incident.objects.filter(
        machine=machine,
        type='mem',
        resolved=False
    ).first()

    if all_above_threshold:
        if not active_incident:
            Incident.objects.create(
                type='mem',
                machine=machine
            )
    elif active_incident:
        active_incident.close()

def check_disk_incident(machine: Machine) -> None:
    disk_threshold = 95.0
    duration_threshold = timedelta(hours=2)
    start_time = timezone.now() - duration_threshold

    metrics = Metric.objects.filter(
        machine=machine,
        created_at__gte=start_time
    )

    if not metrics:
        return
    
    all_above_threshold = all(metric.disk > disk_threshold for metric in metrics)

    active_incedent = Incident.objects.filter(
        machine=machine,
        type='disk',
        resolved=False
    ).first()

    if all_above_threshold:
        if not active_incedent:
            Incident.objects.create(
                type='disk',
                machine=machine
            )
    elif active_incedent:
        active_incedent.close()

@app.task
def fetch_machine_metric(machine_id: int) -> str:
    try:
        machine = Machine.objects.filter(id=machine_id).first()
        response = requests.get(machine.url)
        response.raise_for_status()

        data = response.json()

        cpu_value = float(data['cpu'])
        mem_value = float(data['mem'].strip('%'))
        disk_value = float(data['disk'].strip('%'))

        metric = Metric.objects.create(
            machine=machine,
            cpu=cpu_value,
            memory=mem_value,
            disk=disk_value,
            uptime=data['uptime'],
        )

        check_cpu_incident(machine, metric)

        return f"Success: {machine.name}"
    except Machine.DoesNotExist:
        return "Machine not found"
    except requests.RequestException as e:
        return f"Request error: {str(e)}"
    except (ValueError, KeyError) as e:
        return f"Parsing error: {str(e)}"
    
@app.task
def poll_machines() -> None:
    machines = Machine.objects.all()
    for machine in machines:
        fetch_machine_metric.delay(machine.id)

@app.task
def check_metrics() -> None:
    machines = Machine.objects.all()
    for machine in machines:
        check_mem_incident.delay(machine)
        check_disk_incident.delay(machine)



