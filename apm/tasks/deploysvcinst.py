"""Define asynchronous tasks"""
from celery import Celery
from celery.utils.log import get_task_logger
from apm.enums import globalenums
from apm.plugins import ansible

#create celery instance
celery_task_queue = Celery('MiniCMDB', broker=globalenums.CELERY_BROKER_URL)
logger = get_task_logger(__name__)

@celery_task_queue.task
def async_deploy_svc_inst(svc_type=None, nodes=None, port=None):
    if svc_type is None or nodes is None or port is None:
        return False

    logger.info('Service type is %s, asynchronous task starting...' % svc_type)
    logger.info('Service deployment: node number --> %s...' % nodes)
    logger.info('Service deployment: port number --> %s...' % port)
    cmd = gen_executive_cmd(svc_type=svc_type)
    logger.info('The command is: %s' % cmd)
    logger.info('Asynchronous task finished!')

def gen_executive_cmd(svc_type):
    if svc_type is None:
        return 'No service type input, nothing to do...'
    elif svc_type == 'Ansible':
        ansible.gen_executive()
        ansible.execute()
