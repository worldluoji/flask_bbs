
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import get_app
from externs import db
from apps.management import models as admin_models

app = get_app()

# link manager and app
manager = Manager(app)

#link app and db
Migrate(app,db)

#add command to manager
manager.add_command('db', MigrateCommand)

Adminer = admin_models.Administrator
Role = admin_models.Role

#python3 manage.py create_manager -u 'luoji' -p '199114' -e '1132416@qq.com'
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_manager(username,password,email):
    user = Adminer(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print('Add an administrator successfully!!!')

#python3 manage.py crate_role
@manager.command
def create_role():
    visitor = Role(name="visitor",desc="can only visit")
    visitor.rights = admin_models.UserRights.VISITOR

    operator = Role(name="operator",desc="can manage comment, article or frontuser")
    operator.rights = (admin_models.UserRights.VISITOR | admin_models.UserRights.COMMENTER | admin_models.UserRights.POSTER | admin_models.UserRights.FRONTUSER)

    adminer = Role(name="adminer",desc="having all rights")
    adminer.rights = (admin_models.UserRights.VISITOR | admin_models.UserRights.COMMENTER | admin_models.UserRights.POSTER | admin_models.UserRights.FRONTUSER
                      | admin_models.UserRights.BOARDEF | admin_models.UserRights.ADMINER)

    developer = Role(name="developer", desc="having all rights")
    developer.rights = admin_models.UserRights.DEVELOPER

    db.session.add_all([visitor,operator,adminer,developer])
    db.session.commit()

if __name__ == '__main__':
    manager.run()
