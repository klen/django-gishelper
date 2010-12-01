import os

from setuptools import setup, find_packages
from gishelper import PROJECT, VERSION


def read( fname ):
    try:
        return open( os.path.join( os.path.dirname( __file__ ), fname ) ).read()
    except IOError:
        return ''


META_DATA = dict(
    name = PROJECT,
    version = VERSION,
    description = read('DESCRIPTION'),
    long_description = read('README.rst'),
    license='Public domain',

    author = "Kirill Klenov",
    author_email = "horneds@gmail.com",

    url = "http://github.com/klen/django-gishelper.git",

    packages = find_packages(),

    install_requires = [ 'django' ],
)

if __name__ == "__main__":
    setup( **META_DATA )
