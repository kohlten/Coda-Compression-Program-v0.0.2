import zlib, sys
from Crypto.Cipher import AES


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


def split_file(files, lengths):
    strings = []
    for length in lengths:
        strings.append(files[0:int(length)])
        files = files[int(length):]

    return strings


# # Get the args from the command line
args = sys.argv

if __name__ == "__main__":
    # # If -name in args, use that name. Otherwise use "out".
    if "-name" in args:
        name = args[args.index("-name") + 1]
    else:
        name = "out"

    # # Open the compressed file and the info file
    text = open(name, "rb").read()
    
    if "-key" in args or "-iv" in args:
        args.append("-decrypt")

    # # Decompress the info and decompress the file names
    # # If the info file is corrupt don't continue
    try:
        info = open("info", "rb").read()
        info = zlib.decompress(info, zlib.MAX_WBITS|32)
        info = info.split(":")
        names = info[0].split(",")
        lengths = info[1].split(",")
    except zlib.error:
        raise ValueError, "Incorrect info file, please recompress or contact the software owner."

    # # Split the text by length
    text = split_file(text, lengths)

    # # Decrypt the text using a key and iv
    if "-decrypt" in args:
        print("Decrypting..")
        if "-key" in args:
            key = args[args.index("-key") + 1]
        if "-iv" in args:
            iv = args[args.index("-iv") + 1]

        for i in range(len(text)):
            text[i], key, iv = decrypt(key, text[i], iv)

    # # Try to decompress the text
    print("Decompressing...")

    try:
        for i in range(len(text)):
            text[i] = zlib.decompress(text[i], zlib.MAX_WBITS|32)
    except zlib.error:
        print("Failed! Are you sure the file isn't encrypted? If it isn't it might be corrupt!")
        sys.exit(1)

    # # Write the text to the associated files
    for i in range(len(names)):
        file = open(names[i], "wb")
        file.write(text[i])
        file.close()

    print("Done without any errors")
