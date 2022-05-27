import os
#import magic
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template, jsonify
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'webp'])


try:
	os.mkdir(app.config['UPLOAD_FOLDER'])
except OSError as error:
	print(error)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('file-upload.html')

@app.route('/python-flask-files-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'files[]' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	personName = request.args.get('person_name')
	if(len(personName.strip())):
		print('The person name is given')
	else:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp

	files = request.files.getlist('files[]')
	
	errors = {}
	success = False
	
	for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			success = True
		else:
			errors[file.filename] = 'File type is not allowed'
	
	if success and errors:
		errors['message'] = 'File(s) successfully uploaded'
		resp = jsonify(errors)
		resp.status_code = 206
		return resp
	if success:
		resp = jsonify({'message' : 'Files successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify(errors)
		resp.status_code = 400
		return resp

if __name__ == "__main__":
    app.run()