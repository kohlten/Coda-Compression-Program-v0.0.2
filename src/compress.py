import zlib

# #Takes in some an array of text and returns the compressed version with the names


def compress(text, names):
    output = []
    lengths = []

    for string in text:
        print(names[text.index(string)] + " is compressed!")
        compressed = zlib.compress(string, zlib.Z_BEST_COMPRESSION)
        output.append(compressed)
        lengths.append(len(compressed))

    names = str(names).replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
    lengths = str(lengths).replace("[", "").replace("]", "").replace("'", "").replace(" ", "")

    return output, names, lengths
