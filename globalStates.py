from datetime import datetime
import json

def nowTime():
    return int(datetime.now().strftime('%s'))

def updateAnyKey(statePath, fkey, fvalue):
    print('saving '+fkey+':'+fvalue)
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
            if key.strip() == fkey.strip():
                newText = newText + fkey + "=" + fvalue + "\n"
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

    stateFile = open(statePath, 'r+')
    count = 0
    tt = 0
    ut = 0
    while True:
        line = stateFile.readline()
        
        if line:
            count += 1
            print("Line - {}: {}".format(count, line.strip()))
            key,value=line.strip().split('=',1)
            print("{}: {}".format(key,value))
            if key.strip() == 'lastUploadTime':
                ut = int(value)
            if key.strip() == 'lastTrainTime':
                tt = int(value)
        else:
            break
    stateFile.close()
    ttt = datetime.strptime(tt)
    utt = datetime.strptime(ut)
    return bool(int(ttt) <= int(utt))


def init(statePath):
    print('init')
    nt = nowTime()
    with open(statePath, 'w') as stateFile:
        stateFile.writelines(("lastUploadTime={}\n".format(str(nt))))
        stateFile.writelines(("lastTrainTime={}\n".format(str(nt))))

