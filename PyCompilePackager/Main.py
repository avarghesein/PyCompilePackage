import os
import Core.Builder as BLD
import Core.Utility as UTL

def Main():
    UTL.ProgramPath = f"{UTL.GetEnv('BUILD_CONFIG')}"

    if not os.path.exists(UTL.ProgramPath): 
        UTL.ProgramPath = UTL.get_script_path()
        UTL.BuildConfig = UTL.GetJsonAsObject(f"{UTL.ProgramPath}\\BuildConfig.json")
    else:
        UTL.BuildConfig = UTL.GetJsonAsObject(UTL.ProgramPath)
        UTL.ProgramPath,_,_ = UTL.GetPathFileExtension(UTL.ProgramPath)
        
    ProgramPath = UTL.ProgramPath

    UTL.LogFile = f"{ProgramPath}/Log.txt"
    UTL.TraceFile = f"{ProgramPath}/Trace.txt"
    UTL.StatusFile = f"{ProgramPath}/Status.txt"

    try:
        BLD.BuildAll()
    except Exception as e:
        UTL.Log(e)

if __name__ == "__main__":
    Main()