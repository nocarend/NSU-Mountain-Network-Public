from dataclasses import dataclass
from datetime import datetime, timedelta

from flask import send_file

from app import db
from app.errors.handlers import StockError, ValidationError
from app.helpers.functions import none_check
from app.models.category import Category


@dataclass
class Item(db.Model):
	__tablename__ = 'ITEM'
	"""
	Что сериализуется
	"""
	item_id: int
	item_name: str
	# category_id: int
	category: Category
	item_weight: int
	item_quantity_current: int
	item_quantity_max: int
	item_cost: int
	item_description: str
	item_image_path: str
	# item_datetime: datetime
	# users:str
	# avatar: str

	"""
	'-' не сериализуется
	"""
	serialize_rules = ('-CATEGORY.items', 'item_datetime', 'category_id')

	item_id = db.Column(db.Integer, primary_key=True, unique=True,
	                    autoincrement=True, index=True)
	item_name = db.Column(db.String(128), index=True)
	category_id = db.Column(db.Integer, db.ForeignKey('CATEGORY.category_id'),
	                        index=True)
	item_weight = db.Column(db.Integer, default=None, index=True)
	item_quantity_current = db.Column(db.Integer, default=0, index=True)
	item_quantity_max = db.Column(db.Integer, default=0, index=True)
	item_cost = db.Column(db.Integer, default=None, index=True)
	item_description = db.Column(db.String(200), default=None)
	item_image_path = db.Column(db.String(200), default='kitten')
	item_datetime = db.Column(db.DateTime, default=datetime.utcnow,
	                          index=True)
	category = db.relationship('Category', backref='category', lazy=True)

	@property
	def category(self):
		return Category.search_by_id(self.category_id)

	@staticmethod
	def getAll():
		return Item.query.all()

	@staticmethod
	def search_by_id(item_id):
		return Item.query.filter_by(item_id=item_id).first()

	@staticmethod
	def search_by_name_and_category(item, category):
		return Item.query.filter_by(item_name=item, category_id=category)

	@staticmethod
	def search_by_category(category_id):
		return Item.query.filter(category_id=category_id)

	# path to uploads
	def avatar(self):
		return send_file(f'./avatarImages/{self.item_image_path}.jpg',
		                 mimetype='image/jpeg')

	def users(self):
		from app.models.item_in_use import ItemInUse
		from app.models.user import User
		return ItemInUse.query.join(
			User, ItemInUse.item_id == self.item_id).filter(
			ItemInUse.user_id == User.user_id).order_by(
			ItemInUse.use_datetime.desc()).all()

	def add(self):
		if not none_check(1, [self.search_by_item_and_category(self.item_name,
		                                                       self.category_id)]):
			raise ValidationError(
				"Name of item and Id of category cannot be null.")
		db.session.add(self)
		db.session.commit()

	def delete(self):
		from app.models.item_in_use import ItemInUse
		users = ItemInUse.search_by_item(self.item_id)
		for x in users:
			x.delete()
		db.session.delete(self)
		db.session.commit()

	def book(self, user_id, count):
		from app.models.item_in_use import ItemInUse
		from app.models.user import User
		if self.item_quantity_current - count < 0:
			raise StockError()
		user = User.search_by_id(user_id)
		"""
		Админы берут сразу, а простые смертные кидают заявку.
		"""
		if 'warehouseman' in user.rolenames or 'admin' in user.rolenames:
			self.item_quantity_current -= count
			db.session.commit()
			itemRecord = ItemInUse(user_id=user_id, item_id=self.item_id,
			                       item_quantity=count,
			                       until_datetime=datetime.utcnow() +
			                                      timedelta(days=60),
			                       is_confirm=1)
		else:
			itemRecord = ItemInUse(user_id=user_id, item_id=self.item_id,
			                       item_quantity=count)
		itemRecord.add()
