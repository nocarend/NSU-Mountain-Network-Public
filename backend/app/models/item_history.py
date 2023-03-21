from dataclasses import dataclass
from datetime import datetime

from app import db


@dataclass
class ItemHistory(db.Model):
	__tablename__ = 'ITEM_HISTORY'
	history_id: int
	user_id: int
	action_id: int
	item_id: int
	change_value: int
	new_value: int
	history_datetime: datetime

	history_id = db.Column(db.Integer, primary_key=True, unique=True,
	                       index=True)
	user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'), index=True)
	action_id = db.Column(db.Integer, index=True)
	item_id = db.Column(db.Integer, db.ForeignKey('ITEM.item_id'), index=True)
	change_value = db.Column(db.Integer)
	new_value = db.Column(db.Integer)
	history_datetime = db.Column(db.DateTime, default=datetime.utcnow(),
	                             index=True)
