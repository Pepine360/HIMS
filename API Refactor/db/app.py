import sqlite3 as sql
import click
import string
from flask import Flask
from numpy.core.fromnumeric import product
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    barcode = db.Column(db.String(128), nullable=False, unique=True)
    amount = db.Column(db.Integer, default=0)
    
        
    def Count(__self__):
        return Product.query.filter_by(barcode=__self__.barcode).count()

    def Add(__self__):
        if __self__.Count() > 0:
            item = Product.query.filter_by(barcode=__self__.barcode).first()
            item.amount += __self__.amount
            item.name = __self__.name
            db.session.commit()
            return item
        else:
            db.session.add(__self__)
            db.session.commit()
            return __self__
    
    
    def Find(__self__):
        if __self__.barcode:
            products = Product.query.filter_by(barcode=__self__.barcode).all()
        elif __self__.name:
            products = Product.query.filter_by(name=__self__.name).all()
        elif __self__.amount:
            products = Product.query.filter(Product.amount >= __self__.amount).all()
        else:
            products = Product.query().all()
        return products

    def Delete(__self__):
        try :
            item = Product.query.filter_by(barcode=__self__.barcode).first()
            db.session.delete(item)
            db.session.commit()
            return "Item Deleted!"
        except :
            return "Deletion Failed!"

    def Remove(__self__):
        item = Product.query.filter_by(barcode = __self__.barcode).first()
        item.amount -= __self__.amount
        db.session.commit()
        return item

        
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    
class Tagging(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), nullable=False)
    taggable_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    
