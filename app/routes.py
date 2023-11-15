# app/routes.py
from flask import Flask, render_template, request
from .helper import pencarian
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


