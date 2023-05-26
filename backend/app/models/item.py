from dataclasses import dataclass
from datetime import datetime, timedelta

from flask_praetorian import current_user_id

from app import db, timezone
from app.errors.handlers import StockError, ValidationError
from app.helpers.functions import none_check


@dataclass
class Item(db.Model):
	__tablename__ = 'ITEM'
	"""
	Что сериализуется
	"""
	item_id: int
	item_name: str
	category_id: int
	# category: Category
	item_weight: int
	item_quantity_current: int
	item_quantity_max: int
	item_cost: int
	item_description: str
	# item_image_path: str
	# item_datetime: datetime
	# users:str
	# avatar: str

	"""
	'-' не сериализуется
	"""
	serialize_rules = ('-CATEGORY.items', 'item_datetime',)

	item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	item_name = db.Column(db.String(128), index=True)
	category_id = db.Column(db.Integer, db.ForeignKey('CATEGORY.category_id'))
	item_weight = db.Column(db.Integer, default=None)
	item_quantity_max = db.Column(db.Integer, default=0)
	item_cost = db.Column(db.Integer, default=None, index=True)
	item_description = db.Column(db.String(200), default=None, index=True)
	# item_image_path = db.Column(db.String(200), default='kitten',
	# index=True)
	item_datetime = db.Column(db.DateTime,
	                          index=True)

	@staticmethod
	def getAll():
		return Item.query.all()

	@staticmethod
	def search_by_id(item_id):
		return Item.query.filter_by(item_id=item_id).first()

	@staticmethod
	def search_by_name_and_category(item, category):
		return Item.query.filter_by(item_name=item,
		                            category_id=category).first()

	@staticmethod
	def search_by_category(category_id):
		return Item.query.filter_by(category_id=category_id).all()

	def free_items_at_date(self, datetime_from, datetime_to):
		from app.models.item_in_use import ItemInUse
		booked = 0
		items = ItemInUse.search_by_item(self.item_id, 3)
		for item in items:
			if datetime_from <= item.until_datetime <= datetime_to or\
					datetime_from <= item.use_datetime <= datetime_to or\
					item.use_datetime <= datetime_from <= datetime_to <=\
					item.until_datetime:
				if item.is_confirm == 2 or item.is_confirm == 1:
					booked += item.item_quantity
		return self.item_quantity_max - booked

	@property
	def item_quantity_current(self):
		counts = self.free_items_at_date(
			datetime.now(tz=timezone).replace(tzinfo=None),
			datetime.now(tz=timezone).replace(tzinfo=None))
		return counts

	# path to uploads
	# def avatar(self):
	# 	return send_file(f'./avatarImages/{self.item_image_path}.jpg',
	# 	                 mimetype='image/jpeg')

	def users(self):
		from app.models.item_in_use import ItemInUse
		from app.models.user import User
		return ItemInUse.query.join(
			User, ItemInUse.item_id == self.item_id).filter(
			ItemInUse.user_id == User.user_id).order_by(
			ItemInUse.use_datetime.desc()).all()

	def add(self):
		if not none_check(1, [Item.search_by_name_and_category(self.item_name,
		                                                       self.category_id)]):
			raise ValidationError(
				"Name has already taken in this category")
		self.item_datetime = datetime.now(tz=timezone)
		db.session.add(self)

	# db.session.commit()

	def delete(self):
		from app.models.item_in_use import ItemInUse
		users = ItemInUse.search_by_item(self.item_id)
		for x in users:
			x.delete()
		db.session.delete(self)

	# db.session.commit()

	def book(self, count, datetime_from, datetime_to):
		if count < 1:
			raise ValidationError()
		user_id = current_user_id()
		from app.models.item_in_use import ItemInUse
		from app.models.user import User
		counts = self.free_items_at_date(datetime_from, datetime_to)
		if counts - count < 0 or datetime_from + timedelta(
				days=60) > datetime_to:
			raise StockError()
		user = User.search_by_id(user_id)
		"""
		Админы берут сразу, а простые смертные кидают заявку.
		"""
		if self.item_quantity_current - count >= 0 and (
				'warehouseman' in user.rolenames or 'admin' in
				user.rolenames):
			itemRecord = ItemInUse(user_id=user_id, item_id=self.item_id,
			                       item_quantity=count,
			                       use_datetime=datetime_from,
			                       until_datetime=datetime_to,
			                       is_confirm=1)
			# RentHistory.add(user_id, 1, self.item_id, count)
			# RentHistory.add(user_id, 2, self.item_id, count, user_id)
			itemRecord.add()
		elif counts - count >= 0:
			itemRecord = ItemInUse(user_id=user_id, item_id=self.item_id,
			                       item_quantity=count,
			                       use_datetime=datetime_from,
			                       until_datetime=datetime_to)
			# RentHistory.add(user_id, 1, self.item_id, count)
			itemRecord.add()
		else:
			raise StockError()
