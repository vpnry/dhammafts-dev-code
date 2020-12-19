"""
Fix broken lines and make para of 888 tokens
"""

import re
import os
import time


def mkPaths(file_path):
    # Modified https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-dir
    dir = os.path.dirname(file_path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def lsFiles(dir, extStr):
    """
    Modified https://stackoverflow.com/a/21281918
    @extStr = 'html, htm' or '*' to list all
    Return: ['full','file','path']
    """

    matches = []
    if not dir.endswith("/"):
        dir = dir + "/"
    extStr = extStr.strip(" ,")
    lis = extStr.split(",")
    tupleExt = tuple([i.strip() for i in lis])
    print("Listing files end with: " + str(tupleExt))
    for root, dirs, files in os.walk(dir):
        for file in files:
            if extStr == "*":
                matches.append(os.path.join(root, file))
            else:
                if file.endswith(tupleExt):
                    matches.append(os.path.join(root, file))
    print("Finished listing, total files: " + str(len(matches)))
    return matches


# https://stackoverflow.com/a/3861725
def splitter(n, s):
    pieces = s.split()
    return (" ".join(pieces[i : i + n]) for i in range(0, len(pieces), n))


def spit2Token(token, inDir, outDir, frExt, fixBrokenLine=True):

    """
    It will fix broken lines and make paragraphs of number of token words.
    If you index the whole file content with fts5, the search performance later is slow down.
    If you index line by line, the database file size will be larger.
    """

    i = 0
    if not inDir.endswith("/"):
        inDir = inDir + "/"
    if not outDir.endswith("/"):
        outDir = outDir + "/"

    mkPaths(outDir)
    files = lsFiles(inDir, frExt)
    print("")
    print("----- Tika Convert Files to TXT -----------")
    print("Input dir: \033[0;31m" + inDir + "\033[0m")
    print("Input file total: \033[0;32m" + str(len(files)) + "\033[0m files.")
    print("Output dir: \033[0;32m" + outDir + "\033[0m")
    print("-----------------------------------------")
    print("Processing...")
    for url in files:
        with open(url, "r") as fc:
            content = fc.read()
            content = content.strip()
        if fixBrokenLine:
            # remove empty lines
            content = content.split("\n")
            lines = [line for line in content if line.strip()]
            content = ""
            for l in lines:
                content += l.strip() + "\n"

            # Join broken words
            content = re.sub(r"(\S)[ \t]*(?:\r\n|\n)[ \t]*(\S)", r"\1 \2", content)
            content = re.sub(r"[\s]+", r" ", content)
            content = re.sub(r"\n", " ", content)
            strs = ""
            for piece in splitter(token, content):
                strs += piece + "\n"

        newpath = url.replace(inDir, outDir, 1)
        mkPaths(newpath)
        with open(newpath, "w") as fc:
            fc.write(strs)

        i = i + 1
        print(str(i) + ". Processed: " + url)

        # You can limit how many files to be converted here
        # limitFile = 100
        # if i == limitFile:
        #     break

    print("")
    print("-----------------------------------------")
    print("Input file total: \033[0;32m" + str(len(files)) + "\033[0m files.")
    print(
        "\033[0;32mDone\033[0m, processes total: \033[0;32m" + str(i) + "\033[0m files."
    )
    print("Process time: " + str(time.process_time()) + " seconds")
    print("-----------------------------------------")


# spit2Token(888, "dict", "dict4", "*", True)
# spit2Token(888, "pn", "pn4", "*", True)

spit2Token(888, "ttpv-txt", "ttpv", "*", True)


