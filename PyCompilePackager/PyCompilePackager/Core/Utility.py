import os
import sys
import json
from datetime import datetime, timedelta

StatusFile = None
LogFile = None
TraceFile = None
BuildConfig = None
MainPackage = None

ProgramPath = None

def GetNowUtc():
    #return (datetime.utcnow().date()+ timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def GetPathFileExtension(file):
    filePath = os.path.split(file)
    filenamewithext = os.path.basename(file)
    filename, ext = os.path.splitext(filenamewithext)
    return filePath[0], filename, ext

def GetJsonAsObject(templatePath):
    from types import SimpleNamespace
    contents = ""
    with open(templatePath) as f:
        contents = f.read()
        
    obj = json.loads(contents, object_hook=lambda d: SimpleNamespace(**d))
    return obj

def GetEnv(key, defaultVal=""):
    try:
        return os.environ[key] if key in os.environ else defaultVal
    except Exception as e:
        Log(e)
        return defaultVal

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def GetJsonVal(file,key, defaultVal = None):
    try:
        jsonObj = json.loads(open(file, 'r').read())
        return jsonObj[key]
    except Exception as e:
        Log(e)
        return defaultVal
     

def WriteStatus(status, exception = None):
    global StatusFile
    try:
        with open(StatusFile, "w") as logFile:
            logFile.write(status)
            if not (exception is None):
                logFile.write(":" + str(exception))

            logFile.close()
            
    except Exception as e:
        self.Log(e)     

def Trace(message):
    try:
        print("Message->" + message)
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(TraceFile, "a") as logFile:
            logFile.write(date + ":" +message +"\n")
            logFile.close()
    except Exception as e:
        self.Log(e) 

def Log(exception):
    try:
        print("Error->" + str(exception))
        import sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        msg=f"{exc_type},{fname},{exc_tb.tb_lineno}"
        print(exc_type, fname, exc_tb.tb_lineno)
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LogFile, "a") as logFile:
            logFile.write(date + ":" + str(exception) + ":" + msg +"\n")
            logFile.close()
    except Exception as e:
        print(e)  