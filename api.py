# using flask_restful
from flask import Flask, jsonify, request, redirect, url_for
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os, shutil, tempfile
import json

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)

@app.after_request

def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
# other methods include put, delete, etc.
class Hello(Resource):

	# corresponds to the GET request.
	# this function is called whenever there
	# is a GET request for this resource
	def get(self):

		return jsonify({'message': 'hello world'})

	# Corresponds to POST request
	def post(self):
            try:
                file = request.files['file']
                filename = secure_filename(file.filename)
                # create the folders when setting up your app
                os.makedirs(os.path.join(app.instance_path, 'htmlfi'), exist_ok=True)

                # when saving the file
                file.save(os.path.join(app.instance_path, 'htmlfi', filename))
            finally:
                file.close()

            drive = Authenticate()

            # Create folder
            if(os.path.exists("folder_id.txt")):
                with open("folder_id.txt", "r") as folderIdFile:
                    folderId = folderIdFile.read()
            else:
                with open("folder_id.txt", "w") as folderIdFile:
                    folder_name = 'vDrive'
                    folder_metadata = {'title' : folder_name, 'mimeType' : 'application/vnd.google-apps.folder'}
                    folder = drive.CreateFile(folder_metadata)
                    folder.Upload()

                    folderId = folder['id']
                    folderIdFile.write(folderId)

            upload_file = url_for('uploads', filename=filename)[1:]
            
            gfile = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folderId}]})
            # f.close()
            # Read file and set it as the content of this instance.
            gfile.SetContentFile(upload_file)
            gfile.Upload(param={'supportsTeamDrives': True}) # Upload the file.

            new_permission = {
                'id': 'anyoneWithLink',
                'type': 'anyone',
                'value': 'anyoneWithLink',
                'withLink': True,
                'role': 'reader'
            }

            permission = gfile.auth.service.permissions().insert(
                fileId=gfile['id'], body=new_permission, supportsTeamDrives=True).execute(http=gfile.http)

            res = "https://drive.google.com/file/d/" + gfile['id'] + "/view"

            return res

class Uploads(Resource):

    def get(self, filename):

        return jsonify({'uploads': filename})

class ClearFiles(Resource):
    def get(self):
        folder = 'instance/htmlfi'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

class ListFiles(Resource):
    def get(self):
        if(os.path.exists("folder_id.txt")):
            with open("folder_id.txt", "r") as folderIdFile:
                folderId = folderIdFile.read()
        drive = Authenticate()
        file_list = drive.ListFile({'q': "'" + folderId + "' in parents and trashed=false"}).GetList()
        return file_list

class Authenticate(Resource):
    def get(self):
        gauth = GoogleAuth()
        # Try to load saved client credentials
        gauth.LoadCredentialsFile("cs.txt")
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.LocalWebserverAuth()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        # Save the current credentials to a file
        gauth.SaveCredentialsFile("cs.txt")

        return gauth.success()

# adding the defined resources along with their corresponding urls
api.add_resource(Hello, '/')
api.add_resource(Uploads, '/instance/htmlfi/<filename>')
api.add_resource(ClearFiles, '/clear-files')
api.add_resource(ListFiles, '/list-files')
api.add_resource(Authenticate, '/authenticate')


# driver function
if __name__ == '__main__':

	app.run(debug = True)
