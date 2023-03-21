from dataclasses import dataclass

from app import db


@dataclass
class UserSalt(db.Model):
	__tablename__ = 'USER_SALT'
	user_id: int
	salt: str

	user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'), primary_key=True, index=True)
	salt = db.Column(db.Text(150))

	@staticmethod
	def search_by_id(id):
		return UserSalt.query.filter_by(user_id=id).first()
