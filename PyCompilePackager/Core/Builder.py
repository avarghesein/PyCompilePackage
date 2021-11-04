import compileall
import Core.Utility as UTL
import os
from pathlib import Path
from shutil import copyfile, rmtree
from distutils.dir_util import copy_tree
import fnmatch
import zipapp


def Shell(s):
    import subprocess
    return subprocess.check_output(s,shell=True)

def BuildAll():

    buildCfg = UTL.BuildConfig

    srcDir = str(Path(buildCfg.SRC_DIR).absolute())
    dstDir = str(Path(buildCfg.BLD_DIR).absolute())
    if os.path.exists(dstDir):  rmtree(dstDir)
    dstRoot = dstDir    
    dstDir += "/OBJ/"
    UTL.Trace("Compilation Started")
    # Perform same compilation, excluding files in .svn directories.
    import re
    compileall.compile_dir(srcDir, rx=re.compile(r'[//][.]svn'), force=True, maxlevels=buildCfg.BLD_LEVEL, ddir=dstDir)

    if not os.path.exists(dstDir): os.makedirs(dstDir, exist_ok=True)

    def GetCompiledFiles(rootDir):
        for root, dirs, files in os.walk(rootDir):
            for dir in dirs:
                GetCompiledFiles(f"{root}/{dir}")

            for file in fnmatch.filter(files, "*.pyc"):
                yield f"{root}/{file}" 

    for compileFile in GetCompiledFiles(srcDir):
        srcFile = compileFile

        if dstRoot in srcFile:
             continue

        dstFile = srcFile.replace(srcDir,dstDir)
        dstFile = dstFile.replace("__pycache__","")

        dstPath,_,_ = UTL.GetPathFileExtension(dstFile)
        if not os.path.exists(dstPath): os.makedirs(dstPath, exist_ok=True)

        import re
        dstFile = re.sub('\.cpython.+\.pyc', '.pyc', dstFile)
        for objFileName in buildCfg.RENAME_OBJ_FILES:
            if objFileName in dstFile:
                dstFile = dstFile.replace(objFileName,".pyc")
                

        if os.path.exists(dstFile): os.remove(dstFile)
        copyfile(srcFile, dstFile)

    UTL.Trace("Copying Resources")
    for resource in buildCfg.COPY_RESOURCES:
        src = f"{srcDir}/{resource[0]}"

        if os.path.isdir(src):
            for dst in [dstDir, dstRoot]:
                dst = f"{dst}/{resource[1]}"
                copy_tree(src, dst)

       
        for dst in [dstDir, dstRoot]:        
            _,file,ext = UTL.GetPathFileExtension(src)

            if resource[1] == "":
                dst = f"{dst}/{resource[1]}/{file}{ext}"
            else:
                dst = f"{dst}/{resource[1]}"

            if os.path.exists(dst): os.remove(dst)
            dstPath,_,_ = UTL.GetPathFileExtension(dst)
            if not os.path.exists(dstPath): os.makedirs(dstPath, exist_ok=True)
            copyfile(src, dst)
    
    UTL.Trace("Building Package")
    zipapp.create_archive(dstDir + "/", f"{dstRoot}/{buildCfg.PACKAGE_NAME}.pyz",compressed=True,main=buildCfg.ENTRY_POINT)

    if buildCfg.CLEANUP_OBJ_FILES == "YES":
        UTL.Trace("Cleaning up")
        for filename in os.listdir(dstDir):
            if filename.endswith(".pyc"): 
                os.remove(f'{dstDir}/{filename}')
    
        rmtree(dstDir)
