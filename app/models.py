from app import db
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime


ROLE_USER = 0
ROLE_ADMIN = 1

groups = db.Table('groups',
	db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64))
	email = db.Column(db.String(120), index = True, unique = True)
	password = db.Column(db.String(15), unique = True)
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime)
	groups = db.relationship('Group', 
		 secondary = groups, 
		 # primaryjoin = (groups.c.user_id == id), 
		 # secondaryjoin = (followers.c.followed_id == id), 
		 backref = db.backref('users', lazy = 'dynamic'), 
		 lazy = 'dynamic')
	
	def join_group(self, group):
			if not self.is_member(group):
				self.groups.append(group)
				return self

	def leave_group(self, group):
		if self.is_member(user):
			self.followed.remove(group)
			return self

	def is_member(self, group):
		return self.groups.filter(groups.c.group_id == group.id).count() > 0

	def hash_password(self, password):
		self.password = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User name: %r email: %r password: %r>' % (self.name, self.email, self.password)    


class Group(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), unique = True)
	# user = db.relationship('User', 
	# 	 secondary = groups, 
	# 	 # primaryjoin = (groups.c.user_id == id), 
	# 	 # secondaryjoin = (groups.c.group_id == id), 
	# 	 backref = db.backref('groups', lazy = 'dynamic'), 
	# 	 lazy = 'dynamic')
	def members(self):
		return User.query.join(groups, (groups.c.user_id == User.id)).filter(groups.c.group_id == self.id).all()
	def posts(self):
		return sum([u.posts.all() for u in User.query.join(groups, (groups.c.user_id == User.id)).filter(groups.c.group_id == self.id).all()],[])
	def __repr__(self):
		return '<Group %r>' % (self.name)
	
class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	img = db.Column(db.String(300))

	def __repr__(self):
		return '<Post %r>' % (self.body)

		