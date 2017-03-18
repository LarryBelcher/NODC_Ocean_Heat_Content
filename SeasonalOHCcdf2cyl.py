#!/usr/bin/python

import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import netCDF4, sys
from mpl_toolkits.basemap import Basemap, shiftgrid, addcyclic
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap



def gmtColormap(fileName):

      import colorsys
      import numpy as N
      try:
          f = open(fileName)
      except:
          print "file ",fileName, "not found"
          return None

      lines = f.readlines()
      f.close()

      x = []
      r = []
      g = []
      b = []
      colorModel = "RGB"
      for l in lines:
          ls = l.split()
          if l[0] == "#":
             if ls[-1] == "HSV":
                 colorModel = "HSV"
                 continue
             else:
                 continue
          if ls[0] == "B" or ls[0] == "F" or ls[0] == "N":
             pass
          else:
              x.append(float(ls[0]))
              r.append(float(ls[1]))
              g.append(float(ls[2]))
              b.append(float(ls[3]))
              xtemp = float(ls[4])
              rtemp = float(ls[5])
              gtemp = float(ls[6])
              btemp = float(ls[7])

      x.append(xtemp)
      r.append(rtemp)
      g.append(gtemp)
      b.append(btemp)

      nTable = len(r)
      x = N.array( x , N.float32)
      r = N.array( r , N.float32)
      g = N.array( g , N.float32)
      b = N.array( b , N.float32)
      if colorModel == "HSV":
         for i in range(r.shape[0]):
             rr,gg,bb = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
             r[i] = rr ; g[i] = gg ; b[i] = bb
      if colorModel == "HSV":
         for i in range(r.shape[0]):
             rr,gg,bb = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
             r[i] = rr ; g[i] = gg ; b[i] = bb
      if colorModel == "RGB":
          r = r/255.
          g = g/255.
          b = b/255.
      xNorm = (x - x[0])/(x[-1] - x[0])

      red = []
      blue = []
      green = []
      for i in range(len(x)):
          red.append([xNorm[i],r[i],r[i]])
          green.append([xNorm[i],g[i],g[i]])
          blue.append([xNorm[i],b[i],b[i]])
      colorDict = {"red":red, "green":green, "blue":blue}
      return (colorDict)


if __name__ == '__main__':

	datamax = 50; datamin = -50
	figxsize = 13.657
	figysize = 6.817
	figdpi = 72

	imgDate = sys.argv[1] #Expects integer year and month (e.g., 201401)
						  #NOTE: month must be: 01, 04, 07, or 10 only since these are 
						  #seasonal data
	yyyy = imgDate[0:4]
	mm = imgDate[4:6]

	yearIndx = ((int(yyyy) - 1955)*12)/3
	monIndx=0
	if(int(mm) == 1): monIndx = 0
	if(int(mm) == 4): monIndx = 1
	if(int(mm) == 7): monIndx = 2
	if(int(mm) == 10): monIndx = 3

	timeIndx = yearIndx + monIndx



	infile = './Data/heat_content_anomaly_0-700_seasonal.nc'
	outpng = './Images/Seasonal/Orig/heat_content_anomaly_0-700_'+yyyy+'-'+mm+'.png'




	# Load data
	dataset = netCDF4.Dataset(infile)

	# Extract variables & close the file
	time = dataset.variables['time'][:]

	if(time.size == timeIndx):
		print ' '
		print 'Sorry, data are not available for '+yyyy+'-'+mm
		sys.exit()

	lons = dataset.variables['lon'][:]
	lats = dataset.variables['lat'][:]
	data = dataset.variables['h18_hc'][timeIndx,0,:,:]
	dataset.close()

	#shiftgrid(lon0, datain, lonsin, start=True, cyclic=360.0)
	#data,lons1 = shiftgrid(0,data,lons,start=True, cyclic=360.0)
	#data, lons1 = addcyclic(data, lons)

	lons = lons - 0.5
	lons = np.append(lons,180)
	data = np.append(data,data[:,0:1],axis=1)



	#Set the upper & lower bound of data range
	mask = data > 999.
	data[data > datamax] = datamax
	data[data < datamin] = datamin
	#Finally, nan out the missing data based on the above "mask test"
	data[mask] = np.nan

	fig = plt.figure(figsize=(figxsize,figysize))
	ax1 = fig.add_axes([0.0,0.0,1.0,1.0], frameon=False, axisbg='#F5F5F5')

	# setup basemap.
	m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,area_thresh=10000,\
		llcrnrlon=-180,urcrnrlon=180,resolution='l')
	#m.drawlsmask(land_color='#E2E2E2', ocean_color='#E2E2E2', lakes=False)

	cdict1 = gmtColormap('./OceanHeatContent.cpt')
	cmap_temp = LinearSegmentedColormap('cmap_temp', cdict1)


	# Set up grid
	x, y = np.meshgrid(lons, lats)

	levs = np.arange(101)-50
	m.contourf(x, y, data, levs, cmap=cmap_temp)
	#m.fillcontinents(color='#E2E2E2', lake_color='#E2E2E2')
	#m.drawcoastlines(color='#787878',linewidth=0.15)
	#m.drawcoastlines(color='#E2E2E2',linewidth=0.15)
	#m.drawrivers(color='#E2E2E2',linewidth=1)


	#plt.show()
	plt.savefig(outpng,dpi=figdpi, orientation='landscape', bbox_inches='tight', pad_inches=0.0)