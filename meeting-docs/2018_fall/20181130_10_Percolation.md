# Friday, Nov 30 2018

## Recap of meeting 10 this semester!
- One definition of percolation is the connectivity in random systems.
- It is one of the simplest considerations on a system that shows cricitical behaviours.
- We can model percolation in 2D by randomly placing 1's and 0's in an array and seeing for example if pouring 2-dimensional coffee into one side of this system will result in the coffee flowing out of the opposite side (here, 1 means obstruction, 0 means coffee is free to flow).
- These 1's pixels connect to form clusters, which could be thought of as individual coffee grains of different sizes and shapes in a percolator in the above analogy.
- The clusters can be labelled with Scipy's label routine in `scipy.ndimage.measurements`
- The critical point comes when all it takes is the addition of a single 1's pixel for whole clusters to become connected and the resulting giant cluster spans the entire system.
- Determination of this critical point via averaging random instances of the system (Monte Carlo simulation) can result in large error bars because the correlation exactly at the critical point is theoretically at all scales - phase transition!


# More info:
- The Jupyter notebook presented is [here](https://github.com/prickly-pythons/prickly-pythons/blob/master/code_from_meetings/complex_systems/Percolation.ipynb).
- https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.measurements.label.html
