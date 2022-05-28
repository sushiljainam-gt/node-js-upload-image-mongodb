from datetime import datetime
import json

def nowTime():
    return int(datetime.now().strftime('%s'))

def updateAnyKey(statePath, key, value):
    print('saving '+key+':'+value)
    newText=''
    stateFile = open(statePath, 'r+')
    count = 0
  
    while True:
        line = stateFile.readline()
        
        if line:
            count += 1
            print("Line - {}: {}".format(count, line.strip()))
            key,value=line.strip().split('=',1)
            print("{}: {}".format(key,value))
            if key.strip() == key.strip():
                newText = newText + key + "={}\n".format(str(nt))
            else:
                newText = newText + line
            print('newText so far')
            print(newText)
            print('newText so far')
        else:
            break
    stateFile.close()

    with open(statePath, "w") as f:
        f.write(newText)

def saveLastUpload(statePath):
    updateAnyKey(statePath, 'lastUploadTime', str(nowTime()))

def saveLastTrain(statePath):
    updateAnyKey(statePath, 'lastTrainTime', str(nowTime()))

def isTrainingBehind(statePath):
    print('lastTrainingTime isBefore lastUploadTime')
    json_object = {}
    # Opening JSON file
    with open(statePath, 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
        print(json_object)
        tt = json_object.get('lastTrainTime')
        ut = json_object.get('lastUploadTime')
        # ttt = datetime.strptime(tt)
        # utt = datetime.strptime(ut)
        return bool(int(tt) <= int(ut))


def init(statePath):
    print('init')
    nt = nowTime()
    with open(statePath, 'w') as stateFile:
        stateFile.writelines(("lastUploadTime={}\n".format(str(nt))))
        stateFile.writelines(("lastTrainTime={}\n".format(str(nt))))

