import sys
import os
from pathlib import Path


def GetEnv(key, defaultVal=""):
    try:
        return os.environ[key] if key in os.environ else defaultVal
    except Exception as e:
        return defaultVal

def PrinteInternalResource():
    libPath = f"{GetEnv('LIB_PATH')}" + "/PyCompilePackager.pyz"
    location =  str(Path(os.path.dirname(__file__)).absolute())
    package = __package__
    print("Lib Path ->" + libPath)
    sys.path.insert(0,libPath )

     #[Recommended] Use PyCompilePackager's extended ResourceManager to extract any internal resources
    import PyCompilePackager.Core.Resource as RS
    resourceManager = RS.Resource(location,package)
    res = resourceManager.Get('demo.json')
    print(res)
    res = resourceManager.Get('anotherInternal.json','internal_resources')
    print(res)
    res = resourceManager.Get('BuildLevels.png','ASubNamespace/Docs')
    
    #Use Python's normal package manager to extract resources
    import pkgutil
    package = __package__
    print(package)
    #package = "DemoStandAloneApp"
    res = pkgutil.get_data(package, 'demo.json')
    print(res)
    res = pkgutil.get_data(package + '.internal_resources', 'anotherInternal.json')
    print(res)

def Main():
    print('Hello from DemoStandalone App')

    import DemoStandAloneApp.ASubNamespace.Feature1 as F1

    print (F1.MyFeature())

    import DemoStandAloneApp.ASubNamespace.AnotherSubNameSpace.Feature2 as F2

    print (F2.MyFeature2())

    PrinteInternalResource()

    import requests as requests    
    print(str(requests.get("https://www.google.com",verify=False)))

    import numpy as np

    print(np.zeros(2))
    

if __name__ == "__main__":
    if __package__ == "": __package__ = "DemoStandAloneApp"
    
    Main()