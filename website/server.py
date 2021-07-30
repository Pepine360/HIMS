from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from decoder import BarcodeReader
from storage import storeData, loadData

app = Flask(__name__)
app.secret_key = b'_6f\mra8\tu49&jgm\nnss]/'

@app.route("/")
def home():
    return render_template('home.html')
    
    
@app.route("/Products", methods=['POST'])
def addProducts():
    if request.method == 'POST':
        return create_product()

@app.route("/findProducts", methods=["POST"])
def findProducts():
    if request.method == "POST":
        return findProduct()

def create_product():
    f = request.files.get("product_sku")  
    itemName = request.form["itemName"]

    uploaded_file = f"./{secure_filename(f.filename)}" 
    f.save(uploaded_file)
    processResult = process_image(uploaded_file)
    if processResult[0]:
        storeProduct(itemName, processResult[1])
        flash('Product added', category="success")
    else: 
        flash('Unable to process image', category="error")
        
    
    return redirect(url_for('home'))

def findProduct():
    f = request.files.get("product_code")
    itemName = request.form["productName"]
    
    savedImage = f"./{secure_filename(f.filename)}"
    f.save(savedImage)
    processedResult = process_image(savedImage)

    querryResult = ""

    if processedResult[0]:
        querryResult = searchProduct(itemName, processedResult[1])

    return render_template("home.html", data = querryResult)

def process_image(path):
    decodedData = BarcodeReader(path)
    data = [False]
    if len(decodedData) > 0:
        data[0] = True
        data.append(decodedData[0][0])
    return data
    

def storeProduct(itemName, itemData):
    storeData((itemName, itemData), "storage.db")

def searchProduct(name, data):
    result = loadData( (name, data) , "storage.db")
    app.logger.info(result)
    return result