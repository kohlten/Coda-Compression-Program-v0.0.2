from time import time

start_time = time()

import pylzma, sys, os
from Crypto.Cipher import AES
import cPickle



def decrypt(key, text, iv):
    # # Check the key and iv are correct
    if len(key) not in [16, 24, 32]:
        raise ValueError, "Key must be 16, 24, or 32 characters long!"

    if len(iv) not in [16, 24, 32]:
        raise ValueError, "Iv must be 16, 24, or 32 characters long!"

    # # If the length of the text is not a multiple of 16
    # # Add zeros until it is
    characters = 0
    if len(text) % 16 != 0:
        text += "0"
        characters += 1

    # # Create a new encryption object and decrypt the text
    obj = AES.new(key, AES.MODE_CFB, iv)
    out = obj.decrypt(text)

    # # If the text is changed, get rid of the extra text
    if characters > 0:
        out = out[0:len(out) - characters]

    return out, key, iv

# # Get the args from the command line
args = sys.argv

help = """Extract tool for Coda
Meant to be used alongside a download to extract the files.
__________________________________________________________________
# # Syntax:
# #     extract -name name -decrypt -key -iv
# # All options are optional as long as the file is named out.
# # name = The name of the compressed file to extract, if not specified will try to find one
# # -decrypt = Use this option if the compressed file is encrypted
# #     -key = The key for the encrypted files
# #     -iv = The iv for the encrypted files
# # BOTH the key and iv are required to decrypt the files.
__________________________________________________________________"""

"TO DO"
# # -extract_location = The place to put the files when done"

if __name__ == "__main__":
    # # Display the help
    if "-help" in args:
        print(help)
        sys.exit(0)

    # # If -name in args, use that name. Otherwise use "out".
    name = ""
    if "-name" in args:
        name = args[args.index("-name") + 1]
    else:
        for file_name in os.listdir(os.getcwd()):
            print(file_name)
            if len(file_name.split(".")) > 1 and file_name.split(".")[1] == "coda":
                print("Found!")
                name = file_name

    if name == "":
        print("ERROR 2: Unable to find a coda file.")
        sys.exit(2)
    # # Open the compressed file and the info file
    try:
        pickle_in = open(name, "rb")
    except IOError:
        print(help)
        print("ERROR -1: Unable to open the file.")
        sys.exit(-1)

    # # Decompress the info and decompress the file names
    # # If the info is corrupt don't continue
    pickle_in = cPickle.load(pickle_in)
    try:
        names = pylzma.decompress(pickle_in[1][0]).split(",")
    except:
        print("Unable to get info, is your file corrupt?")

    files = pickle_in[0]

    # # Decrypt the text using a key and iv
    if "-decrypt" in args:
        print("Decrypting..")
        if "-iv" in args and "-key" in args:
            iv = args[args.index("-iv") + 1]
            key = args[args.index("-key") + 1]
        else:
            print(help)
            raise ValueError, "Cannot decrypt without a key and iv"
        for i in range(len(names)):
            names[i], key, iv = decrypt(key, names[i], iv)
        for i in range(len(files)):
            files[i], key, iv = decrypt(key, files[i], iv)

    # # Try to decompress the text
    print("Decompressing...")

    try:
        for i in range(len(files)):
            files[i] = pylzma.decompress(files[i])
            print(names[i] + " is decompressed!")
    except:
        print(help)
        print("Failed! Are you sure the file isn't encrypted? If it isn't it might be corrupt!")
        sys.exit(1)

    # # Write the text to the associated files
    for i in range(len(names)):
        file = open(names[i], "wb")
        file.write(files[i])
        file.close()

    print("Took " + str(time() - start_time) + " Seconds!" + "\nDone without any errors")
