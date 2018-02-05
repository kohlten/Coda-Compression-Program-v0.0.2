from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')
file = sys.argv[1]
sys.argv.remove(file)

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    console = [{'script': file}],
    zipfile = None,
)