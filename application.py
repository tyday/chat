import os, json
import requests

from flask import Flask, jsonify, make_response, redirect, render_template, request, session, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret!'
socketio = SocketIO(app)

chat_rooms = {0:{"name":"general","chat_log":[]},1:{"name":"hobbies","chat_log":[]}}


@app.route("/")
def index():
    if 'user_name' in session:
        user_name = session['user_name']
        if 'chat_room' in session:
            chat_room = session["chat_room"]
        else:
            chat_room = 0
    else:
        # return render_template("login.html")
        return redirect(url_for('login'))
    user_data = {"user_name":user_name,"chat_room":chat_room}
    return render_template("index.html", user_data = user_data)
    # username = request.cookies.get('user_name')
    # if not username:
    #     return redirect(url_for('login'))
    # return render_template("index.html")
@app.route("/login")
def login():
    return render_template('login.html')

@app.route('/login/auth', methods = ['GET', 'POST'])
def login_auth():
    if request.method == 'POST':
        user_name = request.form['user_name']
        session['user_name'] = user_name
        if not 'chat_room'  in session:
            print('this fired')
            chat_room = 0
            session['chat_room'] = chat_room
            print (session['chat_room'])
        
    return redirect(url_for('index'))
    # if request.method == 'POST':
    #     user_name = request.form['user_name']
    #     resp = make_response(render_template('index.html'))
    #     resp.set_cookie('user_name', user_name)
    #     chat_room = request.cookies.get("chat_room")
    #     if not chat_room:
    #         chat_room = "0"
    #         resp.set_cookie('chat_room', chat_room)
    #     return resp
        

@socketio.on("submit vote")
def vote(data):
    selection = data["selection"]
    emit("announce vote", {"selection": selection}, broadcast=True)

@socketio.on("submit chat")
def chat(data):
    # print(data)
    # print(session)
    # user_name = data["user_name"]
    # chat_room = data["chat_room"]
    user_name = session["user_name"]
    chat_room = session["chat_room"]
    text = data["chat_text"]
    # print(text)
    chat_rooms[chat_room]["chat_log"] = text
    emit("announce chat", {"user_name":user_name, "chat_room":chat_room, "chat_text": text}, broadcast=True)
    
if __name__=='__main__':
    socketio.run(app)