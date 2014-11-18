# -*- coding: utf-8 -*-
from peewee import *

from . import db

from json import dumps
from flask.ext.login import UserMixin

class BaseModel(db.Model):
	@property
	def simple_dict(self):
		return self.__dict__['_data']

	@property
	def json(self):
		return dumps(self.simple_dict)

class Image(BaseModel):
	filename = CharField()
	url = CharField()

class Brand(BaseModel):
	name = CharField()

class User(BaseModel, UserMixin):
	name = CharField()
	last_name = CharField()
	age = IntegerField()
	email = TextField()
	password = CharField()
	address = CharField()
	accept_news = BooleanField()
	first_login = BooleanField(default=True)

	@property
	def store(self):
		return Store.get(Store.owner == self)

class Store(BaseModel):
	owner = ForeignKeyField(User)
	logo = ForeignKeyField(Image, null=True)
	name = CharField()
	description = TextField(null=True)
	@property
	def showcase(self):
		return [ c for c in Cloth.select().where((Cloth.store == self)&(Cloth.in_showcase == True)) ]

	@property
	def frozen(self):
		return [ c for c in Cloth.select().where((Cloth.store == self)&(Cloth.is_frozen == True)) ]

class Cloth(BaseModel):
	store = ForeignKeyField(Store)
	brand = ForeignKeyField(Brand,null=True)
	image = ForeignKeyField(Image)
	name = CharField()
	description = CharField(null=True)
	in_showcase = BooleanField(default=False)
	is_frozen = BooleanField(default=False)

MODELS=[User,Brand,Image,Store,Cloth]
def create_tables():
	for m in MODELS:
		m.create_table(True)