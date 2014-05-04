from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from forms import LoginForm, RegistrationForm, EditForm, PostForm
from models import Post, User, ROLE_USER, ROLE_ADMIN
import hashlib
from datetime import datetime


def render_template_after_auth(tmpl_name, **kwargs):
	if g.user.is_authenticated():
		post_form = PostForm()
		return render_template(tmpl_name, post_form=post_form, **kwargs)
	return render_template(tmpl_name, **kwargs)

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated():
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()


@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
@login_required
def index():
	user = g.user
	posts = g.user.posts.all()
	if request.method == 'POST':
		post_data = request.form.get('post')
		post = Post(body=post_data, timestamp=datetime.utcnow(), author = g.user)
		db.session.add(post)
		db.session.commit()
		flash('Your post is now live!')
		return redirect(url_for('index'))
	return render_template_after_auth('index.html',
		title = 'Home',
		user = user,
		posts = posts)

@app.route('/login', methods = ['GET', 'POST'])
# @oid.loginhandler
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		# session['remember_me'] = form.remember_me.data
		email=form.email.data
		password=form.password.data
		user = User.query.filter(User.email == email).first()
		if user is None:
			flash('Invalid email')
			return render_template('login.html', title = 'Sign In',form = form)
		if user.verify_password(password) is False:
			flash('Invalid password')
			return render_template('login.html', title = 'Sign In', form = form)
		login_user(user)
		return redirect(url_for('index'))
	return render_template('login.html', 
		title = 'Sign In',
		form = form)

# @user.route('/login', methods=['GET', 'POST'])
# def login():
#     if g.user is not None and g.user.is_authenticated():
#         return redirect(url_for('splash.dashboard'))
#     if request.method == 'GET':
#         email = request.args.get('defaultEmail')
#         return render_template('login.html', defaultEmail=email)
#     email = request.form['email'].lower()
#     password = request.form['password']
#     user = User.query.filter(User.email == email).first()
#     if user is None:
#         flash('Email is invalid!')
#         return redirect(url_for('user.login'))
#     if user.verify_password(password) is False:
#         flash('Password is invalid!')
#         return redirect(url_for('user.login'))
#     if (user.account_approved is False) and (user.company is not None):
#         return redirect(url_for('user.unvalidated'))
#     login_user(user)
#     return redirect(url_for('splash.dashboard'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = RegistrationForm()
	if request.method == 'POST' and form.validate():
		user = User(name=form.name.data, email=form.email.data)
		user.hash_password(form.password.data)
		db.session.add(user)
		# session['remember_me'] = form.remember_me.data
		db.session.commit()
		flash('Thanks for registering')
		return redirect(url_for('login'))
	return render_template('register.html', form=form)



@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/user/<int:userint>')
@login_required
def show_user_profile(userint):
	user = User.query.get_or_404(userint)
	posts = user.posts.all()
	return render_template_after_auth('user.html',
		user = user,
		posts = posts)

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
	form = EditForm()
	if form.validate_on_submit():
		g.user.name = form.name.data
		g.user.about_me = form.about_me.data
		db.session.add(g.user)
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit'))
	else:
		form.name.data = g.user.name
		form.about_me.data = g.user.about_me
	return render_template_after_auth('edit.html',
		form = form)
