from sys import argv, exit, stdout
import os
from subprocess import Popen, PIPE, call
from shutil import copy
import cProfile, pstats, StringIO, logging

help = """Folder Util for Coda
________________________________________________________________________________
 # # Syntax:					
 # # 	folder path encrypt=BOOL name=NAME key=KEY iv=KEY
 # # Path =    Where the folder is. If in the current directory just put the name.
 # # encrypt = Encrypt the outputted file or not. Values are True or False.
 # # name =    The name of the file to output.
 # # Key =     Key to encrypt with. Leave blank to have one provided for you.
 # # Iv =      Iv to encrypt with. Leave blank to have one provided for you.
 # # key_len = How long to make the random key, must be 16, 24, or 32
________________________________________________________________________________\n\n"""

try:
    files = os.listdir(argv[1])
except WindowsError:
    logging.info(help)
    logging.info("ERROR -1: Unable to find " + argv[1] + ". Please try again with a path to a folder!")
    exit(-1)

files_with_path = []
logging.basicConfig(format="%(message)s", level=logging.INFO)

for file in files:
    if len(file.split(".")) == 1:
        del files[files.index(file)]
    else:
        files_with_path.append(argv[1] + file)
    #f " " in file:
        #files[files.index(file)] = '"' + file + '"'

for i in range(len(files_with_path)):
    copy(files_with_path[i], os.getcwd())
    logging.info(files[i] + " Copied!")

if len(files) == 0:
    logging.info(help)
    logging.info("ERROR 1: No files found in that folder!")
    exit(1)

files_str = ",".join(files)

if len(argv) >= 3:
    encrypt = argv[2].split("=")[1]
    if encrypt.lower() == "true":
        encrypt = True
    else:
        encrypt = False
else:
    logging.info(help)
    logging.info("ERROR 2: Encryption bool not found!")
    exit(1)
if len(argv) >= 4:
    name = argv[3].split("=")[1]
else:
    loging.info(help)
    logging.info("ERROR 3: Name not found!")
    exit(1)

if len(argv) >= 5:
    key = argv[4].split("=")[1]
else:
    key = ""
if len(argv) >= 6:
    iv = argv[5].split("=")[1]
else:
    iv = ""

if encrypt:
    if key != "" and iv == "":
        call('coda -files ' + "'" + files_str + "'" + " -compress -encrypt -name " + name + " -key " + key)
    elif iv != "" and key == "":
        call('coda -files ' + files_str + " -compress -encrypt -name " + name + " -iv " + iv)
    elif key != "" and iv != "":
        call('coda -files ' + files_str + " -compress -encrypt -name " + name + " -iv " + iv + " -key " + key)
    else:
        call('coda -files ' + files_str + " -compress -encrypt -name " + name)
else:
    call("coda -files " + "'" + files_str + "'" + " -compress -name " + name)

for i in range(len(files)):
    os.remove(files[i])
