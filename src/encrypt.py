from Crypto.Cipher import AES
from random import choice

choices = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_key(length):
    if length not in [16, 24, 32]:
        raise ValueError, "Number must be 16, 24, or 32"

    # # Create a random key
    return "".join([choice(choices) for _ in range(length)])


def encrypt(key, text, iv):
    # # Get a key and iv if one is not provided.
    if key == "":
        key = get_key(16)

    if iv == "":
        iv = get_key(16)

    # # Check if the key and iv is valid
    if len(key) not in [16, 24, 32]:
        raise ValueError("Key must be 16, 24, or 32 characters long!")

    if len(iv) not in [16, 24, 32]:
        raise ValueError("Iv must be 16, 24, or 32 characters long!")

    # # If the length of the text is not a multiple of 16
    # # Add zeros until it is.
    characters = 0
    if len(text) % 16 != 0:
        characters = 0
        while len(text) % 16 != 0:
            text += "0"
            characters += 1

    # # Create a new AES encryption object and encrypt the text
    obj = AES.new(key, AES.MODE_CFB, iv)
    out = obj.encrypt(text)

    # # If the text is changed, get rid of the extra text
    if characters > 0:
        out = out[0:len(out) - characters]

    return out, key, iv


def decrypt(key, text, iv):
    # # Check the key and iv are correct
    if len(key) not in [16, 24, 32]:
        raise ValueError("Key must be 16, 24, or 32 characters long!")

    if len(iv) not in [16, 24, 32]:
        raise ValueError("Iv must be 16, 24, or 32 characters long!")

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



