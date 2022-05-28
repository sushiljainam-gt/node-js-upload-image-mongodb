from datetime import datetime
import os
#import magic
from app import app
from flask import Flask, flash, request, redirect, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from faceRec.tester import trainingFn, runTest
import globalStates


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'webp'])

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = app.config['UPLOAD_FOLDER']
TEST_DIR = app.config['TEST_DIR']
DETECT_OUT_DIR = app.config['DETECT_OUT_DIR']

jsonFilePath = 'trainDataMap.txt'
trainResFilePath = 'trainingSaved.yml'
globalStatespath = 'globalsFaceApp.txt'

try:
	if not os.path.isdir(os.path.join(ROOT_DIR,UPLOAD_DIR)):
		os.mkdir(os.path.join(ROOT_DIR,UPLOAD_DIR))
	if not os.path.isdir(os.path.join(ROOT_DIR,TEST_DIR)):
		os.mkdir(os.path.join(ROOT_DIR,TEST_DIR))
	if not os.path.isdir(os.path.join(ROOT_DIR,DETECT_OUT_DIR)):
		os.mkdir(os.path.join(ROOT_DIR,DETECT_OUT_DIR))
	open(os.path.join(ROOT_DIR,jsonFilePath),'x')
except OSError as error:
	print(error)

globalStates.init(os.path.join(ROOT_DIR, globalStatespath))

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def checkNameInJsonMap(personName):
	print(os.path.join(ROOT_DIR, jsonFilePath))
	# if not os.path.isfile(jsonFilePath):

	file1 = open(os.path.join(ROOT_DIR, jsonFilePath), 'r+')
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

def nameForNumberMap(num):
	return 'priyanka'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/file-upload')
def upload_form():
	return render_template('file-upload.html')	

@app.route('/detect')
def html_detect():
	return render_template('detect.html')	

@app.route('/res/<path:path>')
def send_report(path):
    return send_from_directory('res', path)

@app.route('/stats')
def send_stats():
	resp = jsonify({
		'persons':[{'name':'pc','imageCount':4}, {'name':'kr','imageCount':16}],
		'trainingNeeded':globalStates.isTrainingBehind(os.path.join(ROOT_DIR, globalStatespath)),
		'timestamp':datetime.now()})
	resp.status_code = 200
	return resp

@app.route('/train', methods=['POST'])
def trainer():
	print('start training')
	trainingFn(os.path.join(ROOT_DIR, UPLOAD_DIR), os.path.join(ROOT_DIR,trainResFilePath))
	globalStates.saveLastTrain(os.path.join(ROOT_DIR, globalStatespath))
	resp = jsonify({'message' : 'Training successfully done'})
	resp.status_code = 200
	return resp

@app.route('/detect-image', methods=['POST'])
def detect_image():
	print('start detecting and recognition')
	# check if the post request has the file part
	if 'files[]' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	
	errors = {}
	success = False
	files = request.files.getlist('files[]')
	for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			if not os.path.isdir(os.path.join(ROOT_DIR, TEST_DIR)):
				os.mkdir(os.path.join(ROOT_DIR, TEST_DIR))
			file.save(os.path.join(ROOT_DIR, TEST_DIR, filename))
			success = True
		else:
			errors[file.filename] = 'File type is not allowed'
	if not success:
		resp = jsonify({'message' : 'File upload failed'})
		resp.status_code = 401
		return resp

	trainingNeeded = globalStates.isTrainingBehind(os.path.join(ROOT_DIR, globalStatespath))
	print('trainingNeeded:{}'.format(trainingNeeded))
	if trainingNeeded:
		trainer()
	runTest(
		nameForNumberMap,
		os.path.join(ROOT_DIR,trainResFilePath),
		os.path.join(ROOT_DIR, TEST_DIR, filename),
		os.path.join(ROOT_DIR, DETECT_OUT_DIR, filename),
	)
	if not os.path.isfile(os.path.join(ROOT_DIR, DETECT_OUT_DIR, filename)):
		resp = jsonify({'message' : 'Detection failed'})
		resp.status_code = 401
		return resp
	resp = jsonify({'message' : 'Detected successfull', 'outputUrl': os.path.join(DETECT_OUT_DIR, filename)})
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
		resp = jsonify({'message' : 'No person name in the request'})
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
		globalStates.saveLastUpload(os.path.join(ROOT_DIR, globalStatespath))
		errors['message'] = 'File(s) successfully uploaded'
		resp = jsonify(errors)
		resp.status_code = 206
		return resp
	if success:
		globalStates.saveLastUpload(os.path.join(ROOT_DIR, globalStatespath))
		resp = jsonify({'message' : 'Files successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify(errors)
		resp.status_code = 400
		return resp


if __name__ == "__main__":
    app.run()