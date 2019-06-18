from distutils.core import setup
import glob

setup(name='blog',
      version='1.0',
      description='Blog Project',
      author='Leo Yan',
      author_email='yanruining@126.com',
      url='https://yrn.com',
      packages=['blog', 'post','user'],
      py_modules=['manage'],
      data_files = ['requirements'] + glob.glob('templates/*.html') + glob.glob('static/*.html')
     )