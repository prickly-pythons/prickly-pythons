#example 1
import PP1
reload(PP1)
import PP2 as p
reload(p)

PP1.writename('Francis')
p.writename('Francis')


'''
#example 2
from PP1 import writename
from PP2 import *

writename('Francis')
'''
