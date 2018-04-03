"""Plugin for Ansible
This plugin could return callable object which should have two main functions:
 .. 1. generate command based on input arguments;
 .. 2. execute command generated by 1);
To fulfill functionality above, 3rd plugin module must implement
functions below:
 .. 1. function:: get_executor(name, *args, **kwargs) --> return with callable object which include two functions above
 .. 2. function:: init_executor(name, *args, **kwargs) --> supply an entry point to initial executor after creative action
 .. 3. class:: AnsibleExecutor(name, *args, **kwargs) --> will be instantiated by get_executor function

Version 0.1: execute command[ansible-playbook] on remote host directly
Version 0.2: encapsulating ansible API
"""

import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import ansible.constants as C

from logging import getLogger
from uuid import uuid1

#initial logger
logger = getLogger('Celery')

#Function: create executor
def get_executor(name=None, *args, **kwargs):
    if name is None:
        name = uuid1()
    logger.info('Plugin -- The current executor is: [%s].' % name)
    return AnsibleExecutor(name, *args, **kwargs)

#class: AnsibleExecutor
class AnsibleExecutor:
    #essential properties

    # __init__
    def __init__(self, name, *args, **kwargs):
        # maybe defined by outer module or uuid1()
        self.__executor_name__ = name
        # could be redefined by other implements
        self.__api_version__ = 0.1
        # default is 'simple', could be extended by followers
        self._exec_mode = 'simple'
        self._executive = None
        # ansible module properties
        self._Options = namedtuple('Options',
                                   ['connection', 'module_path', 'forks',
                                    'become', 'become_method', 'become_user',
                                    'check', 'diff'])
        self._options = self._Options(connection='local', module_path=['/path/to/mymodules'],
                                      forks=1, become=None, become_method=None,
                                      become_user=None, check=False, diff=False)
        self._loader = DataLoader()
        self._inventory = InventoryManager(loader=self._loader, sources='localhost,')
        self._variable_manager = VariableManager(loader=self._loader, inventory=self._inventory)

        # generate executives
        self._gen_executive(*args, **kwargs)

    #initial executor after creative action
    def init_executor(self, *args, **kwargs):
        self._gen_executive(*args, **kwargs)

    # prepare play data
    def _gen_play(self):
        pass

    #function: generate executive(s)
    # .. param: args, type: dict
    def _gen_executive(self, *args, **kwargs):
        """Definition"""
        if args is None and kwargs is None:
            logger.error('No input parameter for Ansible plugin...')
            return False
        else:
            logger.info('Starting to generate executive(s)...')
            logger.info('Ansible deployment for zookeeper cluster, '
                         'nodes [{0}], port [{1}].'.format(kwargs['nodes'], kwargs['port']))
            self._executive = 'ansible-playbook site.yml ' \
                              '-e "zk_install_dir=/opt/testzk zk_client_port={0}"'.format(kwargs['port'])
            return True


    #function: execute -- to execute command(s) generated above
    def execute(self, exec_mode=None):
        """Definition of execute function
        called by outer module, i.e. task module..."""
        if exec_mode is None:
            exec_mode = self._exec_mode

        logger.debug('Starting to execute...')
        logger.info('Execute mode is [%s]...' % exec_mode)

        #execute
        logger.info('Plugin -- executive is [%s].' % self._executive)
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self._inventory,
                variable_manager=self._variable_manager,
                loader=self._loader,
                options=self._options,
                # passwords=passwords,
                # stdout_callback=results_callback,
                #  Use our custom callback instead of the ``default`` callback plugin
            )

            result = tqm.run(self._gen_play)
            logger.info(result)
        finally:
            if tqm is not None:
                tqm.cleanup()

        logger.info('Deployment finished!')
        return True



if __name__ == '__main__':
    get_executor()
