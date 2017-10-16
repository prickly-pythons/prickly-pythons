from astropy.io import ascii
from astropy.table import Table, vstack
from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np

ned1=ascii.read("/Users/dhk/work/cat/NGC_IC/ned_result_1.txt")
ned2=ascii.read("/Users/dhk/work/cat/NGC_IC/ned_result_2.txt")
ned3=ascii.read("/Users/dhk/work/cat/NGC_IC/ned_result_3.txt")
ned4=ascii.read("/Users/dhk/work/cat/NGC_IC/ned_result_4.txt")
ned5=ascii.read("/Users/dhk/work/cat/NGC_IC/ned_result_5.txt")

ned_tot=vstack([ned1,ned2,ned3,ned4,ned5])

sha1=ascii.read("/Users/dhk/work/cat/NGC_IC/SHA_mosaic_quarry_result_0.tbl",format='ipac')
sha2=ascii.read("/Users/dhk/work/cat/NGC_IC/SHA_mosaic_quarry_result_1.tbl",format='ipac')
sha3=ascii.read("/Users/dhk/work/cat/NGC_IC/SHA_mosaic_quarry_result_2.tbl",format='ipac')
sha4=ascii.read("/Users/dhk/work/cat/NGC_IC/SHA_mosaic_quarry_result_3.tbl",format='ipac')
sha5=ascii.read("/Users/dhk/work/cat/NGC_IC/SHA_mosaic_quarry_result_4.tbl",format='ipac')
sha6=ascii.read("/Users/dhk/work/cat/NGC_IC/SHA_mosaic_quarry_result_5.tbl",format='ipac')
sha7=ascii.read("/Users/dhk/work/cat/NGC_IC/SHA_mosaic_quarry_result_6.tbl",format='ipac')
sha8=ascii.read("/Users/dhk/work/cat/NGC_IC/SHA_mosaic_quarry_result_7.tbl",format='ipac')
sha9=ascii.read("/Users/dhk/work/cat/NGC_IC/SHA_mosaic_quarry_result_8.tbl",format='ipac')
sha10=ascii.read("/Users/dhk/work/cat/NGC_IC/SHA_mosaic_quarry_result_9.tbl",format='ipac')
sha11=ascii.read("/Users/dhk/work/cat/NGC_IC/SHA_mosaic_quarry_result_10.tbl",format='ipac')
sha12=ascii.read("/Users/dhk/work/cat/NGC_IC/SHA_mosaic_quarry_result_11.tbl",format='ipac')
sha13=ascii.read("/Users/dhk/work/cat/NGC_IC/SHA_mosaic_quarry_result_12.tbl",format='ipac')
sha14=ascii.read("/Users/dhk/work/cat/NGC_IC/SHA_mosaic_quarry_result_13.tbl",format='ipac')

sha_tot=vstack([sha1,sha2,sha3,sha4,sha5,sha6,sha7,sha8,sha9,sha10,sha11,sha12,sha13,sha14],join_type='exact')

sha_ned_match = Table(names=('id','ra','dec','mag','2a','2b','off','fov','param','a_fov','off_fov'),dtype=('S8','f4','f4','S6','f4','f4','f4','f4','f4','f4','f4'))
#sha_ned_match = Table()

for x in range(0,len(ned_tot)):
	if ned_tot['col11'][x] > 0:
		sha_match = sha_tot[(sha_tot['Search_Tgt'] == ned_tot['col2'][x]) & (sha_tot['band_name'] == 'IRAC1')]	# select same NGC/IC name w/ band_name IRAC1
		if len(sha_match) == 0:
			continue
		coord_ned = SkyCoord(ned_tot['col4'][x],ned_tot['col5'][x],frame='icrs')
		coord_sha = SkyCoord(sha_match['ra'],sha_match['dec'],unit="deg")
		off = coord_ned.separation(coord_sha)   
		pri = (sha_match['s_fov']*30 - off.arcminute)/(ned_tot['col11'][x]/2)			# (s_fov/2 - offset)/(a/2)
		a_fov = ned_tot['col11'][x] / (sha_match['s_fov']*30)					# a_fov
		off_fov = off.arcminute / (sha_match['s_fov']*30)
		ind = np.argmin(pri)									# 
		sha_ned_match.add_row([sha_match['Search_Tgt'][ind],coord_ned.ra,coord_ned.dec,ned_tot['col10'][x],ned_tot['col11'][x],ned_tot['col12'][x],off[ind].arcminute,sha_match['s_fov'][ind]*60,pri[ind],a_fov[ind],off_fov[ind]])



sha_ned_match.write('sha_ned_match_w_mag.txt',format='ascii',overwrite=True)
#thefile = open('sha_ned_match.txt','w')
#for item in sha_ned_match:
#	thefile.write("%s\n" % item)
	
