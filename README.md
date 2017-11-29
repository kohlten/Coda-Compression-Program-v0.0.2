# Coda Compression Program v0.0.2

Self-Extractor
Made by: Alex Strole on 11/9/2017
-----------------------------------------------------------------------------------------------------------
Simple self-extracter program. Takes an inputted file or files and compresses them and then puts that into one file.
Can also encrypt the data in the file with a key and iv. 

Commands:
*    -help       Display this message.
*    -files      Files to be compressed / file that needs to be decompressed. For decompression, if left out will try to find the file in the current folder.
*    -compress   Compress the files inputted.
*        -name       Name for the compressed file to be named. Will default to out if unspecified.
*    -decompress Decompress the file inputted.
*   -encrypt    Encrypt the files to be compressed. You Should not use this with the decompress option.
*        -key        The key to be used to encrypt, If you dont use this option, one will be provided for you. If you lose the key you cannot decompress.
*        -iv         The iv used to encrypt, If you dont use this option, a random one will be provided for you. If you lose the iv you cannot decompress.
*        -key_len    The length of the key and iv to be provided. Must be 16, 24, or 32. Only use this option if not providing a key.
*    -decrypt    Decrypt the file using a key and an iv. They should be provided.
*        -key        The key to be used to decrypt. Required.
*        -iv         The iv to be used to decrypt. Required.'
        
    Your key and iv must either be 16, 24, or 32 characters long. Anything else will result in an error.
    It is also not reccomended to use the same key and iv. It can result in errors.
    Encryption can cause a small loss of data rarely. Be warned. I am not to blame for any lost files.

Extract tool for Coda

Meant to be used alongside a download to extract the files.
__________________________________________________________________
*  Syntax:
*      extract -name name -decrypt -key -iv
*  All options are optional as long as the file is named out.
*  name = The name of the compressed file to extract, if not specified will try to find one
*  -decrypt = Use this option if the compressed file is encrypted
*      -key = The key for the encrypted files
*      -iv = The iv for the encrypted files
*  BOTH the key and iv are required to decrypt the files.
__________________________________________________________________

Folder Util for Coda
________________________________________________________________________________
 *  Syntax:					
 *  	folder path encrypt=BOOL name=NAME key=KEY iv=KEY
 *  Path =    Where the folder is. If in the current directory just put the name.
 *  encrypt = Encrypt the outputted file or not. Values are True or False.
 *  name =    The name of the file to output.
 *  Key =     Key to encrypt with. Leave blank to have one provided for you.
 *  Iv =      Iv to encrypt with. Leave blank to have one provided for you.
 *  key_len = How long to make the random key, must be 16, 24, or 32
________________________________________________________________________________


