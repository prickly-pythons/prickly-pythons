__all__ = ["power","aux"]

from windpype.power import *

print('windpype module import complete')


import matplotlib as mpl

fs = 14
mpl.rcParams['lines.linewidth']=2
mpl.rcParams['lines.markersize']=5
mpl.rcParams['font.size']=fs
mpl.rcParams['font.weight']=500
mpl.rcParams['xtick.labelsize'] = fs
mpl.rcParams['axes.labelweight'] = 500
mpl.rcParams['ytick.labelsize'] = fs
mpl.rcParams['axes.labelsize']=fs
mpl.rcParams['axes.linewidth'] = 1.5
mpl.rcParams['xtick.major.width'] = 1.5
mpl.rcParams['xtick.minor.width'] = 1.3
mpl.rcParams['ytick.major.width'] = 1.5
mpl.rcParams['ytick.minor.width'] = 1.3

# Use this instead??
plt.style.use('seaborn-talk')