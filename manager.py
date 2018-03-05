"""
Manager For Whole Application
Author: Light Gao
Mailto: gaoliang@asiainfo.com
"""
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from apm import create_app, models
from apm.enums import globalenums
from os import environ

#Obtain env on host, if NOT exists then use 'dev'
env = environ.get('APM_ENV', 'dev')
#Generate app based on env('dev' or some other self-define value) via Factory Method
app = create_app('apm.config.%sConfig' % env.capitalize())
#Generate Manager object using app object
manager = Manager(app)
#Generate Migrate object using app & db object
migrate = Migrate(app, models.db)

#为manager增加指令，届时可直接以 server 作为sub-command
#即 python manager.py server/ python manager.py db ...
manager.add_command("server", Server(host='0.0.0.0', port=globalenums.DEFAULT_PORT))
manager.add_command("db", MigrateCommand)

@manager.shell
def make_shell_context():
    #Create a python CLI.
    # return: Default import object |type: `Dict`
    # 确保有导入 Flask app object，否则启动的 CLI Context 中仍然没有 app 对象
    return dict(app=app, db=models.db, User=models.User,
                Resource=models.Resource, Service=models.Service,
                SvcInstance=models.SvcInstance)

if __name__ == '__main__':
    manager.run(default_command='server')
