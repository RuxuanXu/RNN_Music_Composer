import os
import glob

def createDir(di):
    try:
        if not os.path.exists(di):
            os.makedirs(di)
    except OSError:
        print ('Error: Failed to create directory ' +  di)
        return 0

def readDir(di):
    training_data = glob.glob(di)
    if training_data==[]:
        print('Error: There is no file in directory ' + di)
        return 0
    return training_data

def getName(fp):
    return os.path.basename(fp)