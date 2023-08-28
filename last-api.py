from flask import Flask, request, redirect, jsonify
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from flask_mysqldb import MySQL
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import OAuth2Credentials
import json
import ast

app = Flask(__name__)

@app.after_request

def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# Connect to the database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'vdrive'

mysql = MySQL(app)
gauth = GoogleAuth()

@app.route('/')
def hello_world():
    if request.args:
        code = request.args['code']
        gauth.Auth(code)
    else:
        cursor = mysql.connection.cursor()
        cursor.execute('''select first_name from users where email=%s limit 1''', ('webdeveloper@gmail.com',))
        user = cursor.fetchone()

        if user is not None:
            token = json.loads(str(user[0]))
            access_token = []
            access_token['access_token'] = str(token['access_token'])
            return access_token[0]['access_token']
            gauth.credentials = OAuth2Credentials.from_json(json.loads(str(user[0]['access_token'])))
    credentials = gauth.credentials.to_json()
    access_token_expired = gauth.access_token_expired
    drive = GoogleDrive(gauth)

    cursor = mysql.connection.cursor()
    cursor.execute('''select code from users where email=%s limit 1''', ('webdeveloper@gmail.com',))
    user = cursor.fetchone()

    if user is not None:
        cursor.execute("UPDATE users SET first_name = %s, last_name = %s WHERE id = %s", (str(credentials),access_token_expired, 4,))
        mysql.connection.commit()
        cursor.close()

        return "Success"
    else:
        cursor.execute(''' INSERT INTO users VALUES(%s,%s,%s,%s,%s,%s)''',(4, str(credentials), access_token_expired,'webdeveloper@gmail.com',code,'password'))
        mysql.connection.commit()
        cursor.close()

    # Auto-iterate through all files that matches this query
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:
      return ('title: %s, id: %s' % (file1['title'], file1['id']))

@app.route('/login')
def login():
    cursor = mysql.connection.cursor()
    cursor.execute('''select first_name from users where email=%s limit 1''', ('webdeveloper@gmail.com',))
    user = cursor.fetchone()

    if user is not None:
        gauth.credentials = json.loads(str(user[0]))
        # gauth.Refresh()
        return "Success"
    else:
        return redirect(gauth.GetAuthUrl(), code=302)


if __name__ == '__main__':

	app.run()