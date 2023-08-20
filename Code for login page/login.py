from flask import Flask, jsonify, request, redirect, session, render_template
from flask_cors import CORS
from flask_session import Session
import modules.Data_functions as func
import secrets

app = Flask(__name__)

CORS(app)

app.secret_key = 'ASDHFOT568As51@#'

@app.route("/")
def index():
    if session.get('is_verified')==True:
        return redirect('/protected-page')
    else:    
        return render_template('login_page.html')

@app.route('/', methods=['POST'])
def login():
    data = request.get_json()
    
    if func.verify(data['email'], data['password']):
        session['is_verified'] = True
        response_data = {"verified": "yes"}
    else:    
        response_data = {"verified": "no"}
        
    return jsonify(response_data)

@app.route('/protected-page', methods=['GET'])
def protected_page():
    if session.get('is_verified')==True:
        return render_template('homepage.html')
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)