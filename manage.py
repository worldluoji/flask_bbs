
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import get_app
from externs import db
from apps.management import models as admin_models
from flask_wtf import CSRFProtect

app = get_app()
CSRFProtect(app)

# link manager and app
manager = Manager(app)

#link app and db
Migrate(app,db)

#add command to manager
manager.add_command('db', MigrateCommand)

Adminer = admin_models.Administrator


#python3 manage.py create_manager -u 'luoji' -p '199114' -e '1132416@qq.com'
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_manager(username,password,email):
    user = Adminer(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print('Add an administrator successfully!!!')

if __name__ == '__main__':
    manager.run()
