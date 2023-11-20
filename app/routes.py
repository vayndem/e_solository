# app/routes.py
from flask import Flask, render_template, request
from .helper import pencarian, inserting
from app import app




@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        text = request.form['text']
        length = pencarian(text)
        return render_template('result.html', length=length, text=text)
    
@app.route('/initial', methods=['POST'])
def initial():
    if request.method == 'POST':
        simpan = "Prigel"
        koleksi = "buka"
        inisiasi = inserting(simpan,koleksi)
        return render_template('initial.html', inisiasi=inisiasi)


