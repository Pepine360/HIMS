from flask import Flask, request
from numpy.core.fromnumeric import product
from werkzeug.datastructures import FileStorage
from flask_restful import Api, Resource, reqparse
from werkzeug.utils import secure_filename
from product import Product
from actions import Actions as act


app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)

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
        itemName = request.form["name"]

        if type(file) == str:
            raise TypeError(f"{file} is a string, not a FileSystem")

        #Creates the product from the parsed reqhest, then returns it's content and a 200 http code
        product = Product(act.DecodeBarcode(act.SaveFile(file)), amount, itemName)
        
        act.HandleStorage("create", product, )

        return {
            "data" : product.GetProductData(),
        }, 200

    
    #Any product fitting the arguments will be returned 
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required = False)
        parser.add_argument("amount", required = False)
        args = parser.parse_args()

        itemName = act.scrub(args["name"]) if act.scrub(args["name"]) != "" else "Default Name"
        amount = int(args["amount"]) if int(args["amount"]) != 0 else 1
        file = request.files.get("file")


        product = Product(act.DecodeBarcode(act.SaveFile(file)), amount, itemName)
        
        queryResult = act.HandleStorage("read", product)

        return queryResult, 200



api.add_resource(ProductResources, "/api/v1/product/")

if __name__ == "__main__":
    app.run()
