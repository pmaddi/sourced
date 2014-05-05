from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from forms import LoginForm, RegistrationForm, EditForm, PostForm, GroupForm, JoinForm
from models import Post, User, ROLE_USER, ROLE_ADMIN, Group
import hashlib
from datetime import datetime
import urllib, cStringIO
from bs4 import BeautifulSoup
from config import WHOOSH_ENABLED


def getsize(url):
	try:
		file = urllib.urlopen(url)
		return len(file.read())
	except:
		return 0

def addhttp(link, domain):
	if link is None:
		return ''
	if link.startswith('http://') or link.startswith('https://'):
		return link
	else:
		return domain+link

def findLink(url):
	if not url.startswith('http://'):
		url = 'http://' + url
	try:	
		url = urllib.urlopen(url).geturl()
	except:
		return False
	return url

def retrieveImage(url):
	if not url.startswith('http://'):
		url = 'http://' + url
	try:	
		html = urllib.urlopen(url).read()
		url = urllib.urlopen(url).geturl()
	except:
		return ''
	domain = url
	soup = BeautifulSoup(html)
	imgs = soup.find_all('img')
	links = [addhttp(img.get('src'),domain) for img in imgs]
	sizes = [getsize(link) for link in links]
	max_value = max(sizes)
	max_index = sizes.index(max_value)
	return links[max_index]

def render_template_after_auth(tmpl_name, **kwargs):
	if g.user.is_authenticated():
		post_form = PostForm()
		new_group_form = GroupForm()
		groups = g.user.groups.all() 
		return render_template(tmpl_name, groups=groups, new_group_form=new_group_form, post_form=post_form, **kwargs)
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
		link = findLink(post_data)
		if link is not False:
			print link
			post = Post(body=link, timestamp=datetime.utcnow(), author = g.user, img = retrieveImage(post_data))
			db.session.add(post)
			db.session.commit()
			flash('Your post is now live!')
			return redirect(url_for('index'))
		flash(post_data+' is invalid')
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

@app.route('/register', methods=['GET', 'POST'])
def register():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = RegistrationForm()
	if request.method == 'POST' and form.validate():
		if User.query.filter(User.email == form.email.data).first() is not None:
			flash('Account exists for this email')
			return redirect(url_for('login'))
		user = User(name=form.name.data, email=form.email.data)
		user.hash_password(form.password.data)
		db.session.add(user)
		# session['remember_me'] = form.remember_me.data
		db.session.commit()
		user.join_group(Group.query.get(1))
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

@app.route('/group/<int:groupint>', methods = ['GET', 'POST'])
@login_required
def show_group_profile(groupint):
	group = Group.query.get_or_404(groupint)
	users = group.members()
	posts = group.posts()
	if request.method == 'POST':
		print "doing"
		g.user.join_group(group)
		db.session.commit()
		flash('Group joined')
		return redirect(url_for('show_group_profile', groupint=groupint ))
	return render_template_after_auth('group.html',
		# user = g.user,
		group = group,
		users = users,
		posts = posts,
		join_form = JoinForm())

@app.route('/groups', methods = ['GET','POST'])
@login_required
def show_all_groups():
	allgroups = Group.query.all()
	if request.method == 'POST':
		group_name = request.form.get('new_group')
		if Group.query.filter(Group.name == group_name).first() is not None:
			flash('Group exists')
			return redirect(url_for('show_group_profile', groupint = Group.query.filter(Group.name == group_name).first().id ))
		new_group = Group(name=group_name)
		db.session.add(new_group)
		db.session.commit()
		g.user.join_group(new_group)
		db.session.commit()
		flash('Group created')
		return redirect(url_for('show_group_profile', groupint=new_group.id))
	return render_template_after_auth('groups.html',
		# user = g.user,
		allgroups = allgroups)

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
		form = form,
		user = g.user)
