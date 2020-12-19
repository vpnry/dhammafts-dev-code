"""
Created: 08 Nov 2020
Modified 29 Nov 2020
List files and full text search index with fts5 sqlite3
Many code snippets are adapted from:
sqlite3 section https://docs.python.org
fts5 section http://www.sqlite.org
answers from https://stackoverflow.com
"""
import sqlite3
import os
import re


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


def runIndexer(inDir, extStr, dbname):
    # Filter files to index, use "*" for all
    paths = lsFiles(inDir, extStr)
    if os.path.exists(dbname):
        print("")
        print("Deleting old database file: \033[0;31m" + str(dbname) + "\033[0m")
        print("")
        os.remove(dbname)
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("CREATE VIRTUAL TABLE pn USING fts5(path, cont)")

    n = 0
    for path in paths:
        with open(path, "r") as fc:
            n = n + 1
            text = fc.read()
            text = text.strip()
            text = text.split("\n")
            # tubleList = [(path, t) for t in text]
            tubleList = [(path, t.strip()[4:].strip()) for t in text if t.strip()]

            c.executemany("INSERT INTO pn VALUES (?,?)", tubleList)

            # the whole file has one problem is that fts5 snippet only can extract 1 fragment
            # and make the SORT BY path much slower, should not use this
            # tubleList = [(path, text)]
            # c.executemany("INSERT INTO pn VALUES (?,?)", tubleList)

            print(str(n) + ". Done: " + path)

    # Special optimize command of fts5
    print()
    print("Now it is optimizing the database...")
    c.execute("INSERT INTO pn(pn) VALUES('optimize')")

    # Save (commit) and close
    conn.commit()
    conn.close()

    print("Done indexed files: " + str(n))


def toCheckDump(dbname):
    # Convert file existing_db.db to SQL dump file dump.sql
    con = sqlite3.connect(dbname)
    with open("dump.sql", "w") as f:
        for line in con.iterdump():
            f.write("%s\n" % line)
    con.close()


def testQuery(dbname):
    print()
    print(
        "Now making a query test and fetching one result for the indexed database " + str(dbname)
    )

    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("SELECT * FROM pn WHERE cont MATCH 'Naḷamālikā' ORDER BY rank")
    print(c.fetchone())
    print()
    conn.close()


# -----------------------------------------------------------------------
dbname = "tptk.sqlite3"
runIndexer("tptk", "*", dbname)
testQuery(dbname)
# toCheckDump(dbname)
