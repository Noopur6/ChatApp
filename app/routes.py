from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from app import app, mongo
from app.models import User
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PasswordResetRequestForm, ResetPasswordForm
from flask_login import login_required
from werkzeug.urls import url_parse
from datetime import datetime
from app.email import send_password_reset_email

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
@login_required
def index():
    return render_template('index.html', title='Home', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
	if current_user.is_authenticated():
		return redirect(url_for('index'))
	form=LoginForm()
	if form.validate_on_submit():
		user=User.objects.(username=form.username.data).first()
		if user is None or not user.verify_password(form.password.data):
			flash('Invalid username or password')
		login_user(user, remember=form.remember_me.data)
		next_page=request.args.get('next')
		if not next_page or url_parse(next_page).netloc!='':
			next_page=url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form=RegistrationForm()
	if form.validate_on_submit():
		user=User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		user.save()
		flash('You have been successfully registered!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
	form=EditProfileForm(current_user.username, current_user.email)
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	if form.validate_on_submit() or form.validate_email_username(form.username.data, form.email.data):
		current_user.username=form.username.data
		current_user.email=form.email.data
		current_user.about_me=form.about_me.data
		current_user.save(username=form.username.data)
		flash('your changes have been saved')
		return redirect(url_for('edit_profile'))
	elif request.method=='GET':
		form.username.data=current_user.username
		form.email.data=current_user.email
		form.about_me.data=current_user.about_me
	return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/reset_password_request', methods=['GET','POST'])
@login_required
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form=PasswordResetRequestForm()
	if form.validate_on_submit():
		user=User.objects(email=form.email.data).first()
		if user:
			send_password_reset_email(user)
			flash('Check your email for reset instructions')
			return redirect(url_for('login'))
		else:
			flash('Enter email you used to sign up')
	return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>/', methods=['GET','POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user=User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('index'))
	form=ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.new_password.data)
		user.save()
		return redirect(url_for('login'))
	return render_template('reset_password.html',title='Reset Password',form=form)

@app.route('/delete/<username>/')
@login_required
def delete_profile(username):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	if user.objects(username=username).delete() is None:
		flash("User by {username} doesn't exist!".format(username))
	else:
		flash('Profile successfully deleted')
	return render_template('login.html')

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))
