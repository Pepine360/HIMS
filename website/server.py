from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

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
    f = request.files['product_sku']
    uploaded_file = f"/tmp/{secure_filename(f.filename)}" 
    f.save(uploaded_file)
    if process_image(file=uploaded_file):
        flash('Product added', category="success")
    else: 
        flash('Unable to process image', category="error")
        
    
    return redirect(url_for('home'))
    
def process_image(file):
    return False