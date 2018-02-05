from time import sleep, time
import sys, os
from encrypt import *
import compress, pylzma
import cPickle

start_time = time()
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
    -files      Files to be compressed. For decompression, Coda will try to find the .coda file in the current folder.
    -compress   Compress the files inputted.
        -name       Name for the compressed file to be named. Will default to out if unspecified.
    -decompress Decompress the file inputted.
    -encrypt    Encrypt the files to be compressed. You Should not use this with the decompress option.
        -key        The key to be used to encrypt, If you dont use this option, one will be provided for you. If you lose the key you cannot decompress.
        -iv         The iv used to encrypt, If you dont use this option, a random one will be provided for you. If you lose the iv you cannot decompress.
        -key_len    The length of the key and iv to be provided. Must be 16, 24, or 32. Only use this option if not providing a key.
    -decrypt    Decrypt the file using a key and an iv. They should be provided.
        -key        The key to be used to decrypt. Required.
        -iv         The iv to be used to decrypt. Required.'
        
    Your key and iv must either be 16, 24, or 32 characters long. Anything else will result in an error.
    It is also not reccomended to use the same key and iv. It can result in errors.
    Encryption can cause a small loss of data rarely. Be warned. I am not to blame for any lost files.'''


def split_file(files, lengths):
    strings = []
    print(lengths, "split")
    for length in lengths:
        strings.append(files[0:int(length)])
        files = files[int(length):]

    return strings

accepted_values = ["-compress", "-decompress", "-help", "-files", "-name", "-key", "-iv", "-key_len", "-encrypt", "-decrypt", "-file"]


def check_for_args():
    if "-help" in args:
        print(help)
        sys.exit(0)
    for arg in args:
        if ("-" == arg[0] and arg not in accepted_values): #or ("-files" not in args and "-name" not in args and arg not in accepted_values):
            print(help)
            print("Error -1: " + arg + " is not a recognized value!")
            sys.exit(1)
    if "-encrypt" in args and "-decompress" in args:
        print(help)
        raise ValueError("Cannot encrypt a file to be decompressed")
    if "-decrypt" in args and "-compress" in args:
        print(help)
        raise ValueError("Cannot decrypt a file to be compressed")

    if "-compress" in args and "-decompress" in args:
        print(help)
        raise ValueError("Cannot both decompress and compress")

    if "-compress" not in args and "-decompress" not in args:
        print("What do you want me to do? I cant do anything with those arguments!")
        sleep(2)
        print(help)
        sys.exit(1)


def get_files():
    files = []
    names = []
    if "-files" in args:
        string = args[args.index("-files") + 1].split(",")

        if "-compress" in args:
            for file in string:
                file = open(file, 'rb')
                names.append(file.name)
                files.append(file.read())
                file.close()
        else:
            raise ValueError("ERROR 1: Only use this this option for compression. Or -compression not found in args.")
    elif "-name" not in args and "-files" not in args:
        string = []
        for file_name in os.listdir(os.getcwd()):
            if len(file_name.split(".")) > 1 and file_name.split(".")[1] == "coda":
                print("Found! " + file_name)
                string.append(file_name)
                break
        if len(string) > 0:
            files = open(string[0], 'rb')
            names.append(files.name)
        else:
            print(help)
            raise ValueError("ERROR -2: Could not find a coda file! " + ' '.join(os.listdir(os.getcwd())))
    elif "-files" not in args:
        files = open(args[args.index("-name") + 1], 'rb')
        names.append(files.name)
    else:
        raise ValueError("Error -1: No files specifed!")

    return files, names


def compress_files(files, names):
    print("Compressing...")
    files, names = compress.compress(files, names)

    # # Encrypt the text
    # # If -key in args use that key instead of a random one
    names = names.split(',')
    if "-encrypt" in args:
        print("Encrypting...")
        if "-key_len" in args:
            key_len = int(args[args.index("-key_len") + 1])
        else:
            key_len = 16
        if "-key" in args:
            key = args[args.index("-key") + 1]
        else:
            key = get_key(key_len)
        if "-iv" in args:
            iv = args[args.index("-iv") + 1]
        else:
            iv = get_key(key_len)

        for i in range(len(files)):
            print(names[i] + " is encrypted!")
            files[i], key, iv = encrypt(key, files[i], iv)
        for i in range(len(names)):
            names[i], key, iv = encrypt(key, names[i], iv)
        print("Your key is: " + str(key) + " Your iv is: " + str(iv))
        print("Encryption done")

    # #Dump the files into a pickle file
    if "-name" in args:
        out = open(args[args.index("-name") + 1] + ".coda", 'wb')
    else:
        out = open("out" + ".coda", "wb")

    arrays = [files, [pylzma.compress(','.join(names))]]
    cPickle.dump(arrays, out, protocol=2)

    out.close()
    print("Completed with no errors!")


def decompress_file(files):
    pickle_in = cPickle.load(files)
    names = pylzma.decompress(pickle_in[1][0]).split(",")
    files = pickle_in[0]

    if "-decrypt" in args:
        print("Decrypting..")

        if "-iv" in args and "-key" in args:
            iv = args[args.index("-iv") + 1]
            key = args[args.index("-key") + 1]
        else:
            raise ValueError("Cannot decrypt without a key and iv")
        for i in range(len(names)):
            names[i], key, iv = decrypt(key, names[i], iv)
        for i in range(len(files)):
            files[i], key, iv = decrypt(key, files[i], iv)
            print(names[i] + " is decrypted!")

        print("Decrypted")

    print("Decompressing...")
    try:
        for i in range(len(files)):
            files[i] = pylzma.decompress(files[i])
            print(names[i] + " is decompressed!")
    except:
        raise Exception("Unable to decompress. Are you sure it isnt encrypted?")

    for i in range(len(names)):
        file = open(names[i], "wb")
        file.write(files[i])
        file.close()

if __name__ == '__main__':
    # # Check for correct arguments
    check_for_args()

    # # Getting the files/file to compress
    files, names = get_files()

    # # Take the files and compress them. If -encrypt in args, encrypt them with a key and iv.
    # # Info of the files will also be stored.
    if "-compress" in args:
        compress_files(files, names)

    # # Decompress the text and put them into their files.
    # # If needed to decrypt, a key and iv is needed.
    elif "-decompress" in args:
        decompress_file(files)

    print("Done with no errors!")
    print("Took " + str(time() - start_time) + " Seconds!")
