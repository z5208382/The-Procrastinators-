from json import *
from flask import Flask, request
from flask import render_template
import os
import sys
import helper

if sys.platform.lower() == "win32": 
    os.system('color')

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def logIn():
        return render_template('main.html')

@app.route('/Home')
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

@app.route('/Feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/History')
def history(): 
    return render_template('history.html')

# @app.route('/test', methods=['POST', 'GET'])
# def test():
#     response = request.get_json()
#     print(response)
#     result = {'data' : 'poop'}
#     return dumps(result)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)