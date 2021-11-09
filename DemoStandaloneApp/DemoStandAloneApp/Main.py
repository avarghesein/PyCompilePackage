import os

def PrinteInternalResource():
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