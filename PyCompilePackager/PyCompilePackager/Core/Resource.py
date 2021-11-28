
import os
import re
from pathlib import Path

class Resource:

    def __init__(self, location="",rootPackage=""):
        self.isZip = False
        self.rootNameSpace = None
        self.package = None

        isSelf = not (location != "" or rootPackage != "")

        if rootPackage == "": rootPackage =  __package__

        exp = r'(.+)\..+'
        self.package = re.sub(exp, r'\1', rootPackage)
        
        if location == "": location =  str(Path(os.path.dirname(__file__)).absolute())

        self.isZip = '.pyz' in location

        if self.isZip:            
            exp = r'(.+\.pyz)(.+)'
            self.rootNameSpace = re.sub(exp, r'\1', location)       
        else:
            exp = r'(.+)' + self.package + '.*'
            print("RegX->" + exp)
            self.rootNameSpace = re.sub(exp, r'\1', location)
        
        self.rootNameSpace = self.rootNameSpace.rstrip("/\\")

        print("Root->" + self.rootNameSpace)
        print("Package Root->" + self.package)
        print("Is Zip->" + str(self.isZip))
    
    def IsZip(self):
        return self.isZip

    def GetRootNamespace(self):
        return self.rootNameSpace + "/" + self.package
    
    def Get(self, resource, subNamespace = ""):
        subNamespace = subNamespace.lstrip("/\\").rstrip("/\\").replace("\\","/")

        if subNamespace != "":
            resourcePath = self.package + "/" + subNamespace + "/" + resource
        else:
            resourcePath = self.package + "/" + resource

        if self.isZip:            
            import zipfile
            resourcePath = re.sub('/+', '/', resourcePath)

            print("Resource Path->" + resourcePath)

            try:
                with zipfile.ZipFile(self.rootNameSpace) as z:
                    idx = list(map(str.lower, z.namelist())).index( resourcePath.lower() )
                    if idx < 0 : return None
                    with z.open(z.namelist()[idx]) as f:
                        return f.read()
            except Exception as e:
                return None
        else:
            resourcePath = self.rootNameSpace + "/" + resourcePath
            print("Resource Full Path->" + resourcePath)
            if not os.path.exists(resourcePath): return None

            with open(resourcePath,'rb') as f:
                return f.read()


    def GetPackageResource(self, resource, nameSpace=""):
        import pkgutil
        if nameSpace != "":
            nameSpace = self.package + "." + nameSpace
        else:
            nameSpace = self.package

        print(f"Resource->{nameSpace}.{resource}")
        return pkgutil.get_data(nameSpace, resource)