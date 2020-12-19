# Converting utf-16-le binary files to plain utf-8 text files
# 05 Nov 2020, Panmux

import os
import time


def mkPaths(file_path):
    # Modified https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-dir
    dir = os.path.dirname(file_path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def lsFiles(dir, fileExt):
    """
    Modified https://stackoverflow.com/a/21281918
    @fileExt = 'html, htm' or '*' to list all
    Return: ['full','file','path']
    """

    matches = []
    if not dir.endswith("/"):
        dir = dir + "/"
    fileExt = fileExt.strip(" ,")
    lis = fileExt.split(",")
    tupleExt = tuple([i.strip() for i in lis])
    print("Listing files end with: " + str(tupleExt))
    for root, dirs, files in os.walk(dir):
        for file in files:
            if fileExt == "*":
                matches.append(os.path.join(root, file))
            else:
                if file.endswith(tupleExt):
                    matches.append(os.path.join(root, file))
    print("Finished listing, total files: " + str(len(matches)))
    return matches


def binary2text(inDir, outDir, frExt, frCode="utf-16-le", toCode="utf-8"):
    """
    inDir: Input doc directory
    outDir: Output doc directory
    frExt: Filter input file 'html, htm' or '*' to list all
    toExt: Save converted text in this file extention
    """

    i = 0
    if not inDir.endswith("/"):
        inDir = inDir + "/"
    if not outDir.endswith("/"):
        outDir = outDir + "/"

    mkPaths(outDir)
    files = lsFiles(inDir, frExt)

    print("")
    print("----- Convert Binary Files to TXT -----------")
    print("Input dir: \033[0;31m" + inDir + "\033[0m")
    print("Input file total: \033[0;32m" + str(len(files)) + "\033[0m files.")
    print("Output dir: \033[0;32m" + outDir + "\033[0m")
    print("-----------------------------------------")
    print("Processing...")
    for url in files:
        newpath = url.replace(inDir, outDir, 1)
        mkPaths(newpath)
        with open(url, mode="r", encoding=frCode) as f:
            with open(newpath, mode="w", encoding=toCode) as fw:
                fw.write(f.read())
        i = i + 1
        print(str(i) + ". Converted: " + url)

        # # You can limit how many files to be converted here
        # limitFile = 10
        # if(i == limitFile):
        #   break

    print("")
    print("-----------------------------------------")
    print("Input file total: \033[0;32m" + str(len(files)) + "\033[0m files.")
    print(
        "\033[0;32mDone\033[0m, processes total: \033[0;32m" + str(i) + "\033[0m files."
    )
    print("Process time: " + str(time.process_time()) + " seconds")
    print("-----------------------------------------")


binary2text(
    "/home/d/dev/tipitakaAppEdit/tipitaka.app-master/static/text",
    "/home/d/dev/tipitakaAppEdit/tipitaka.app-master/static/text-plain",
    "txt",
)
