from flask import Flask, request
from werkzeug.datastructures import FileStorage
from flask_restful import Api, Resource, reqparse
from werkzeug.utils import secure_filename
from product import Product
from actions import Actions as act


app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)

#Create Product class that handles creating the object, decoding the data and saving it to the database
class CreateProduct(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        #Adds the necessary arguments to the API call, then parses it once it comes in
        # parser.add_argument("file", required = True, location='form', type = FileStorage)
        # parser.add_argument("amount", required=True, type = int)
        # args = parser.parse_args()

        file = request.files.get("file")
        amount = int(request.form["amount"])

        if type(file) == str:
            raise TypeError(f"{file} is a string, not a FileSystem")

        #Creates the product from the parsed reqhest, then returns it's content and a 200 http code
        product = Product(act.DecodeBarcode(act.SaveFile(file)), amount)
        
        act.HandleStorage("create", product)

        return {
            "data" : product.getProductData(),
            "HTTP Method " : "POST",
            "Action" : "Create"
        }, 200

#Class that gets the products corresponding to the request arguments
#Any product fitting the arguments will be returned
class GetProduct(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("barcode", required = True)
        parser.add_argument("amount", required = False)
        args = parser.parse_args()

        

        # if args["amount "] > 0:
        #     data = act.GetAllData(args["barcode"])
        # else:
        #     data = act.GetAllData(args["barcode"], args["amount"])

        return {"data": args}, 200



api.add_resource(GetProduct, "/api/v1/product/get")
api.add_resource(CreateProduct, "/api/v1/product/create")

if __name__ == "__main__":
    app.run()
