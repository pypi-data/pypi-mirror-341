from setuptools import find_packages,setup

setup(name='houhou',
      py_modules=['houhou.etsy','houhou.sql_handler','houhou.logger','houhou.request_handler'],
      version='0.0.91',
      description='This is for my own use',
      author='hhh',
      author_email='',
      packages=find_packages(),
      classifiers=[
              "Programming Language :: Python :: 3",#使用Python3
              "License :: OSI Approved :: Apache Software License",#开源协议
              "Operating System :: OS Independent",
          ],

      )