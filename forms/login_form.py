from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    user_id = StringField("工号",validators=[DataRequired()])
    password = PasswordField("密码",validators=[DataRequired()])
    submit = SubmitField("登录")