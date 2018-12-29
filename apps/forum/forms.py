
from wtforms.validators import Length,EqualTo,Regexp
from wtforms import StringField, ValidationError, IntegerField
from flask_wtf import FlaskForm
from utils import memcache_operate
from wtforms.validators import InputRequired


class SignupForm(FlaskForm):
    telephone = StringField(validators=[Regexp(regex=r'^1[3-9]\d{9}',message="Please input right telephone number")])
    sms_captcha = StringField(validators=[Regexp(regex=r'[0-9A-Za-z]{4}',message="Please input right SMS captcha")])
    username = StringField(validators=[Length(min=6,max=20,message="Username length between 6 and 20")])
    password = StringField(validators=[Length(6, 20, message='Please input password with length 6-20')])
    password_repeat = StringField(validators=[EqualTo("password",message='Two passwords must be the same')])
    graph_captcha = StringField(validators=[Regexp(r'[0-9A-Za-z]{4}',message='Please input right graph captcha')])

    '''
    def validate_sms_captcha(self,field):
        #TODO
        pass
    '''

    def vlidate_graph_captcha(self,field):
        captcha = field.data
        captcha_mem = memcache_operate.get(captcha.lower())
        print('mem captcha is {}, user input captcha is {}'.format(captcha_mem,captcha))
        if not captcha_mem:
            return ValidationError('Graph captcha error')

    def get_error(self):
        msg = self.errors.popitem()[1][0]
        return msg


class SignInForm(FlaskForm):

    telephone = StringField(validators=[Regexp(regex=r'^1[3-9]\d{9}',message="Please input right telephone number")])
    password = StringField(validators=[Length(6, 20, message='Please input password with length 6-20')])
    remember = StringField()

    def get_error(self):
        msg = self.errors.popitem()[1][0]
        return msg

class PubPostForm(FlaskForm):
    title = StringField(validators=[InputRequired(message='Please input title')])
    content = StringField(validators=[InputRequired(message='Please input content')])
    board_id = IntegerField(validators=[InputRequired(message='Please input board_id')])

    def get_error(self):
        msg = self.errors.popitem()[1][0]
        return msg