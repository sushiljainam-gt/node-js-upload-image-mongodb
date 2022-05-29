import cv2
import os
import numpy as np
import faceRec.faceRecognition as fr

def prepareTest(imgPath):
    #This module takes images  stored in diskand performs face recognition
    # test_img=cv2.imread('TestImages/pri.webp')#test_img path
    # test_img=cv2.imread('TestImages/sati.jpeg')#test_img path
    # test_img=cv2.imread('TestImages/Kangana.jpg')#test_img path
    # test_img=cv2.imread('TestImages/kan.webp')#test_img path
    # test_img=cv2.imread('TestImages/pr.jpg')#test_img path
    test_img=cv2.imread(imgPath)#test_img path
    faces_detected,gray_img=fr.faceDetection(test_img)
    print("faces_detected:",faces_detected)
    return test_img,faces_detected,gray_img


def trainingFn(trainingImageDirPath, trainDataSavePath):
    #Comment belows lines when running this program second time.Since it saves training.yml file in directory
    faces,faceID=fr.labels_for_training_data(trainingImageDirPath)
    face_recognizer=fr.train_classifier(faces,faceID)
    face_recognizer.write(trainDataSavePath)
    return face_recognizer

def reuseTrainingData(trainDataSavePath):
    #Uncomment below line for subsequent runs
    face_recognizer=cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read(trainDataSavePath)#use this to load training data for subsequent runs
    return face_recognizer

def runTest(nameGetter, trainDataSavePath, inputImgPath, imgOutPath):
    # name={0:"P",1:"K"}#creating dictionary containing names for each label
    test_img,faces_detected,gray_img = prepareTest(inputImgPath)
    face_recognizer = reuseTrainingData(trainDataSavePath)
    names=[]
    for face in faces_detected:
        (x,y,w,h)=face
        roi_gray=gray_img[y:y+h,x:x+h]
        label,confidence=face_recognizer.predict(roi_gray)#predicting the label of given image
        print("confidence:",confidence)
        print("label:",label)
        predicted_name=nameGetter(label)
        print("name:",predicted_name)
        fr.draw_rect(test_img,face)
        # if(confidence!=96.98802546113127):#If confidence more than 37 then don't print predicted face text on screen
        #     continue
        fr.put_text(test_img,predicted_name,x,y)
        names.append({'name':predicted_name,'confidence':("{:.2f}".format(100-confidence) if confidence < 100 else 0) })

    resized_img=cv2.resize(test_img,(1000,1000))
    cv2.imwrite(imgOutPath, resized_img)
    return names
    # return resized_img.
    # cv2.imshow("face dtecetion tutorial",resized_img)
    # cv2.waitKey(0)#Waits indefinitely until a key is pressed
    # cv2.destroyAllWindows





