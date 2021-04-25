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
    return render_template('index.html')

@app.route('/Home', methods=['POST'])
def loadEvents():
    events = getEvents()
    return jsonify(events)

@app.route('/Eventdetails')
def loadEventDetailsPage():
    return render_template('eventdetails.html')

@app.route('/Eventdetails', methods=['POST'])
def loadEventDetails():
    events = getEvents()
    return jsonify(events)

@app.route('/Societies')
def loadSocietiesPage():
    return render_template('societies.html')

@app.route('/Societies', methods=['POST'])
def loadSocieties():
    societies = getSocieties()
    return jsonify(societies)

@app.route('/Society', methods=['GET'])
def loadSociety():
    id = request.args.get('id')
    society = getSociety(id)
    return render_template('society.html', society=society)

@app.route('/Profile')
def loadProfilePage(): 
    return render_template('profile.html')

@app.route('/Profile', methods=['POST'])
def loadProfile(): 
    events = getEvents()
    return jsonify(events)

@app.route('/Feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/History')
def loadHistoryPage(): 
    return render_template('history.html')

@app.route('/History', methods=['POST'])
def loadHistory(): 
    events = getEvents()
    return jsonify(events)

@app.route('/Category', methods=['POST'])
def loadCategoryEvents():
    category = request.args.get('category')
    events = getFilterEvents(category)
    return render_template('index.html', events=events)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)