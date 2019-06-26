from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from mongoengine.queryset.visitor import Q

class LoginForm(FlaskForm):
	username=StringField('Username', validators=[DataRequired()])
	password=StringField('Password', validators=[DataRequired()])
	remember_me=BooleanField('Remember me')
	submit=SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username=StringField('Username', validators=[DataRequired()])
	email=StringField('Email', validators=[Email(), DataRequired()])
	password=StringField('Password', validators=[DataRequired()])
	password2=StringField('Confirm Password', validators=[EqualTo('password'), DataRequired()])
	submit=SubmitField('Register')

	def validate_username(self, username):
		user=User.objects(username=username).first()
		if user is not None:
			raise ValidationError('Please use a different username')

	def validate_email(self, email):
		user=User.objects(email=email).first()
		if user is not None:
			raise ValidationError('Please use a different email address')

class EditProfileForm(FlaskForm):
	username=StringField('Username', validators=[DataRequired()])
	email=StringField('Email', validators=[Email(), DataRequired()])
	about_me=TextAreaField('About Me', validators=[Length(min=1, max=140)])
	submit=SubmitField('submit')

	def __init__(self, original_username, original_email, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username=original_username
		self.original_email=original_email

	def validate_username_email(self, username, email):
		if username!=self.original_username or email!=self.original_email:
			user=User.objects(Q(username=self.username.data) | Q(email=self.email.data)).first()
			if user is not None:
				return False

	def PasswordResetRequestForm(FlaskForm):
		email=StringField('Email', validators=[Email(), DataRequired()])
		submit=SubmitField('submit')

	def ResetPasswordForm(FlaskForm):
		new_password=StringField('New Password', validators=[DataRequired()])
		confirm_new_password=StringField('Confirm New Password', 
			validators=[DataRequired(), EqualTo('new_password')])
		submit=SubmitField('Request Password Reset')

