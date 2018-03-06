"""Define asynchronous tasks"""
from celery import Celery
from apm.enums import globalenums
from time import sleep

#create celery instance
celery_task_queue = Celery('MiniCMDB', broker=globalenums.CELERY_BROKER_URL)

@celery_task_queue.task
def async_deploy_svc_inst(svc_type=None):
    if svc_type is None:
        return False
    print('Service type is %s, asynchronous task starting...' % svc_type)
    sleep(5)
    print('Asynchronous task finished!')

