import compress
import sys, os
from zlib import decompress as decomp, compress as comp
from zlib import error as zliberror
from zlib import MAX_WBITS
from encrypt import *
from time import sleep

'''TO DO
'''

# # Get the args from the command line
args = sys.argv[1:]

# # Help text
help = '''Self-Extractor
Made by: Alex Strole on 11/9/2017
-----------------------------------------------------------------------------------------------------------
Simple self-extracter program. Takes an inputted file or files and compresses them and then puts that into one file.
Can also encrypt the data in the file with a key and iv. 

Commands:
    -help       Display this message.
    -files      Files to be compressed / file that needs to be decompressed.
    -compress   Compress the files inputted.
        -name       Name for the compressed file to be named. Will default to out if unspecified.
    -decompress Decompress the file inputted.
    -encrypt    Encrypt the files to be compressed. You Should not use this with the decompress option.
        -key        They key to be used to encrypt, If you dont use this option, one will be provided for you.\n If you lose the key you cannot decompress.
    -decrypt    Decrypt the file using a key and an iv. They should be provided.
        -key        The key to be used to decrypt. Required.
        -iv         The iv to be used to decrypt. Required.'
        
    Your key and iv must either be 16, 24, or 32 characters long. Anything else will result in an error.'''


def split_file(files, lengths):
    strings = []
    print(lengths, "split")
    for length in lengths:
        strings.append(files[0:int(length)])
        files = files[int(length):]

    return strings

if __name__ == '__main__':
    # # Display the help menu
    if "-help" in args:
        print(help)
        sys.exit(0)

    # # Getting the files/file to compress
    if "-files" in args or "-file" in args:
        if "-file" in args:
            args[args.index("-file")] = "-files"
        string = args[args.index("-files") + 1].split(",")
        files = []
        names = []
        for file in string:
            file = open(file, 'rb')
            names.append(file.name)
            files.append(file.read())
            file.close()
    else:
        print(help)
        raise ValueError, "At least one file is required"

    # # Check for correct arguments
    if "-encrypt" in args and "-decompress" in args:
        print(help)
        raise ValueError, "Cannot encrypt a file to be decompressed"
    if "-decrypt" in args and "-compress" in args:
        print(help)
        raise ValueError, "Cannot decrypt a file to be compressed"

    if "-compress" in args and "-decompress" in args:
        print(help)
        raise ValueError, "Cannot both decompress and compress"

    if "-compress" not in args and "-decompress" not in args:
        print("What do you want me to do? I cant do anything with those arguments!")
        sleep(2)
        print(help)
        sys.exit(1)

    # # Make an info file with the name and folder data, and compress the text from the files.
    # # Can also optionally encrypt the text
    if "-compress" in args:
        print("Compressing...")
        files, names, lengths = compress.compress(files, names)

        info = open("info", "wb")

        text = comp(str(names) + ":" + str(lengths))
        #text = str(names) + ":" + str(lengths)
        info.write(text)
        info.close()

        # # Encrypt the text
        # # If -key in args use that key instead of a random one
        if "-encrypt" in args:
            print("Encrypting...")
            if "-key" in args:
                key = args[args.index("-key") + 1]
            else:
                key = get_key(16)

            iv = get_key(16)

            names = names.split(",")
            for i in range(len(files)):
                print(names[i] + " is encrypted!")
                files[i], key, iv = encrypt(key, files[i], iv)
            print("Your key is: " + str(key) + " Your iv is: " + str(iv))
            print("Encryption done")

        if "-name" in args:
            out = open(args[args.index("-name") + 1], 'wb')
            for i in range(len(files)):
                out.write(files[i])
        else:
            out = open("out", "wb")
            for i in range(len(files)):
                out.write(files[i])

        out.close()
        print("Completed with no errors!")

    # # Decompress the text and put them into their files.
    # # If needed to decrypt, a key and iv is needed.
    elif "-decompress" in args:
        try:
            info = open("info", "rb").read()
            info = decomp(info, MAX_WBITS|32)
            info = info.split(":")
            names = info[0].split(",")
            lengths = info[1].split(",")
        except zliberror:
            print(help)
            raise ValueError, "Incorrect info file, please recompress or contact the software owner."

        if "-decrypt" in args:
            print("Decrypting..")
            files = split_file(files[0], lengths)
            if "" in files:
                del files[files.index("")]

            if "-iv" in args and "-key" in args:
                iv = args[args.index("-iv") + 1]
                key = args[args.index("-key") + 1]
            else:
                raise ValueError, "Cannot decrypt without a key and iv"
            for i in range(len(files)):
                files[i], key, iv = decrypt(key, files[i], iv)
                print(names[i] + " is decrypted!")

            print("Decrypted")

        else:
            if len(names) > 1:
                print("Split")
                files = split_file(files[0], lengths)

        print("Decompressing...")
        print(len(files[0]))
        for i in range(len(files)):
            files[i] = decomp(files[i], MAX_WBITS|32)
            print(names[i] + " is decompressed!")

        for i in range(len(names)):
            file = open(names[i], "wb")
            file.write(files[i])
            file.close()

        print("Done with no errors!")
