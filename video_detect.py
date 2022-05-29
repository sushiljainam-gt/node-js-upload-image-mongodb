import os
from flask import Flask, Response
import cv2
from faceRec.tester import reuseTrainingData
from setproctitle import setproctitle, getproctitle

print('old:',getproctitle())
setproctitle('aish_video_detect')
print('new:',getproctitle())

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
trainResFilePath = 'trainingSaved.yml'
jsonFilePath = 'trainDataMap.txt'


file1 = open(os.path.join(ROOT_DIR, jsonFilePath), 'r+')
count = 0
resName = 'unknown'
dictName = {}

while True:
    line = file1.readline()

    if not line:
        break
    count += 1
    print("Line{}: {}".format(count, line.strip()))
    name,nameNum=line.strip().split('=',1)
    print("{}: {}".format(name,nameNum))
    dictName[int(nameNum)] = name

file1.close()
print(dictName)
# return resName


app = Flask(__name__)
video = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier()
face_cascade.load(cv2.samples.findFile("faceRec/HaarCascade/haarcascade_frontalface_default.xml"))

@app.route('/')
def index():
    return "Default Message"

def gen(video):
    face_recognizer = reuseTrainingData(os.path.join(ROOT_DIR,trainResFilePath))
    while True:
        success, image = video.read()
        frame_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.equalizeHist(frame_gray)

        faces = face_cascade.detectMultiScale(frame_gray,scaleFactor=1.32,minNeighbors=5) # some params are copied from prev code

        for (x, y, w, h) in faces:
            center = (x + w//2, y + h//2)
            cv2.putText(
                image,
                "X: " + str(center[0]) + " Y: " + str(center[1]),
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                3)
            image = cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

            faceROI = frame_gray[y:y+h, x:x+w]
            label,confidence=face_recognizer.predict(faceROI)
            print('label:',label)
            preName = dictName[label]
            print('name:',preName)
            cv2.putText(
                image,
                "confidence: "+str(round(100 - confidence if confidence < 100 else 0, 2)),
                (50, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                3)
            if confidence < 50:
                cv2.putText(image,preName,(x,y),cv2.FONT_HERSHEY_DUPLEX,2,(255,0,0),4)
        ret, jpeg = cv2.imencode('.jpg', image)

        frame = jpeg.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2204, threaded=True)