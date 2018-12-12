
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import get_app
from apps.forum.models import FrontUser
from externs import db
from apps.management import models as admin_models
from apps.communal import models as communal_models

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

@manager.option('-e','--email',dest='email')
def show_rights(email):
    adminer = Adminer.query.filter_by(email=email).first()
    if adminer:
        print('User rights is {}'.format(adminer.rights))
    else:
        print('The user {} is not exist'.format(email))

@manager.option('-e','--email',dest='email')
@manager.option('-r','--role',dest='role')
def add_role(email,role):
    adminer = Adminer.query.filter_by(email=email).first()
    if adminer:
        roles = Role.query.filter_by(name=role).first()
        if roles:
            roles.users.append(adminer)
            db.session.commit()
            print('Succeed to add role {} to user {}'.format(role,email))
        else:
            print('There is no this role {}'.format(role))
    else:
        print('The user {} is not exist'.format(email))


@manager.option('-t','--telephone',dest='telephone')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
def create_frontuser(telephone,username,password):
    user = FrontUser(telephone=telephone,username=username,password=password)
    db.session.add(user)
    db.session.commit()
    print('Create front user successfully!!!')


if __name__ == '__main__':
    manager.run()
