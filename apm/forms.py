"""Forms Definition For Pages
Author  Light Gao
Mailto  gaoliang@asiainfo.com
Date    20180112
Last Modified 20180228
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms import validators
from apm.models import User

#Form for add svc instance
class SvcInstanceForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired(),
                                validators.Length(max=255)])
    remark = TextAreaField('Remark', [validators.Length(max=255)])

#Form for add Login page
class LoginForm(FlaskForm):
    user_name = StringField('Username', [validators.DataRequired(),
                                         validators.Length(max=64)])
    user_passwd = PasswordField('Password', [validators.DataRequired(),
                                             validators.Length(min=6)])

    #reload validate() function from parent class FlaskForm
    def validate(self):
        check_validate = super(LoginForm, self).validate()
        #return false directly if super validate() not pass
        if not check_validate:
            print("Did not pass Validator in Flaskform!")
            return False
        #check user whether exists or not
        user = User.query.filter_by(apm_user_name=self.user_name.data).first()
        if not user:
            self.user_name.errors.append("Username does not exists!")
            return False
        #check if password is right
        if not user.check_passwd(self.user_passwd.data):
            self.user_passwd.errors.append("Password does not match!")
            return False
        return True

#Form for register new user
class RegisterForm(FlaskForm):
    user_name = StringField('Username', [validators.DataRequired(),
                                         validators.Length(max=64)])
    user_passwd = PasswordField('Password', [validators.DataRequired,
                                             validators.Length(min=6)])
    confirm_passwd = PasswordField('Confirm Password', [validators.DataRequired(),
                                                        validators.EqualTo('user_passwd')])

    #reload validate() function from parent class FlaskForm
    def validate(self):
        check_validate = super(RegisterForm, self).validate()
        #return false directly if super validate() not pass
        if not check_validate:
            return False
        #check if user name has been registered by others before
        user = User.query.filter_by(apm_user_name=self.user_name.data).first()
        if user:
            self.user_name.errors.append("User name already exits!")
            return False
        return True
