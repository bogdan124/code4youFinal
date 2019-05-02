from flask import Flask,render_template,session,url_for,redirect,Blueprint
from flask_socketio import SocketIO
from second_part_forms import form_s

form_s=Blueprint('')

@app.route('/',methods=['POST','GET'])
def index():
    return render_template("index.html")


@app.route('/login',methods=['POST','GET'])
def login():
    return render_template('login.html')


@app.route('/register',methods=['POST','GET'])
def register():
    return render_template("register.html")
