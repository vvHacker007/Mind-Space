from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField, BooleanField, IntegerField, DateField, TextAreaField, ValidationError
from wtforms.validators import Length, Email, DataRequired, EqualTo
from datetime import date

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    phone = IntegerField('Phone No.',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password',validators=[DataRequired()])
    birthdate = DateField('Birth Date')
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Username/Email',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(),Length(min=5,max=100)])
    content = TextAreaField('Content', validators=[DataRequired(),Length(min=300)])
    submit = SubmitField('Post')
    save = SubmitField('Save')

def length_check(form,field):
    if len(field.data) != 6 or field.data.isdigit()==False:
        raise ValidationError('Field must contain only 6 digits')

class OTPForm(FlaskForm):
    otp = StringField('Enter OTP', validators=[DataRequired(),length_check])
    submit = SubmitField('Verify')
