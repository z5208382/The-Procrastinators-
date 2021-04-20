from flask import Flask
from flask import render_template
import os
import sys

if sys.platform.lower() == "win32": 
    os.system('color')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Eventdetails')
def event():
    return render_template('Eventdetails.html')

@app.route('/Societies')
def socieities(): 
    return render_template('societies.html')

@app.route('/Society')
def society(): 
    return render_template('society.html')

@app.route('/Profile')
def profile(): 
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)