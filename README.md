# Description
I tried to find some popular open source CMDB system, I succeed. <br/>
And then I tired to pick up one which should be easy to handle, I failed.</br>
I am not sure why, and I do not want to figure it out. Since I decide to make one all by myself.

# Using components
1. Flask
2. SQLAlchemy
3. Extensions: flask-sqlalchemy/flask-wtf/flask-migrate/flask-bcrypt...
You may find these extensions in `requirements.txt` file.

## How to start
1. Clone this project;
2. Install python3(at least python3.5.2) on your host;
3. Install all dependencies in requirements.txt: `pip install requirements.txt`;
4. Make sure you have Mysql installed on your host, and database(configured in config.py) exists ;
5. Prepare database: changing directory into project of AICMDB,
execute `python manager.py db init` to initial migration repository,
then `python manager.py db migrate` to identify differences between database and its definition in code(models.py),
at last `python manager.py db upgrade` to make synchronization;
6. After preparation above, you may start this web application by `python manager.py [server]`,
browser it through `http://ip:6688`(which configured in enums/globalenums.py);

## License
GPL license,<br/>
which means you must keep it as open source project no matter what and keep the same license in your project.
