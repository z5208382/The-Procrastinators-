from json import *
from flask import Flask, request, render_template, make_response, jsonify, json
import os
import sys
from helper import getEvents, getFilterEvents, getSocieties, getSociety, getProfile


if sys.platform.lower() == "win32": 
    os.system('color')

app = Flask(__name__)

@app.route('/')
def logIn():
    return render_template('main.html')

@app.route('/Home')
def loadHomePage():
    events = getEvents()
    print(f'events: {events}', file=sys.stdout)
    return render_template('index.html')

# @app.route('/Home', methods=['GET'])
# def loadEvents():
#     return jsonify(events)

@app.route('/eventdetails')
def event():
    return render_template('Eventdetails.html')

@app.route('/societies')
def socieities(): 
    return render_template('societies.html')

@app.route('/society')
def society(): 
    return render_template('society.html')

@app.route('/profile')
def profile(): 
    return render_template('profile.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/history')
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