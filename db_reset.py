# importa all models
from app.models import User, Post
from app.views import retrieveImage
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
stuff = "I am a banana"
p1 = Post(body=google,timestamp=datetime.utcnow(),author=u1,img=retrieveImage(google))
p2 = Post(body=youtube,timestamp=datetime.utcnow(),author=u1, img=retrieveImage(youtube))
p3 = Post(body=stuff,timestamp=datetime.utcnow(),author=u1, img=retrieveImage(stuff))
db.session.add(p1)
db.session.add(p2)
db.session.add(p3)

p1 = Post(body=google,timestamp=datetime.utcnow(),author=u2,img=retrieveImage(google))
p2 = Post(body=youtube,timestamp=datetime.utcnow(),author=u2,img=retrieveImage(youtube))
p3 = Post(body=stuff,timestamp=datetime.utcnow(),author=u2,img=retrieveImage(stuff))

db.session.add(p1)
db.session.add(p2)
db.session.add(p3)

p1 = Post(body=google,timestamp=datetime.utcnow(),author=u3,img=retrieveImage(google))
p2 = Post(body=youtube,timestamp=datetime.utcnow(),author=u3,img=retrieveImage(youtube))
p3 = Post(body=stuff,timestamp=datetime.utcnow(),author=u3,img=retrieveImage(stuff))
db.session.add(p1)
db.session.add(p2)
db.session.add(p3)

db.session.commit()

