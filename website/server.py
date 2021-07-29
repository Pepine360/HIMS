from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from decoder import BarcodeReader
from numpy import asarray

app = Flask(__name__)
app.secret_key = b'_6f\mra8\tu49&jgm\nnss]/'

@app.route("/")
def home():
    return render_template('home.html')
    
    
@app.route("/products", methods=['POST'])
def products():
    if request.method == 'POST':
        return create_product()


def create_product():
    f = request.files.get("product_sku")
    uploaded_file = f"./{secure_filename(f.filename)}" 
    f.save(uploaded_file)
    if process_image(uploaded_file):
        flash('Product added', category="success")
    else: 
        flash('Unable to process image', category="error")
        
    
    return redirect(url_for('home'))
    
def process_image(path):
    decodedData = BarcodeReader(path)
    status = False
    if len(decodedData) > 0:
        status = True
        for item in decodedData:
            app.logger.debug(item)
    
    return status
