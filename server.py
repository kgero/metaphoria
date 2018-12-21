import json

from flask import Flask, Response, render_template, request

from src.expand_source import get_suggestions
from src.compound import get_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/get_sug', methods=['POST'])
def get_sug():
    data = get_suggestions(request.form['p'], request.form['c'])
    if len(data) == 0:
        print('concept not in glove vocab')
        data = {'error': "That concept isn't in the vocabulary. Try another one."}
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp

@app.route('/get_more', methods=['POST'])
def get_more():
    suggestion = request.form['s']
    poetic = request.form['p']
    concrete = request.form['c']
    data = get_template(suggestion, poetic, concrete)
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp
