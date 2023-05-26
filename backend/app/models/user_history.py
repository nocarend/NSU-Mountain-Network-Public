from dataclasses import dataclass
from datetime import datetime

from app import db, timezone

"""
что происходит с деньгами
"""


@dataclass
class UsersHistory(db.Model):
	__tablename__ = 'MONEY_HISTORY'
	history_id: int
	user_id: int
	auser_id: int
	action_id:int
	old_value: int
	new_value: int
	history_datetime: datetime

	history_id = db.Column(db.Integer, primary_key=True, unique=True,
	                       autoincrement=True, index=True)
	user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'), index=True)
	auser_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'),
	                     index=True)
	action_id=db.Column (db.Integer)
	old_value = db.Column(db.Integer)
	new_value = db.Column(db.Integer)
	history_datetime = db.Column(db.DateTime,
	                             default=datetime.now(tz=timezone),
	                             index=True)

	# @staticmethod
	# def add(user_id, auser_id, old_value, new_value, action_id):
	# 	entity = MoneyHistory(user_id=user_id,
	# 	                      auser_id=auser_id,old_value=old_value,
	# 	                      new_value=new_value,
	# 	                      history_datetime=datetime.now(tz=timezone))
	# 	db.session.add(entity)
	#
	# @staticmethod
	# def getAll():
	# 	return MoneyHistory.query.all()
