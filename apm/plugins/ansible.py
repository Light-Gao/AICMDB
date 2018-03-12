"""Plugin for Ansible
This plugin defines two main functions:
 .. 1. generate command based on input args;
 .. 2. execute command generated by 1);
To fulfill functionality above, 3rd plugin module must implement
functions below:
 .. 1. gen_executive(*args, **kwargs);
 .. 2. execute(*args, **kwargs);

Version 0.1: execute command on remote host directly
Version 0.2: encapsulating ansible API
"""



from paramiko import SSHClient, AutoAddPolicy
from time import sleep
from logging import getLogger

#initial logger
logger = getLogger('Celery')

#Function: generate executive(s)
# .. param: args, type: dict
def gen_executive(*args, **kwargs):
    """Definition"""
    if args is None and kwargs is None:
        return False
    else:
        logger.info('Starting to generate executive(s)...')
        logger.info('Ansible deployment for zookeeper cluster, '
                     'nodes [{0}], port [{1}].'.format(kwargs['nodes'], kwargs['port']))
        return 'ansible-playbook -i [hosts] zookeeper.yml ' \
               '-e "nodes={0} port={1}"'.format(kwargs['nodes'], kwargs['port'])


#Function: execute -- to execute command(s) generated above
def execute(executive):
    """Definition"""
    logger.info('Starting to execute [%s]...' % executive)
    sleep(5)
    logger.info('Deployment finished!')
    return True



if __name__ == '__main__':
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(hostname='10.10.100.131', port=22, username='root', password='admin@123')
    stdin, stdout, stderr = ssh.exec_command('ls')
    out = stdout.read()
    print(out.decode())

