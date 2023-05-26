from dataclasses import dataclass
from datetime import datetime, timedelta

from flask_praetorian import current_rolenames, current_user_id

from app import db, timezone
from app.errors.handlers import ConditionsError, ElementNotFoundError,\
	StockError
from app.models.item import Item


@dataclass
class ItemInUse(db.Model):
	__tablename__ = 'ITEM_IN_USE'
	use_id: int
	user_id: int
	# item_id: int
	# item: Item
	# user: User
	item_quantity: int
	# item_quantity_return: int
	is_confirm: int
	use_description: str
	use_datetime: datetime
	until_datetime: datetime
	item_id: int
	# is_notified:int
	warehouseman_id: int

	serialize_rules = ('-item', '-item_datetime', '-is_notified')

	use_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
	                   index=True)
	user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'))
	item_id = db.Column(db.Integer, db.ForeignKey('ITEM.item_id'))
	item_quantity = db.Column(db.Integer, default=1)
	item_quantity_return = db.Column(db.Integer, default=0)
	is_confirm = db.Column(db.Integer, default=0)
	use_description = db.Column(db.String(150), default='')
	use_datetime = db.Column(db.DateTime, default=datetime.now(tz=timezone),
	                         index=True)
	until_datetime = db.Column(db.DateTime, default=datetime.now(tz=timezone),
	                           index=True)
	# default delete from datetime
	is_notified = db.Column(db.Integer, default=0)
	warehouseman_id = db.Column(db.Integer, default=-1)

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
	def search_by_user(user_id, all=3):
		return ItemInUse.query.filter_by(
			user_id=user_id).all() if all == 3 else\
			ItemInUse.query.filter_by(user_id=user_id, is_confirm=all).all()

	@staticmethod
	def search_by_item(item_id, all=3):
		return ItemInUse.query.filter_by(
			item_id=item_id).all() if all == 3 else\
			ItemInUse.query.filter_by(item_id=item_id, is_confirm=all).all()

	def prolong(self, days_time=30):
		counts = self.item.free_items_at_date(self.until_datetime,
		                                      self.until_datetime +
		                                      timedelta(
			                                      days=days_time))
		if counts < self.item_quantity or self.use_datetime + timedelta(
				days=days_time) > self.until_datetime:
			raise StockError(
				"Cannot prolong due to not enough items. Or your prolong "
				"time "
				"is too heavy.")
		self.until_datetime += timedelta(days=days_time)
		self.is_notified = 0

	def unbook(self, count, flag=0, description=''):
		if count is None or count > self.item_quantity or count <= 0:
			raise StockError()
		if (self.user_id != current_user_id() and 'admin' not in
		    current_rolenames() and 'warehouseman' not in
		    current_rolenames())\
				or self.is_confirm == 2 or self.is_confirm == 4:
			raise ElementNotFoundError()
		self.use_description = description
		if count == self.item_quantity and flag == 1:
			self.is_confirm = 4  # rej
		else:
			self.item_quantity -= count

	def return_(self, quantity=1):
		if quantity > self.item_quantity or quantity <= 0 or self.is_confirm\
				!= 2:
			raise StockError()
		if quantity == self.item_quantity:
			self.item_quantity = self.item_quantity_return
			self.is_confirm = 5
		else:
			self.item_quantity -= quantity

	@staticmethod
	def approve(use_id, description):
		itemRecord = ItemInUse.search_by_use_id(use_id)
		if itemRecord is None:
			raise ElementNotFoundError()
		item = itemRecord.item
		if item.free_items_at_date(itemRecord.use_datetime,
		                           itemRecord.until_datetime) -\
				itemRecord.item_quantity < 0:
			raise StockError(
				"В этой заявке больше вещей чем будет свободно на складе")
		itemRecord.is_confirm = 1
		itemRecord.use_description = description
		itemRecord.warehouseman_id = current_user_id()

	@staticmethod
	def reject(use_id, reason):
		itemRecord = ItemInUse.search_by_use_id(use_id)
		if itemRecord is None:
			raise ElementNotFoundError()
		itemRecord.use_description = reason
		itemRecord.is_confirm = 4

	@staticmethod
	def give(use_id):
		itemRecord = ItemInUse.search_by_use_id(use_id)
		if itemRecord.is_confirm != 1:
			raise ConditionsError()
		if itemRecord is None:
			raise ElementNotFoundError()
		itemRecord.is_confirm = 2

	def sest_description(self, description):
		self.use_description = description

	def add(self):
		db.session.add(self)

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def notify(self):
		self.is_notified = 1
		db.session.commit()
