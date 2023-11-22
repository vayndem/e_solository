# app/routes.py
from flask import Flask, render_template, request
from .helper import pencarian, inserting, add_mongo
from app import app




@app.route('/', methods=['GET','POST'])
def index():
    if request.method ==" POST":
        v = request.form['id_skripsi']
        w = request.form['judul']
        x = request.form['abstrak']
        y = request.form['link']
        tambahin= tambah(v, w, x, y)
        return render_template('index.html',tambah=tambahin)
    else:
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
        koleksi = "buku"
        inisiasi = inserting(simpan,koleksi)
        return render_template('initial.html', inisiasi=inisiasi)
    

@app.route('/tambah', methods=['POST'])
def tambah():
    if request.method == 'POST':
        return render_template('tambah.html')
    

@app.route('/inserting', methods=['POST'])
def tambahan():
    if request.method == "POST":
        v = request.form['id_skripsi']
        w = request.form['judul']
        x = request.form['abstrak']
        y = request.form['link']
        tambahin = add_mongo(v,w,x,y)
        return render_template('initial.html',inisiasi=tambahin)

    




