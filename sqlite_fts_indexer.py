'''Prepare text and perform sqlite3 fts5 index

Index html and txt only.

If there are other files like pdf, docx...,
use Apache tika to convert them to txt first
'''

import re
import time
import sqlite3
import os
import glob
from bs4 import BeautifulSoup

__version__ = '0.3'
__author__ = 'kunda'


def mkdir_res(d=None):
    if d:
        os.makedirs(d, exist_ok=True)


def rf(f):
    t = ''
    with open(f, 'r') as fi:
        t = fi.read()
    return t


def wf(f, data):
    with open(f, 'w') as fo:
        fo.write(data)
    print(f'Wrote {f}')


def glob_dir(d, ext="*"):
    return glob.glob(f'{d}/**/*.{ext}', recursive=True)


def unzip_rename(zip_file):
    bare_name = zip_file[0: -len('.zip')]
    no_ver_name = re.sub(r'[\d\W]+', '', bare_name)

    cm_unzip = f'unzip -o -qq {zip_file}'
    cm_cpbackup = f'cp -r {bare_name} {bare_name}_origin'
    cm_rename = f'mv -f {bare_name} {no_ver_name}'

    os.system(cm_unzip)
    os.system(cm_cpbackup)
    os.system(cm_rename)

    return no_ver_name


def splitter(n, s):
    # https://stackoverflow.com/a/3861725
    pieces = s.split()
    return (" ".join(pieces[i: i + n]) for i in range(0, len(pieces), n))


def html_to_text(html):
    m = BeautifulSoup(html, 'lxml')
    return m.text


def prepare_line_chunk(content, token=800):
    content = content.split("\n")
    lines = [line for line in content if line.strip()]
    content = ""
    for line in lines:
        content += line.strip() + "\n"
    content = re.sub(r"(\S)[ \t]*(?:\r\n|\n)[ \t]*(\S)", r"\1 \2", content)
    content = re.sub(r"[\s]+", r" ", content)
    content = re.sub(r"\n", " ", content)
    strs = ""
    for piece in splitter(token, content):
        strs += piece + "\n"
    return strs


def fts_html_indexer(in_dir, db=None, index_file_ext='html,txt'):
    '''Indexing notes:


    Do not use the entire file content as one string to index

    Because:
    1- fts5 snippet function will only see it as 1 fragment
    2- the fts5 SORT BY path function will be much slower

    So avoid using this:
        tuble_list = [(path, filetext)]
        c.executemany("INSERT INTO pn VALUES (?,?)", tuble_list)
    '''

    # listing files with index_file_ext
    print(f'Listing {index_file_ext} in:', in_dir)
    index_file_ext = index_file_ext.split(',')
    index_file_ext = [e for e in index_file_ext if e]

    files = []
    log_skipped = ''
    for e in index_file_ext:
        files += glob_dir(in_dir, e)
    if not files:
        print(f'No {index_file_ext} files to index in', in_dir)
        return

    len_file = len(files)
    print_chunk = len_file // 100

    print('Processing', len_file, 'please wait...')

    # delete the old db of exist
    if not db:
        no_ver_name = re.sub(r'[\d\W]+', '', in_dir)
        db = no_ver_name + '.sqlite3'
    if os.path.isfile(db):
        os.remove(db)
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("CREATE VIRTUAL TABLE pn USING fts5(path, cont)")

    # read index, and convert to txt if html
    n = 0
    for f in files:
        text = ''
        if f.endswith('.html'):
            text = html_to_text(rf(f))
        elif f.endswith('.txt'):
            text = rf(f)
        else:
            log_skipped += 'Not html or txt file: ' + f + '\n'
            continue
        text = text.strip()
        if len(text) < 1:
            log_skipped += 'Empty data: ' + f + '\n'
            continue

        # chunk text and index
        text = prepare_line_chunk(text).split('\n')
        my_app_need = 'dev/' + f + '.txt'
        tuble_list = [(my_app_need, t.strip())
                      for t in text if len(t.strip()) > 3]
        c.executemany("INSERT INTO pn VALUES (?,?)", tuble_list)
        n += 1
        if n % print_chunk == 0:
            print(str(n) + ". Indexed: " + f)

    print(str(n) + ". Last indexed file: " + f)
    print("Optimizing the database...")
    c.execute("INSERT INTO pn(pn) VALUES('optimize')")
    conn.commit()
    conn.close()
    print('Done indexed:', n, '/', len(files))

    if log_skipped:
        with open('log_skipped.txt', 'w') as f:
            f.write(log_skipped)
        print('Check skipped files: log_skipped.txt')


if __name__ == '__main__':
    t = time.time()
    # fts_html_indexer('JavaScript', index_file_ext='html')
    fts_html_indexer('jdk-17_doc-all', index_file_ext='html,htm')
    print('Took:', time.time() - t, 'second(s).')
