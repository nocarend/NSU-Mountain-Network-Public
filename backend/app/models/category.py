from dataclasses import dataclass
from datetime import datetime

from app import db, timezone


@dataclass
class Category(db.Model):
	__tablename__ = 'CATEGORY'
	"""
	Что сериализуется
	"""
	category_id: int
	category_name: str
	category_weight: int
	# category_datetime: datetime
	# items: list
	# serialize_rules = ('-CATEGORY.items', 'item_datetime',)

	category_id = db.Column(db.Integer, primary_key=True, unique=True,
	                        autoincrement=True,
	                        index=True)
	category_name = db.Column(db.String, index=True)
	category_weight = db.Column(db.Integer, default=None, index=True)
	category_datetime = db.Column(db.DateTime,
	                              index=True)  # datetime.now() переместить в

	# метод

	@staticmethod
	def search_by_name(name):
		return Category.query.filter_by(category_name=name).first()

	@staticmethod
	def search_by_id(id):
		return Category.query.filter_by(category_id=id).first()

	@staticmethod
	def getAll():
		return Category.query.all()

	# @property
	def items(self):
		from app.models.item import Item
		return Item.search_by_category(self.category_id)

	def add(self):
		self.category_datetime = datetime.now(tz=timezone)
		db.session.add(self)

	def delete(self):
		db.session.delete(self)
