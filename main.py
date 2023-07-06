from msilib.schema import File
import os
import zipfile
import argparse
import re


parser=argparse.ArgumentParser(description="Extract file from an archive and convert it to Lucid CSV and Archimate model")
parser.add_argument("filename")
args = parser.parse_args()

toProcess=args.filename

if not zipfile.is_zipfile(toProcess):
    print ("File is not a ZIP")
    exit (1)
workdir="./workdir"

if not os.path.exists(workdir):
   os.mkdir(workdir)
elif not os.path.isdir(workdir):
    print ("File "+workdir+" exists but is not a directory")
    exit(1)

with zipfile.ZipFile(toProcess) as zip:
    zip.extract("dup_import_script.py",workdir)

with open(workdir+"/dup_import_script.py",mode="r") as file:
    data=file.readlines()

newdata=[]
for line in data:
    if re.match("W*from java\.lang.*",line):
        pass
    elif re.match("W*import java.*",line):
        pass
    else:
        newdata.append(line)


import standardFunctions
from standardFunctions import defineExternalRepository
from standardFunctions import EssentialGetInstance
from standardFunctions import addIfNotThere
from standardFunctions import kb
from standardFunctions import Integer
from standardFunctions import dump_Archi
from standardFunctions import dump_Lucid

exec("\n".join(newdata))
 
dump_Lucid(toProcess[:-4])
#dump_Archi(toProcess[:-4])