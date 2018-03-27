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
def async_deploy_svc_inst(svc_type=None, *args, **kwargs):
    #service type is the only and essential precondition/parameter
    if svc_type is None:
        logger.error('No service type input, please check...')
        return False
    elif svc_type == 'Ansible':
        #log service type info
        logger.info('Service type is [%s], asynchronous task starting...' % svc_type)
        #get an executor | name attribute may re-defined by other ways
        cur_executor = ansible.get_executor(name='AnsibleExecutor', *args, **kwargs)
        #initial executor above or initial it like below...
        #cur_executor.init_executor(svc_type, *args, **kwargs)

        # log executor info
        logger.info('Task -- The current executor is: [%s].' % cur_executor.__executor_name__)
        logger.info('The current executor version is [%s].' % cur_executor.__api_version__)

        #execute current executor, so Plugins must have such a function named execute(exec_mode)
        cur_executor.execute(exec_mode='simple')

        logger.info('Asynchronous task finished!')

        return True
    else:
        return False
