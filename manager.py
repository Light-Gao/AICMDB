"""
Manager For Whole Application
Author: Light Gao
Mailto: gaoliang@asiainfo.com
"""
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from apm.enums import globalenums
from apm.tasks.deploysvcinst import celery_task_queue
from apm import create_app, models
from os import environ

#Obtain env on host, if NOT exists then use 'dev'
env = environ.get('APM_ENV', 'dev')
#Generate app based on env('dev' or some other self-define value) via Factory Method
app = create_app('apm.config.%sConfig' % env.capitalize())
#app logger format

#log app creation
app.logger.debug('application has been created...')
#Generate Manager object using app object
manager = Manager(app)
#Generate Migrate object using app & db object
migrate = Migrate(app, models.db)
#Update config for celery instance
celery_task_queue.conf.update(app.config)

#add executive for manager, then you may take 'server' as sub-command
#namely, python manager.py server/ python manager.py db/ etc.
manager.add_command("server", Server(host='0.0.0.0', port=globalenums.DEFAULT_PORT))
manager.add_command("db", MigrateCommand)

@manager.shell
def make_shell_context():
    #Create a python CLI.
    # return: Default import object |type: `Dict`
    # make sure Flask app object has been imported,
    # otherwise CLI Context has no app object, which will lead to error...
    return dict(app=app, db=models.db, User=models.User,
                Resource=models.Resource, Service=models.Service,
                SvcInstance=models.SvcInstance, Attribute=models.Attribute)

#execute on localhost IDE, lazy me...
if __name__ == '__main__':
    manager.run(default_command='server')
