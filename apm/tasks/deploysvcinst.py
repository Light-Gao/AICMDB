"""Define asynchronous tasks"""
from celery import Celery
from celery.utils.log import get_task_logger
from apm.enums import globalenums
from apm.plugins import ansible


#initail celery instance
celery_task_queue = Celery('Celery', broker=globalenums.CELERY_BROKER_URL)
logger = get_task_logger('Celery')

#Publishing asynchronous task,
# encapsulating all kinds plugins(service deployment only) in apm.plugins directory
# arranging data flow for sub-task(s) if needed...
@celery_task_queue.task
def async_deploy_svc_inst(svc_type=None, nodes=None, port=None):
    if svc_type is None or nodes is None or port is None:
        logger.error('No service type input, please check...')
        return False
    else:
        logger.info('Service type is %s, asynchronous task starting...' % svc_type)
        logger.info('Service deployment: node number --> %s...' % nodes)
        logger.info('Service deployment: port number --> %s...' % port)
        cmd = gen_executive_cmd(svc_type=svc_type, nodes=nodes, port=port)
        logger.info('The executive is: %s' % cmd)
        logger.info('Asynchronous task published!')

#create executives
def gen_executive_cmd(*args, **kwargs):
    if args is None and kwargs is None:
        logger.error('No service type input, please check...')
        return 'Error, no service type input, nothing to do...'
    elif kwargs['svc_type'] == 'Ansible':
        logger.info('Service type is %s...' % kwargs['svc_type'])
        executive = ansible.gen_executive(*args, **kwargs)
        if executive:
            ansible.execute(executive)
        return executive
