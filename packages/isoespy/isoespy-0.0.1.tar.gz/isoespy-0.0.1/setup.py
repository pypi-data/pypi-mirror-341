from setuptools import setup
from Cython.Build import cythonize
#from setuptools.command.install import install
#import subprocess
#import shutil

# cython
result_1 = cythonize("src/isoespy/isoespy_de.pyx")
result_2 = cythonize("src/isoespy/isoespy_ff.pyx")
result_3 = cythonize("src/isoespy/isoespy_edger.pyx")
result_4 = cythonize("src/isoespy/isoespy_makefa.pyx")
result_5 = cythonize("src/isoespy/isoespy_makegtf.pyx")
result_6 = cythonize("src/isoespy/isoespy_orfpred.pyx")
setup(ext_modules=result_1)
setup(ext_modules=result_2)
setup(ext_modules=result_3)
setup(ext_modules=result_4)
setup(ext_modules=result_5)
setup(ext_modules=result_6)
