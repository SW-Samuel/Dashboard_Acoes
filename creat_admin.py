from models import session, User
import bcrypt

password = '123456'
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
user = User(name='teste', password=hashed_password, email='t@t.com', admin=False)
session.add(user)
session.commit()