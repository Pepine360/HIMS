from os import error
from flask import Flask, request, jsonify
from werkzeug.datastructures import FileStorage
from flask_restful import Api, Resource, reqparse
from werkzeug.utils import secure_filename

from actions import Actions as act
from db.app import db, Product, Tag, Tagging
import errors as err

app = Flask(__name__)


app.config["DEBUG"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
api = Api(app)

db.create_all()
db.init_app(app)

#Create Product class that handles creating the object, decoding the data and saving it to the database
class ProductResources(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        #Adds the necessary arguments to the API call, then parses it once it comes in
        # parser.add_argument("file", required = True, location='form', type = FileStorage)
        # parser.add_argument("amount", required=True, type = int)
        # args = parser.parse_args()

        file = request.files.get("file")
        amount = int(request.form["amount"])
        name = request.form["name"]

        if type(file) == str:
            raise TypeError(f"{file} is a string, not a FileSystem")
            
        # Product.query.all()

        #Creates the product from the parsed reqhest, then returns it's content and a 200 http code
        barcode = act.DecodeBarcode(act.SaveFile(file))
        product = Product(name=name, barcode=barcode, amount=amount).add()
        # product = Product.find(barcode=barcode)

        # response = jsonify()

        # response.headers.add("Access-Control-Allow-Origin", "*")

        return{
        "name": product.name,
        "barcode": product.barcode,
        "amount": product.amount,
        }, 200


#Class that gets the products corresponding to the request arguments
#Any product fitting the arguments will be returned
# class GetProduct(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required = False)
        parser.add_argument("amount", required = False)
        args = parser.parse_args()

        itemName = act.scrub(args["name"] if act.scrub(args["name"]) != "" else "")
        amount = (int(args['amount']) if int(args["amount"]) > 0 else 1) if args["amount"] != None else -1
        file = request.files.get("file")

        if type(file) == str:
            raise TypeError(f"{file} is a string, not a FileSystem")
        
        try:
            barcode = act.DecodeBarcode(act.SaveFile(file))
        except:
            barcode = ""

        querryResult = Product(name=itemName, barcode=barcode, amount=amount).Find()

        for item in querryResult:
            if item.barcode == "No barcodes detected":
                querryResult.remove(item)

        # response = jsonify()

        # response.headers.add("Access-Control-Allow-Origin", "*")

        return {"data": [{
            "Name": item.name,
            "barcode": item.barcode,
            "amount": item.amount
            }
            for item in querryResult]
            if len(querryResult) > 0
            else "No Data Found"}, 200

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=False)
        args = parser.parse_args()

        itemName = act.scrub(args["name"] if act.scrub(
            args["name"]) != "" else "")
        file = request.files.get("file")

        if type(file) == str:
            raise TypeError(f"{file} is a string, not a FileSystem")

        barcode = act.DecodeBarcode(act.SaveFile(file))

        if barcode == "No barcodes detected":
            raise err.InvalidBarcodeError(
                "No barcodes were found. Aborting Request")
        
        result = Product(name=itemName, barcode =barcode).delete()

        return result, 200



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
        
        product = Product(name=itemName, barcode=barcode, amount=amount).remove()

        return {"data" :
            {
                "name" : product.name,
                "barcode" : product.barcode,
                "amount" : product.amount
            }
        }, 200


api.add_resource(ProductResources, "/api/v1/product/")


if __name__ == "__main__":
    app.run(host="192.168.2.25", port='5000')
