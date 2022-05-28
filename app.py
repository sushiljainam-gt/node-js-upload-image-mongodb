from flask import Flask

UPLOAD_FOLDER = 'trainingImagesPython'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEST_DIR'] = 'testImages'
app.config['DETECT_OUT_DIR'] = 'detectOutDir'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024