from app import db, login, app
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt

class User(UserMixin, db.Document):
	id=db.IntField(primaryKey=True)
	username=db.StringField(max_length=64, index=True, unique=True)
	email=db.EmailField(max_field=120, index=True, unique=True)
	password_hash=db.StringField(max_length=128)
	about_me=db.StringField(max_length=140)

	def set_password(self, password):
		self.password_hash=generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def avatar(self, size):
		digest=md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode({'reset_password':self.id, 'exp':	time()+expires_in},
			app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id=jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
		except:
			return
		return User.objects(_id=id).first()

	@login.user_loader
	def load_user(id):
		return User.objects(_id=id).first()