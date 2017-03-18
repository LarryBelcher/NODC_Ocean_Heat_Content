#!/usr/bin/python

import subprocess


years = ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016']
mons = ['01', '04', '07', '10']
isz = ['620', '1000', 'DIY', 'HD', 'HDSD']


for i in range(len(years)):
	for j in range(len(mons)):
		for k in range(len(isz)):
			cmd = 'python  SeasonalOHCcdf2cyl.py '+years[i]+mons[j]
			subprocess.call(cmd,shell=True)
			cmd = 'python  nodc_seasonal_driver.py '+years[i]+mons[j]+' '+isz[k]
			subprocess.call(cmd,shell=True)
