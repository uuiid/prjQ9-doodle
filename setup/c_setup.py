from distutils.core import setup
from Cython.Build import cythonize

setup(name="test", ext_modules=cythonize('temp/test.pyx', annotate=True),)