# importa all models
from app.models import *
from app.views import retrieveImage, findLink
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

db.session.add(u1)
db.session.add(u2)
db.session.add(u3)

db.session.commit()

google = "www.google.com"
youtube = "www.youtube.com"
reddit = "www.reddit.com"
facebook = "www.facebook.com"

stuff = "I am a banana"
p1 = Post(body=findLink(google),timestamp=datetime.utcnow(),author=u1,img=retrieveImage(google))
p2 = Post(body=findLink(reddit),timestamp=datetime.utcnow(),author=u2,img=retrieveImage(reddit))
p3 = Post(body=findLink(facebook),timestamp=datetime.utcnow(),author=u2,img=retrieveImage(facebook))

# p2 = Post(body=youtube,timestamp=datetime.utcnow(),author=u1, img=retrieveImage(youtube))
# p3 = Post(body=stuff,timestamp=datetime.utcnow(),author=u1, img=retrieveImage(stuff))
db.session.add(p1)
# db.session.add(p2)
# db.session.add(p3)

# p1 = Post(body=google,timestamp=datetime.utcnow(),author=u2,img=retrieveImage(google))
# p2 = Post(body=youtube,timestamp=datetime.utcnow(),author=u2,img=retrieveImage(youtube))
# p3 = Post(body=stuff,timestamp=datetime.utcnow(),author=u2,img=retrieveImage(stuff))

# db.session.add(p1)
# db.session.add(p2)
# db.session.add(p3)

# p1 = Post(body=google,timestamp=datetime.utcnow(),author=u3,img=retrieveImage(google))
# p2 = Post(body=youtube,timestamp=datetime.utcnow(),author=u3,img=retrieveImage(youtube))
# p3 = Post(body=stuff,timestamp=datetime.utcnow(),author=u3,img=retrieveImage(stuff))
# db.session.add(p1)
# db.session.add(p2)
# db.session.add(p3)



g1 = Group(name="Medtronic",group_type=MAIN_GROUP)
g2 = Group(name="Corporate Finance")

# print g1
db.session.add(g1)
db.session.add(g2)

db.session.commit()


u1.join_group(g1)
u1.join_group(g2)

u2.join_group(g1)
u3.join_group(g1)

db.session.commit()

# print "member?" , u1.is_member(g1)
# print "member?" , u1.is_member(g2)
# print u1.groups.all()
# print Group.query.all()

# print sum([u.posts.all() for u in User.query.join(groups, (groups.c.user_id == User.id)).filter(groups.c.group_id == g1.id).all()],[])
# print User.query.join(groups, (groups.c.user_id == User.id)).filter(groups.c.group_id == g1.id).first().posts.all()

db.session.commit()

