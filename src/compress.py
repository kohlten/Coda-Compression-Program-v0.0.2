import pylzma

# #Takes in some an array of text and returns the compressed version with the names


def compress(text, names):
    output = []

    for string in text:
        print(names[text.index(string)] + " is compressed!")
        compressed = pylzma.compress(string)
        output.append(compressed)

    names = str(names).replace("[", "").replace("]", "").replace("'", "").replace(" ", "")

    return output, names
