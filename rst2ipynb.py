import glob
import io
import os
from subprocess import Popen, PIPE
import sys

join = os.path.join

dolfin_root = 'dolfin-1.6.0'

documented = join(dolfin_root, 'demo', 'documented')

def rst2ipynb(name):
    src = join(documented, name, 'python', 'documentation.rst')
    pandoc = Popen([
            'pandoc',
            '--atx-headers',
            '--from', 'rst',
            '--to', 'markdown',
            src,
        ], stdout=PIPE, stdin=PIPE)
    md, _ = pandoc.communicate()
    if pandoc.returncode:
        sys.exit("pandoc failed")
    
    dst = name + '.ipynb'
    notedown = Popen([
            'notedown', '-o', dst,
        ], stdin=PIPE)
    notedown.communicate(md)
    if notedown.returncode:
        sys.exit("notedown failed")

for name in sorted(os.listdir(documented)):
    print(name)
    rst2ipynb(name)

    