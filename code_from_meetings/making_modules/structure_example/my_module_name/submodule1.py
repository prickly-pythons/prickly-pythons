print('This is sub-module 1')


def function1():
	print('This is function 1')

	number1        	=    raw_input('write one number: [default: 1] ... ')
	if number1 == '': number1 = '1'
	number2        	=    raw_input('write another number: [default: 1] ... ')
	if number2 == '': number2 = '1'

	number1 		=	float(number1) 
	number2 		=	float(number2)

	print('The sum of these two numbers is: '+str(number1+number2))

	# print('The difference between these two numbers is: '+str(number1-number2))

	return(number1+number2)

