import compileall
import PyCompilePackager.Core.Utility as UTL
import os
from pathlib import Path
from shutil import copy, copyfile, rmtree
from distutils.dir_util import copy_tree
import fnmatch
import zipapp


def Shell(s):
    import subprocess
    return subprocess.check_output(s,shell=True)

def RemovePyCaches(srcDir):
    foldersToCleanup = []

    def FindSourceObjFiles(rootDir):
        for root, dirs, files in os.walk(rootDir):
            for dir in dirs:
                if(dir.endswith("__pycache__")): 
                    foldersToCleanup.append(f"{root}/{dir}")                    
                else:
                    FindSourceObjFiles(f"{root}/{dir}")             

    FindSourceObjFiles(srcDir)    

    for folder in foldersToCleanup: 
        try:
            rmtree(folder)
        except Exception as e:
            pass

def RemoveSourceObjectFiles(srcDir):
    filesToCleanup = []
    foldersToCleanup = []

    def FindSourceObjFiles(rootDir):
        for root, dirs, files in os.walk(rootDir):
            for dir in dirs:
                if(dir.endswith("__pycache__")): 
                    foldersToCleanup.append(f"{root}/{dir}")                    
                else:
                    FindSourceObjFiles(f"{root}/{dir}")

            for file in fnmatch.filter(files, "*.py"):
                filesToCleanup.append(f"{root}/{file}")
               

    FindSourceObjFiles(srcDir)

    for file in filesToCleanup: 
        try:
            os.remove(file)
        except Exception as e:
            pass        

    for folder in foldersToCleanup: 
        try:
            rmtree(folder)
        except Exception as e:
            pass


def IsSrcCopy():
    if not hasattr(UTL.BuildConfig, "NO_COMPILE") : return False
    return UTL.BuildConfig.NO_COMPILE == "YES"

def Compile(srcDir, dstDir, dstRoot, buildLevel, objFiles, isPipPackagesCompile=False):
    print("SKIP DIRS->" + UTL.BuildConfig.SKIP_DIRS)
    # Perform same compilation, excluding files in .svn directories.
    import re

    if not IsSrcCopy():
        compileall.compile_dir(srcDir, rx=re.compile(UTL.BuildConfig.SKIP_DIRS), force=True, maxlevels=buildLevel, ddir=dstDir)

    if not os.path.exists(dstDir): os.makedirs(dstDir, exist_ok=True)

    def GetCompiledFiles(rootDir):
        for root, dirs, files in os.walk(rootDir):
            for dir in dirs:
                GetCompiledFiles(f"{root}/{dir}")

            for file in fnmatch.filter(files, "*.pyc" if not IsSrcCopy() else "*.py"):
                yield f"{root}/{file}" 

    for compileFile in GetCompiledFiles(srcDir):
        srcFile = compileFile

        if not isPipPackagesCompile:
            if dstRoot in srcFile:
                continue

        dstFile = srcFile.replace(srcDir,dstDir)
        dstFile = dstFile.replace("__pycache__","")

        dstPath,_,_ = UTL.GetPathFileExtension(dstFile)
        if not os.path.exists(dstPath): os.makedirs(dstPath, exist_ok=True)

        import re
        dstFile = re.sub('\.cpython.+\.pyc', '.pyc', dstFile)
        for objFileName in objFiles:
            if objFileName in dstFile:
                dstFile = dstFile.replace(objFileName,".pyc")                

        if os.path.exists(dstFile): os.remove(dstFile)
        copyfile(srcFile, dstFile)

def BuildAll():

    buildCfg = UTL.BuildConfig

    import re
    buildCfg.SKIP_DIRS = re.sub(r'([\\/])', r'[/\\\\]',buildCfg.SKIP_DIRS)
    buildCfg.SKIP_DIRS = re.sub(r'([.+*]+)', r'\\\1',buildCfg.SKIP_DIRS)    
    buildCfg.SKIP_DIRS = "|".join([ f"({token})" for token in buildCfg.SKIP_DIRS.split(",") ])

    UTL.BuildConfig = buildCfg

    srcDir = str(Path(buildCfg.SRC_DIR).absolute())
    dstDir = str(Path(buildCfg.BLD_DIR).absolute())

    dstRoot = dstDir
    dstPreCompiled = dstDir + "/CompiledCache/"
    dstOut = dstDir + "/OUTPUT/"    
    dstDir += "/OBJ/"    

    if os.path.exists(dstDir):  rmtree(dstDir)     
    if os.path.exists(dstOut):  rmtree(dstOut)

    os.makedirs(dstDir, exist_ok=True)
    os.makedirs(dstOut, exist_ok=True)
    
    UTL.Trace("Copying Resources")

    def CopyResource(srcResource, dstDir, resource):
        src = srcResource
        dst = dstDir

        if os.path.isdir(src):
           dst = f"{dst}/{resource}"
           copy_tree(src, dst)
           return
       
        _,file,ext = UTL.GetPathFileExtension(src)

        if resource == "":
            dst = f"{dst}/{file}{ext}"
        else:
            dst = f"{dst}/{resource}"

        if os.path.exists(dst): os.remove(dst)
        dstPath,_,_ = UTL.GetPathFileExtension(dst)
        if not os.path.exists(dstPath): os.makedirs(dstPath, exist_ok=True)
        copyfile(src, dst) 
            
    bootStrapFile = f"{srcDir}/{buildCfg.PACKAGE_NAME}/Bootstrap.py"
    bootStrapCachedFile = f"{dstPreCompiled}/Bootstrap.py"

    for resource in buildCfg.INTERNAL_RESOURCES:
        src = f"{srcDir}/{resource[0]}"
        CopyResource(src,dstDir, resource[1])

        if "requirements.txt" in resource[0]:
            UTL.Trace("Copying Dependencies.This may take a while...")

            dstRequirements = f"{dstPreCompiled}/requirements.txt"
            dstCompiledCache = dstPreCompiled + "/Cache"

            if os.path.exists(dstRequirements) and os.path.exists(dstCompiledCache):
                import filecmp
                result = filecmp.cmp(src, dstRequirements,shallow=False)
                if result == True:
                    copy_tree(dstCompiledCache, dstDir)                    
                    UTL.Trace("Reusing Compiled/Package Cache")
                    continue
            
            UTL.Trace("Building Compiled/Package Cache.This may take a while...")
            if os.path.exists(bootStrapCachedFile):  os.remove(bootStrapCachedFile)
            CopyResource(src,dstPreCompiled, resource[1])
            dstCompiledTmp = dstPreCompiled + "/TMP"
            dstTmpPackages = f"{dstCompiledTmp}/packages"
            if os.path.exists(dstCompiledTmp):  rmtree(dstCompiledTmp)
            if not os.path.exists(dstTmpPackages): os.makedirs(dstTmpPackages, exist_ok=True)

            Shell(f"python -m pip install -r {src} --target {dstTmpPackages}")

            for root, dirs, files in os.walk(dstTmpPackages):
                for dir in dirs:
                    if (dir.endswith("dist-info")): rmtree(f"{root}/{dir}")

            if buildCfg.PRE_COMPILE_REQUIREMENTS == "YES":
                Compile(dstTmpPackages, dstCompiledCache, dstPreCompiled,20,buildCfg.RENAME_OBJ_FILES, True)
                RemoveSourceObjectFiles(dstTmpPackages)
                copy_tree(dstTmpPackages, dstCompiledCache)
            else:
                copy_tree(dstTmpPackages, dstCompiledCache)

            rmtree(dstTmpPackages)
            
            copy_tree(dstCompiledCache, dstDir)

            UTL.Trace("Copying Resources")
   
    for resource in buildCfg.RESOURCES:
        src = f"{srcDir}/{resource[0]}"
        CopyResource(src,dstOut, resource[1])  

    def AddBootStrap():
        if buildCfg.EXTRACT_REQUIREMENTS == "YES":            
            if os.path.exists(bootStrapCachedFile):
                copyfile(bootStrapCachedFile, bootStrapFile)
                UTL.Trace("Adding Bootstrapper")
                buildCfg.ENTRY_POINT = f"{buildCfg.PACKAGE_NAME}.Bootstrap:Main"
                return
                
            import pkgutil
            package = UTL.MainPackage
            res = pkgutil.get_data(package + '.Template', 'Bootstrap.py.tpl').decode("utf-8")
            entryPackage = buildCfg.ENTRY_POINT
            entryPackage = entryPackage.split(":")[0]
            res = res.replace("<<namespace>>",f"import {entryPackage}")
            entryPoint = buildCfg.ENTRY_POINT
            entryPoint = entryPoint.replace(":",".") + "()"
            res = res.replace("<<main>>",entryPoint)            
            import uuid
            venv = uuid.uuid4().hex
            res = res.replace("<<GUILD>>",venv)
            with open(bootStrapFile, "w") as bootstrapPy:
                content = res
                bootstrapPy.write(content)
                bootstrapPy.close()

            UTL.Trace("Adding Bootstrapper")
            buildCfg.ENTRY_POINT  = f"{buildCfg.PACKAGE_NAME}.Bootstrap:Main"
            copyfile(bootStrapFile,bootStrapCachedFile)
        else:
            UTL.Trace("Skipping Bootstrapper")

    UTL.Trace("Source Compilation Started")   
    RemovePyCaches(srcDir)
    UTL.Trace("Removed Old Pyc files")
    AddBootStrap()
    UTL.Trace("Processed Bootstrap")
    Compile(srcDir, dstDir, dstRoot,buildCfg.BLD_LEVEL,buildCfg.RENAME_OBJ_FILES)    
    if os.path.exists(bootStrapFile): os.remove(bootStrapFile)

    UTL.Trace("Building Package")
    zipapp.create_archive(dstDir + "/", f"{dstOut}/{buildCfg.PACKAGE_NAME}.pyz",compressed=True,main=buildCfg.ENTRY_POINT)

    if buildCfg.CLEANUP_OBJ_FILES == "YES":
        UTL.Trace("Cleaning up")
        for filename in os.listdir(dstDir):
            if filename.endswith(".pyc"): 
                os.remove(f'{dstDir}/{filename}')
    
        rmtree(dstDir)