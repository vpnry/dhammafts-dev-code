"""
08 Nov 2020
List files and full text search index with fts5 sqlite3
Many code snippets are adapted from:
sqlite3 section https://docs.python.org
fts5 section http://www.sqlite.org
answers from https://stackoverflow.com
"""
import sqlite3
import os


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
        "Now making a query fetching one result for the indexed database " + str(dbname)
    )

    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("SELECT * FROM pn WHERE pn MATCH 'kathina'")
    print(c.fetchall())
    print()
    conn.close()


# -----------------------------------------------------------------------
dbname = "libtxt.sqlite3"
testQuery(dbname)

# toCheckDump(dbname)
