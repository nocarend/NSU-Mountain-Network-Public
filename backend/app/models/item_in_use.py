from dataclasses import dataclass
from datetime import datetime, timedelta

from flask_praetorian import current_user_id

from app import db
from app.errors.handlers import ElementNotFoundError, StockError
from app.models.item import Item


@dataclass
class ItemInUse(db.Model):
	__tablename__ = 'ITEM_IN_USE'
	# use_id: int
	user_id: int
	# item_id: int
	item: Item
	# user: User
	item_quantity: int
	is_confirm: int
	use_description: str
	use_datetime: datetime
	until_datetime: datetime
	# is_notified:int

	use_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
	user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'), index=True)
	item_id = db.Column(db.Integer, db.ForeignKey('ITEM.item_id'), index=True)
	item_quantity = db.Column(db.Integer, default=1, index=True)
	is_confirm = db.Column(db.Integer, default=0, index=True)
	use_description = db.Column(db.String(150), default='')
	use_datetime = db.Column(db.DateTime, default=datetime.utcnow(), index=True)
	until_datetime = db.Column(db.DateTime, default=datetime.utcnow(), index=True)
	is_notified = db.Column(db.Integer, default=0, index=True)

	@property
	def item(self):
		return Item.query.filter_by(item_id=self.item_id).first()

	@property
	def user(self):
		from app.models.user import User
		return User.query.filter_by(user_id=self.user_id).first()

	@staticmethod
	def search_by_use_id(use_id):
		return ItemInUse.query.filter_by(use_id=use_id).first()

	@staticmethod
	def getAll():
		return ItemInUse.query.all()

	@staticmethod
	def search_by_user(user_id, all=True):
		return ItemInUse.query.filter_by(user_id=user_id).all() if all else\
			ItemInUse.query.filter_by(user_id=user_id, is_confirm=2).all()

	"""
	взятые вещи, не забронированные
	"""

	@staticmethod
	def search_by_item(item_id, all=True):
		return ItemInUse.query.filter_by(item_id=item_id).all() if all else\
			ItemInUse.query.filter_by(item_id=item_id, is_confirm=2).all()

	def prolong(self, days_time=30):
		self.until_datetime += timedelta(days=days_time)
		self.is_notified = 0
		db.session.commit()

	def unbook(self, count):
		item = self.item
		if count is None or count > self.item_quantity or count <= 0:
			raise StockError()
		if self.user_id != current_user_id() or self.is_confirm == 2:
			raise ElementNotFoundError()
		if self.is_confirm == 1:
			item.item_quantity_current += count
		if count == self.item_quantity:
			self.delete()
		else:
			self.item_quantity -= count
		db.session.commit()

	def return_(self, quantity=1):
		if quantity > self.item_quantity or quantity <= 0:
			raise StockError()
		item = self.item
		item.item_quantity_current += quantity
		if quantity == self.item_quantity:
			self.delete()
		else:
			self.item_quantity -= quantity
		db.session.commit()

	def add(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def notify(self):
		self.is_notified = 1
		db.session.commit()
