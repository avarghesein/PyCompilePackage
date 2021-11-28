import os
from shutil import rmtree
import sys
from pathlib import Path
import zipfile

def Main():
    location =  str(Path(os.path.dirname(__file__)).absolute())
    location = location.replace( str(__package__) + ".pyz","")
    location = location.replace(__package__,"")
    print("Zip Location:" +  location + "\n\n")

    venv = f"{location}/.venv/<<GUILD>>"

    print("Virtual Environment:" +  venv + "\n\n")

    if not os.path.exists(venv):
        venvRoot = f"{location}/.venv"
        if os.path.exists(venvRoot): rmtree(venvRoot)
        os.makedirs(venv, exist_ok=True)

        import re
        exp = r'(.+\.pyz).*'
        zipFileLocation = re.sub(exp, r'\1', os.path.dirname(__file__))

        print("Opening Zip File->" + zipFileLocation)

        with zipfile.ZipFile(zipFileLocation) as zf:
            zf.extractall(venv)

    sys.path.insert(0,venv)

    <<namespace>>
    <<main>>