import os
import requests

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret!'
socketio = SocketIO(app)

chat_rooms = {0:{"name":"general","chat_log":[]},1:{"name":"hobbies","chat_log":[]}}


@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("submit vote")
def vote(data):
    selection = data["selection"]
    emit("announce vote", {"selection": selection}, broadcast=True)

@socketio.on("submit chat")
def chat(data):
    print(data)
    chat_room = data["chat_room"]
    text = data["chat_text"]
    print(text)
    chat_rooms[chat_room]["chat_log"] = text
    emit("announce chat", {"chat_text": text}, broadcast=True)
    
if __name__=='__main__':
    socketio.run(app)