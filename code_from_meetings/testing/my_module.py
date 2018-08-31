
from __future__ import division

def calc_mean(num_list):
    
    try:
        return sum(num_list) / len(num_list)
    
    except TypeError:
        msg = "Don't be silly"
        raise TypeError(msg)
        
    except ZeroDivisionError:
        msg = "Oh no. No elements in your array."
        raise TypeError(msg)
