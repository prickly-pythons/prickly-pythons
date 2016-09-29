# Matplotlib Demo 8
# basemap
# JDWest 10/19/2015

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# lists of values for all runs
Titles = ["Southern California", "Northern California", "Pacific NorthWest", "Utah" ]
MinLats = [32, 34, 42, 36.5 ]
MaxLats = [37, 43, 49, 42.5 ]
MinLons = [-120, -125, -125, -114 ]
MaxLons = [-115, -117, -117, -109 ]
Colors = ['m', 'c', 'b', 'y']
Lines = []

# plot the map of the western US
map = Basemap(projection = 'laea', llcrnrlon = -125, llcrnrlat = 29.5, urcrnrlon = -95, urcrnrlat = 49.5, resolution = 'l', area_thresh = 10, lat_0 = 39.5, lon_0 = -110)

# base map with no symbols
map.drawcountries(linewidth=1.5)
map.drawcoastlines(linewidth=.75)
map.drawmapboundary() 
map.drawstates(linewidth=0.5)
map.drawmeridians(range(int(-125), int(-95), 5), dashes=[5,5], labels=[0,0,0,1], labelstyle="+/-", linewidth=.25, size=7)
map.drawparallels(range(int(29.5), int(49.5), 5), dashes=[5,5], labels=[0,1,0,0], labelstyle="+/-", linewidth=.25, size=7)

plt.title("Study Areas in Western US", size='12')

plt.tick_params(axis='both', labelsize=7)

map.bluemarble()	

for Run in range(len(Titles)):

	# values for this run
	Title = Titles[Run]
	MinLat = MinLats[Run]
	MaxLat = MaxLats[Run]
	MinLong = MinLons[Run]
	MaxLong = MaxLons[Run]
	BoxColor = Colors[Run]
	
	# draw a rectangle on the map
	map.drawgreatcircle(MinLong, MinLat, MinLong, MaxLat, color=BoxColor, linewidth=3.0)
	map.drawgreatcircle(MinLong, MinLat, MaxLong, MinLat, color=BoxColor, linewidth=3.0)
	map.drawgreatcircle(MaxLong, MinLat, MaxLong, MaxLat, color=BoxColor, linewidth=3.0)
	map.drawgreatcircle(MaxLong, MaxLat, MinLong, MaxLat, color=BoxColor, linewidth=3.0)

	# build the legend list
	Lines.append(plt.Line2D(range(0), range(0), color=BoxColor, linewidth=3.0))

# show the legend	
plt.legend(Lines, Titles, loc="upper right")


# trickery to make the plot come up maximized for presentation
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()

plt.show()
