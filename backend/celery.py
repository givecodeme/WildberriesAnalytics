import os
import django
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.dev')
django.setup()
app = Celery('backend')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    # "update_stock": {
    #     "task": "backend.tasks.update_stock",
    #     # "schedule": crontab(hour="*/3", minute='30'),
    # "schedule": 30.0,
    # },
    # "update_sales": {
    #     "task": "backend.tasks.update_sales",
    #     # "schedule": crontab(minute="*/30"),
    #     "schedule": crontab(hour="*/3"),
    #     # "schedule": 30.0,
    # },
    "update_orders": {
        "task": "backend.tasks.update_orders",
        # "schedule": crontab(minute="*/30"),
        # "schedule": crontab(hour="*/3"),
        "schedule": 30.0,
    },
    # "update_comissions": {
    #     "task": "backend.tasks.update_comissions",
    #     "schedule": crontab(hour="*/3"),
    #     # "schedule": 30.0,
    # },
}


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     # sender.add_periodic_task(
#     #     10.0, update_sales.s(), name='add every 10')

#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(1.0, test.s('tes'))

#     # Executes every Monday morning at 7:30 a.m.

#     # sender.add_periodic_task(
#     #     crontab(hour=7, minute=30, day_of_week=1),
#     #     test.s('Happy Mondays!'),
#     # )
