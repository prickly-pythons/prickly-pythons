
from my_module import calc_mean

def test_int():
	num_list = [1,2,3,4,5]

	observed = calc_mean(num_list)
	expected = 3

	assert observed == expected


def test_double():
	num_list = [1,2,3,4]

	observed = calc_mean(num_list)
	expected = 2.5

	assert observed == expected


def test_big():
	num_list = [1000000000]

	observed = calc_mean(num_list)
	expected = 1000000000

	assert observed == expected