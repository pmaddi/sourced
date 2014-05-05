# importa all models
from app.models import User, Post
from app import db
from datetime import datetime

# recreate the database
db.drop_all()
db.create_all()



u1 = User(name="Christian", email="christian@laurence.com")
u2 = User(name="Hun", email="hun@wong.com")
u3 = User(name="Pranav", email="pranav@maddi.com")

u1.hash_password("user1")
u2.hash_password("user2")
u3.hash_password("user3")

# u1.registered_on=datetime.utcnow()
# u2.registered_on=datetime.utcnow()
# u3.registered_on=datetime.utcnow()

db.session.add(u1)
db.session.add(u2)
db.session.add(u3)

db.session.commit()


p1 = Post(body="First post",timestamp=datetime.utcnow(),author=u1)
p2 = Post(body="Second post",timestamp=datetime.utcnow(),author=u1)
p3 = Post(body="I am Christian.",timestamp=datetime.utcnow(),author=u1)
db.session.add(p1)
db.session.add(p2)
db.session.add(p3)


p1 = Post(body="First post",timestamp=datetime.utcnow(),author=u2)
p2 = Post(body="Second post",timestamp=datetime.utcnow(),author=u2)
p3 = Post(body="I am Hun.",timestamp=datetime.utcnow(),author=u2)
db.session.add(p1)
db.session.add(p2)
db.session.add(p3)

p1 = Post(body="First post",timestamp=datetime.utcnow(),author=u3)
p2 = Post(body="Second post",timestamp=datetime.utcnow(),author=u3)
p3 = Post(body="I am Pranav.",timestamp=datetime.utcnow(),author=u3)
db.session.add(p1)
db.session.add(p2)
db.session.add(p3)

db.session.commit()

