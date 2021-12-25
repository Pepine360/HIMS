from os import error
import re
from flask import Flask, request, jsonify, render_template
from flask.helpers import url_for
from werkzeug.datastructures import FileStorage
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

from actions import Actions as act
from db.app import db, Product, Tag, Tagging
import errors as err

app = Flask(__name__)

cors = CORS(app, resources={r"/api/v1/product": {"origins": "*"}})

app.config["DEBUG"] = True
app.config["CORS_HEADERS"] = 'Content-Type'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
api = Api(app)

db.create_all()
db.init_app(app)


#Create Product class that handles creating the object, decoding the data and saving it to the database
class ProductResources(Resource):
    def post(self):
        
        file = request.files.get("file")
        amount = int(request.form["amount"]) if len(request.form["amount"]) > 0 else 0
        name = request.form["name"]
        action = request.form["action"]

        if action == "GetObject":
            return GetItem(file, amount, name)
        
        elif action == "CreateObject":
            if type(file) == str:
                raise TypeError(f"{file} is a string, not a FileSystem")

            #Creates the product from the parsed reqhest, then returns it's content and a 200 http code
            barcode = act.DecodeBarcode(act.SaveFile(file))
            product = Product(name=name, barcode=barcode, amount=amount).Add()

            return {
                "name": product.name,
                "barcode": product.barcode,
                "amount": product.amount,
            }, 200, {'Access-Control-Allow-Origin': '*'}
        
        else:
            return 400

    def get(self):
        querryResult = Product().FindAll()

        for item in querryResult:
            if item.barcode == "No barcodes detected":
                querryResult.remove(item)


        return {"data": [{
            "Name": item.name,
            "barcode": item.barcode,
            "amount": item.amount
            }
            for item in querryResult]
            if len(querryResult) > 0
            else "No Data Found"}, 200, {'Access-Control-Allow-Origin': '*'}

    def delete(self):
        name = request.form["name"]

        itemName = act.scrub(name if act.scrub(
            name) != "" else "")
        file = request.files.get("file")

        if type(file) == str:
            raise TypeError(f"{file} is a string, not a FileSystem")

        barcode = act.DecodeBarcode(act.SaveFile(file))

        if barcode == "No barcodes detected":
            raise err.InvalidBarcodeError(
                "No barcodes were found. Aborting Request")
        
        result = Product(name=itemName, barcode =barcode).Delete()

        return result, 200, {'Access-Control-Allow-Origin': '*'}



    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=False)
        parser.add_argument("amount", required=False)
        args = parser.parse_args()

        itemName = act.scrub(args["name"] if act.scrub(
            args["name"]) != "" else "")
        amount = (int(args['amount']) if int(args["amount"])
                  > 0 else 1) if args["amount"] != None else -1
        file = request.files.get("file")

        if type(file) == str:
            raise TypeError(f"{file} is a string, not a FileSystem")

        barcode = act.DecodeBarcode(act.SaveFile(file))

        if barcode == "No barcodes detected":
            raise err.InvalidBarcodeError("No barcodes were found. Aborting Request")
        
        product = Product(name=itemName, barcode=barcode, amount=amount).Remove()

        return {"data" :
            {
                "name" : product.name,
                "barcode" : product.barcode,
                "amount" : product.amount
            }
        }, 200, {'Access-Control-Allow-Origin': '*'}

def GetItem(file, amount, name):
    if type(file) == str:
        raise TypeError(f"{file} is a string, not a FileSystem")
    
    try:
        barcode = act.DecodeBarcode(act.SaveFile(file))
    except:
        barcode = ""
    
    querryResult = Product(
        name=name, barcode=barcode, amount=amount).Find()

    for item in querryResult:
        if item.barcode == "No barcodes detected":
            querryResult.remove(item)

    return {"data": [{
        "Name": item.name,
        "barcode": item.barcode,
        "amount": item.amount
    }
        for item in querryResult]
        if len(querryResult) > 0
        else "No Data Found"}, 200, {'Access-Control-Allow-Origin': '*'}

api.add_resource(ProductResources, "/api/v1/product/")
