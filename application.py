import os, json
import requests

from flask import Flask, jsonify, make_response, redirect, render_template, request, session, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret!'
socketio = SocketIO(app)

chat_rooms = {0:{"name":"General","chat_log":[]},
            1:{"name":"hobbies","chat_log":[]},
            2:{"name":"school","chat_log":[]}}


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
    session['chat_room_name'] = chat_rooms[chat_room]["name"]
    session['chat_room_id'] = chat_room
    chat_log = chat_rooms[chat_room]["chat_log"]
    print(chat_log)
    print(chat_rooms)
    print(json.dumps(chat_rooms))
    user_data = {"user_name":user_name,"chat_room":chat_room, "chat_log": chat_log, "chat_rooms":chat_rooms}
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
        
@app.route('/logout')
def logout():
    # session['user_name']=None
    # session['chat_room']=0
    session.clear()
    return redirect(url_for('index'))
        

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
    text_log = {"user_name": user_name, "text":data["chat_text"]}
    chat_rooms[chat_room]["chat_log"].append(text_log)
    emit("announce chat", {"user_name":user_name, "chat_room":chat_room, "chat_text": data["chat_text"]}, broadcast=True)
    print(chat_rooms[chat_room])  

@socketio.on("submit room_change")    
def room_change(data):
    user_name = session["user_name"]
    room_source = int(data["room_source"])
    room_destination = int(data["room_destination"])
    departure_message = f"{user_name} has left chat."
    arrival_message = f"{user_name} has entered chat"
    session["chat_room"] = room_destination;
    # Update room logs with information
    # chat_rooms[room_source]["chat_log"].append(departure_message)
    # chat_rooms[room_destination]["chat_log"].append(arrival_message)
    # emit Departure chat message
    emit("announce chat", {"user_name":user_name, "chat_room":room_source, "chat_text": departure_message}, broadcast=True, include_self=False)
    # emit Arrival chat message
    emit("announce chat", {"user_name":user_name, "chat_room":room_destination, "chat_text": arrival_message}, broadcast=True)
    emit("update room", {"chat_log":chat_rooms[room_destination]["chat_log"]})

@socketio.on("submit new_room")
def new_room(data):
    room_name = data['room_name']
    room_id = len(chat_rooms)
    chat_rooms[room_id] = {"name":room_name,"chat_log":[]}
    onclick_code = f"change_room({room_id},{chat_rooms[room_id]})"
    print(onclick_code)
    emit("new room", {"room_name":room_name, "room_id":room_id,"code":onclick_code})
    


if __name__=='__main__':
    socketio.run(app)