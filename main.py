from flask import Flask, request, send_from_directory
from datetime import datetime
from werkzeug.exceptions import BadRequestKeyError
from markupsafe import escape
import os
import sys
import mysql.connector

app = Flask(__name__)
CONF_DIR = 'config'
app.config.from_pyfile(os.path.join(CONF_DIR, 'config.py'), silent=True)

def mysqlconnect():
    mydb = mysql.connector.connect(
        host = app.config["DB_HOST"],
        user = app.config["DB_USER"],
        password = app.config["DB_PASS"],
        database = app.config["DB_DATABASE"]
    )
    return mydb
@app.route('/')
def home():
    return send_from_directory('static', 'index.html')


@app.route('/<room>')
def room(room):
    return send_from_directory('static', 'index.html')


@app.route('/api/chat/<room>', methods=['GET'])
def get_chat(room):
    mydb = mysqlconnect()
    try:
        mycursor = mydb.cursor()
        sql = "select date, username, message from chat_messages where room = %s"
        val = (room,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()        
        mycursor.close()
        mydb.close()
        resultstr = ""
        for row in myresult:
            resultstr = "%s\n[%s] %s: %s"%(resultstr, row[0], row[1], row[2]) 
        #with open(os.path.join(CHAT_LOGS_DIR, f"{room}.txt"), 'r') as f:
            #return f.read()
        return resultstr
    finally:
        mydb.close()
    
# Implemented by Ariel Fellous
@app.route('/api/chat/<room>', methods=['POST'])
def postchatmessage(room):
    status = 200
    message = "success"
    try:
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        username = escape(request.form["username"])
        msg = escape(request.form["msg"])
        if msg != "" and username != "":
            mydb = mysqlconnect()
            try:
                mycursor = mydb.cursor()
                sql = "INSERT INTO chat_messages (date, room, username, message) VALUES (%s, %s, %s, %s)"
                val = (date, room, str(username), str(msg))
                mycursor.execute(sql, val)        
                mycursor.close()
                mydb.commit()
            except:
                status = 500
                message = "error saving to db"
            finally:
                mydb.close()
        else:
            status = 400
            message = "empty name or message"
    except BadRequestKeyError:
        status = 400
        message = "missing form fields"
    return message, status
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

