# Matplotlib Demo 7
# contour plotting
# copied from the web as follows:
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np

# function to contour
def f(x,y):
    return (1-x/2+x**5+y**3)*np.exp(-x**2-y**2)

# create x-y grid, 256 points on a side
n = 256
x = np.linspace(-3,3,n)
y = np.linspace(-3,3,n)
X,Y = np.meshgrid(x,y)

# color contours
plt.contourf(X, Y, f(X,Y), 8, alpha=.75, cmap=plt.cm.hot)

# black contour lines between sections
C = plt.contour(X, Y, f(X,Y), 8, colors='black', linewidth=.5)

# contour labels
plt.clabel(C, inline=1, fontsize=10)


# trickery to make the plot come up maximized for presentation
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()

plt.show()
