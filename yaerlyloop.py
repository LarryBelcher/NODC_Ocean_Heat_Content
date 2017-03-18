#!/usr/bin/python

import subprocess

years = ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014']
isz = ['620', '1000', 'DIY', 'HD', 'HDSD']

for i in range(len(years)):
	for j in range(len(isz)):
		cmd = 'nodc_yearly_driver.py '+years[i]+' '+isz[j]
		subprocess.call(cmd,shell=True)
