from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()

gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

# file1 = drive.CreateFile({'title' : "Test.txt"})

# file1.SetContentString('Hello')

# file1.Upload()

upload_file_list = ['3.jpg']
for upload_file in upload_file_list:
	gfile = drive.CreateFile({'parents': [{'id': '1lBiQI_3BxF2IcnMvoTDC7pAur6brKrtB'}]})
	# Read file and set it as the content of this instance.
	gfile.SetContentFile(upload_file)
	gfile.Upload() # Upload the file.