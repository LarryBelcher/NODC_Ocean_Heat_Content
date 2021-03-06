#!/usr/bin/python

import matplotlib as mpl
mpl.use('Agg')
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import shapefile, os, subprocess, urllib, time, sys, glob
from PIL import Image
from PIL import ImageOps
import matplotlib.font_manager as font_manager


def int2str(mm):
	if(mm == '01'): ms = 'January'
	if(mm == '02'): ms = 'February'
	if(mm == '03'): ms = 'March'
	if(mm == '04'): ms = 'April'
	if(mm == '05'): ms = 'May'
	if(mm == '06'): ms = 'June'
	if(mm == '07'): ms = 'July'
	if(mm == '08'): ms = 'August'
	if(mm == '09'): ms = 'September'
	if(mm == '10'): ms = 'October'
	if(mm == '11'): ms = 'November'
	if(mm == '12'): ms = 'December'
	return ms


imgDate = sys.argv[1] #Expects integer year and month (e.g., 201401)
					  #NOTE: month must be: 01, 04, 07, or 10 only since these are 
					  #seasonal data
yyyy = imgDate[0:4]
mm = imgDate[4:6]

monStr=0
if(int(mm) == 1): monStr = u'Jan\u2013Mar' ###NOTE, the \u2013 is a unicode en-dash
if(int(mm) == 4): monStr = u'Apr\u2013Jun'
if(int(mm) == 7): monStr = u'Jul\u2013Sep'
if(int(mm) == 10): monStr = u'Oct\u2013Dec'
if(int(mm) == 0): monStr = ''

labeldate = monStr+', '+yyyy
if(int(yyyy) == 0): labeldate = 'No Data'

imgsize = sys.argv[2]  #(expects 620, 1000, DIY, HD, or HDSD)

#Define the path to the original images
path2orig = './Images/Seasonal/Orig/'
infile = glob.glob(path2orig+'heat_content_anomaly_0-700_'+yyyy+'-'+mm+'.png')[0]
outpng = './temporary_map.png'

path = './Fonts/Trebuchet_MS.ttf'
propr = font_manager.FontProperties(fname=path)
path = './Fonts/Trebuchet_MS_Bold.ttf'
propb = font_manager.FontProperties(fname=path)



#Define some figure properties

if(imgsize == '620'):
	figxsize = 8.5
	figysize = 5.8
	figdpi = 72
	logo_image = './noaa_logo_42.png'
	logo_x = 568
	logo_y = 1
	mproj = 'HA'
	mlw = 0.2

if(imgsize == '1000'):
	figxsize = 13.78
	figysize = 7.5
	figdpi = 72
	logo_image = './noaa_logo_42.png'
	logo_x = 948
	logo_y = 2
	mproj = 'HA'
	mlw = 0.2


if(imgsize == 'DIY'):
	figxsize = 13.657
	figysize = 6.817
	figdpi = 300
	mproj = 'CE'
	mlw = 0.5

if(imgsize == 'HD'):
	figxsize = 26.67
	figysize = 15
	figdpi = 72
	logo_image = './noaa_logo_100.png'
	logo_x = 1596
	logo_y = 228
	mproj = 'RB'
	mlw = 0.5

if(imgsize == 'HDSD'):
	figxsize = 26.67
	figysize = 15
	figdpi = 72
	logo_image = './noaa_logo_70.png'
	logo_x = 1442
	logo_y = 394
	mproj = 'RB'
	mlw = 0.5


fig = plt.figure(figsize=(figxsize,figysize))
# create an axes instance, leaving room for colorbar at bottom.
if(imgsize == '620' or imgsize == '1000' or imgsize == 'DIY'):
	ax1 = fig.add_axes([0.0,0.0,1.0,1.0], frameon=False, axisbg='#F5F5F5')
if(imgsize == 'HD'):
	#ax1 = fig.add_axes([0.12,0.22,0.76,0.68], frameon=False, axisbg='#F5F5F5')
	ax1 = fig.add_axes([0.12,0.2199,0.76,0.679], frameon=False, axisbg='#F5F5F5')
if(imgsize == 'HDSD'):
	ax1 = fig.add_axes([0.15,0.367,0.7,0.513], frameon=False, axisbg='#F5F5F5')
	

if(mproj == 'HA'):
	# define projection (use -98.5 to center on North America)
	m = Basemap(projection='hammer',lon_0=-150.,resolution='l',area_thresh=10000, ax=ax1)
	m.drawmapboundary(color='#787878', linewidth=0.4)

if(mproj == 'CE'):
	# define projection
	m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,area_thresh=10000,\
	llcrnrlon=30,urcrnrlon=390,resolution='l')

if(mproj == 'RB'):
	m = Basemap(projection='robin',lon_0=-150,resolution='l')


orig = Image.open(infile)
bg = Image.new("RGB", orig.size, (211,211,211))
bg.paste(orig,orig)
bg.save("./tmp.png")
im = m.warpimage("./tmp.png")


# fill the continents/lakes
m.fillcontinents(color='#E2E2E2', lake_color='#E2E2E2')

#m.drawcoastlines(color='#787878',linewidth=mlw)
#m.drawcountries(color='#787878',linewidth=mlw)
#m.fillcontinents(color='#E2E2E2')
#m.drawrivers(color='#E2E2E2',linewidth=mlw+1.)


#Add the NOAA logo (except for DIY)
if(imgsize != 'DIY'):
	logo_im = Image.open(logo_image)
	height = logo_im.size[1]
	# We need a float array between 0-1, rather than
	# a uint8 array between 0-255 for the logo
	logo_im = np.array(logo_im).astype(np.float) / 255
	fig.figimage(logo_im, logo_x, logo_y, zorder=10)

if(imgsize == '620' or imgsize == '1000'):
	plt.savefig(outpng,dpi=figdpi, orientation='landscape', bbox_inches='tight', pad_inches=0.06)

if(imgsize == 'DIY'):
	plt.savefig(outpng,dpi=figdpi,orientation='landscape', bbox_inches='tight', pad_inches=0.01)

if(imgsize == 'HD' or imgsize =='HDSD'):
	plt.savefig(outpng,dpi=figdpi,orientation='landscape')#, bbox_inches='tight', pad_inches=0.01)

#clean up
cmd = "rm tmp.png"
subprocess.call(cmd,shell=True)
