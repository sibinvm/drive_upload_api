from flask import Flask, jsonify, request, redirect, session, url_for
from flask_restful import Resource, Api
from httplib2 import Response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os, shutil
import json

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from flask_session import Session

# creating the flask app
app = Flask(__name__)
# creating an API object
app.secret_key = "123456789"
api = Api(app)

@app.after_request

def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

global gauth
gauth = GoogleAuth()

class Login(Resource):
    def get(self):
        if (session.get('code')):
            gauth.Authenticate(request.args['code'])
            return 'done'
        else:
            return gauth.GetAuthUrl()
    
class getToken(Resource):
    def get(self):
        # gauth.LoadCredentialsFile("mycreds.txt")
        # if gauth.credentials is None:
        #     # Authenticate if they're not there
        #     gauth.LocalWebserverAuth()
        # elif gauth.access_token_expired:
        #     # Refresh them if expired
        #     gauth.Refresh()
        # else:
        #     # Initialize the saved creds
        #     gauth.Authorize()
        # gauth.SaveCredentialsFile("mycreds.txt")
        gauth.Authenticate(request.args['code'])
        # gauth.SaveCredentialsFile("mycreds.txt")
        session["code"] = request.args['code']
        return session.get("code")

class getcode(Resource):
    def get(self):
        if 'code' in session:
            code = session['code']
            return jsonify({'code' :session.get("code")})
    
api.add_resource(Login, '/login')
api.add_resource(getToken, '/')
api.add_resource(getcode, '/get-code')

# driver function
if __name__ == '__main__':

	app.run(debug = True)