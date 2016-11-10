print('This is sub-module 2')

# If we want to use a function from submodule1, 
# we have to import that submodule here:
import submodule1 as submodule1

def function2():
	print('This is function 2 calling function 1')

	submodule1.function1()


def function3():
	print('This is function 2 calling function 1 and saving the result')
	import numpy as np

	result 			=	submodule1.function1()

	np.save('results/some_result',result)