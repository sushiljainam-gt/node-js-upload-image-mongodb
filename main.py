from datetime import datetime
import os
#import magic
from app import app
from flask import Flask, flash, request, redirect, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from faceRec.tester import trainingFn



ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'webp'])

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = app.config['UPLOAD_FOLDER']

jsonFilePath = 'trainDataMap.txt'
trainResFilePath = 'trainingSaved.yml'

try:
	if not os.path.isdir(os.path.join(ROOT_DIR,UPLOAD_DIR)):
		os.mkdir(os.path.join(ROOT_DIR,UPLOAD_DIR))
	open(os.path.join(ROOT_DIR,jsonFilePath),'x')
except OSError as error:
	print(error)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def checkNameInJsonMap(personName):
	print(os.path.join(ROOT_DIR, jsonFilePath))
	# if not os.path.isfile(jsonFilePath):

	file1 = open(jsonFilePath, 'r+')
	count = 0
	resNum = 0
  
	while True:
		line = file1.readline()
	
		if not line:
			file1.writelines(("{}={}\n".format(personName,count)))
			resNum = count
			break
		count += 1
		print("Line{}: {}".format(count, line.strip()))
		name,nameNum=line.strip().split('=',1)
		print("{}: {}".format(name,nameNum))
		if name.strip() == personName.strip():
			resNum = nameNum
			break 
	
	file1.close()
	return resNum


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/file-upload')
def upload_form():
	return render_template('file-upload.html')	

@app.route('/res/<path:path>')
def send_report(path):
    return send_from_directory('res', path)

@app.route('/stats')
def send_stats():
	resp = jsonify({
		'persons':[{'name':'pc','imageCount':4}, {'name':'kr','imageCount':16}],
		'traningNeeded':False,
		'timestamp':datetime.now()})
	resp.status_code = 200
	return resp

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

	numFolder = checkNameInJsonMap(personName)
	files = request.files.getlist('files[]')
	
	errors = {}
	success = False
	
	for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			if not os.path.isdir(os.path.join(ROOT_DIR, UPLOAD_DIR, str(numFolder))):
				os.mkdir(os.path.join(ROOT_DIR, UPLOAD_DIR, str(numFolder)))
			file.save(os.path.join(ROOT_DIR, UPLOAD_DIR, str(numFolder), filename))
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

@app.route('/train', methods=['POST'])
def trainer():
	print('start training')
	trainingFn(os.path.join(ROOT_DIR, UPLOAD_DIR), os.path.join(ROOT_DIR,trainResFilePath))
	resp = jsonify({'message' : 'Training successfully done'})
	resp.status_code = 200
	return resp


if __name__ == "__main__":
    app.run()