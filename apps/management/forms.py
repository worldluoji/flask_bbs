
from flask_wtf import FlaskForm
from wtforms.validators import  Email,Length,InputRequired,EqualTo
from wtforms import StringField,PasswordField,SubmitField,IntegerField,Form,ValidationError
from utils import memcache_operate
from flask import g

class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(message='Please input email'),Email(message='Please input right format of email')])
    password = StringField(validators=[Length(6,20,message='Please input password with length 6-20')])
    remember = IntegerField()


class Resetpwdform(Form):
    oldpwd = StringField(validators=[Length(6, 20, message='Please input password with length 6-20')])
    newpwd = StringField(validators=[Length(6, 20, message='Please input password with length 6-20')])
    newpwd2 = StringField(validators=[Length(6, 20, message='Please input password with length 6-20'),EqualTo('newpwd')])

    def get_error(self):
        msg = self.errors.popitem()[1][0]
        return msg


class ResetEmailForm(Form):
    email = StringField(validators=[Email(message="Please input Email with right format!!!")])
    captcha = StringField(validators=[Length(6,6,message="Please input right CAPTCHA!!!")])

    def validate_email(self, field):
        email = field.data
        #print(email)
        adminer = g.administrator
        if email == adminer.email:
            raise ValidationError("New Email can not be the same with old!!!")
        return True

    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        cached_captcha = memcache_operate.get(email)

        if not (cached_captcha and cached_captcha.lower() == captcha.lower()):
            raise ValidationError("Email Captcha Error!!!")
        return True

    def get_error(self):
        msg = self.errors.popitem()[1][0]
        return msg


class AddBannerForm(Form):
    name = StringField(validators=[InputRequired(message="Please Input banner image name")])
    image_url = StringField(validators=[InputRequired(message='Please Input banner image url')])
    link_url = StringField(validators=[InputRequired(message='Please Input link url')])
    priority = IntegerField(validators=[InputRequired(message='Please Input the priority of the banner image')])

    def get_error(self):
        msg = self.errors.popitem()[1][0]
        return msg

class EditBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message="Please input banner id")])

