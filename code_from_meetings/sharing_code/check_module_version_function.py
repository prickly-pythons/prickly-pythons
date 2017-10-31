# A small function to check package versions before running your code

def check_version(module,version_required):
	'''
	Function that checks version of any module and compares it to a required version number

	Arguments:
	module: name of the module - str
	version_required: list of three version numbers - list

	'''

	version 		=	module.__version__

	for i,subversion in enumerate(version.split('.')):
		if int(subversion) < version_required[i]:
			print('\nActive version of %s module might cause problems...' % module.__name__)
			print('version detected: %s' % version)
			print('version required: %s.%s.%s' % (version_required[0],version_required[1],version_required[2]))
			break
		if i == len(version.split('.'))-1:
			print('\nNo version problems for %s module expected!' % module.__name__)

# check if numpy version is 1.15.0 or higher:

import numpy as np

check_version(np,[1,15,0]) 


# check if pandas version is 0.24.0 or higher:

import pandas as pd

check_version(pd,[0,19,0]) 




