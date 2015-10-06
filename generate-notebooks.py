import glob
import json
import io
import os
from subprocess import Popen, PIPE, check_call
import sys

join = os.path.join

dolfin_version = '1.6.0'
dolfin_root = 'dolfin-' + dolfin_version
dolfin_url = 'https://bitbucket.org/fenics-project/dolfin/downloads/dolfin-%s.tar.gz' % dolfin_version

if not os.path.exists(dolfin_root):
    print("Downloading %s" % dolfin_url)
    check_call(['wget', '-nc', '-q', dolfin_url])
    print("Unpacking %s" % dolfin_root)
    check_call(['tar', '-xzf', dolfin_root + '.tar.gz'])

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
    
    # associate notebooks with fenics kernel
    with io.open(dst) as f:
        nb = json.load(f)
    
    nb['metadata']['kernelspec'] = {
        "display_name": "Python 2 (fenics)",
        "language": "python",
        "name": "fenics",
    }
    with io.open(dst, 'w') as f:
        json.dump(nb, f, indent=1, sort_keys=True)
        f.write('\n')

for name in sorted(os.listdir(documented)):
    print(name)
    rst2ipynb(name)

    