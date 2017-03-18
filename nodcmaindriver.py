#!/usr/bin/python

'''******************************************************************************************************
Program: nodcmaindriver.py

Usage: ./nodcmaindriver.py [args]

Synopsis:
This script will retrieve NODC Oceanheat anomaly data and produce maps. The user has the option to pass arguments
in the form of year and season (01, 04, 07, or 10) to force the script to generate maps for a specific seaon or 
just year to produce the annual maps.

*********************************************************************************************************'''

import subprocess, sys, datetime


if __name__ == '__main__':

	if(len(sys.argv) == 1):
		date_last_month = datetime.datetime.now()
		yyyy = date_last_month.year
		mm = date_last_month.month
		stryyyy = str(yyyy)
		if(mm >= 1 and mm < 4): strmm = '01'
		if(mm >= 4 and mm < 7): strmm = '04'
		if(mm >= 7 and mm < 10): strmm = '07'
		if(mm >= 10): strmm = '10'
		pdate = stryyyy+strmm
			
		#make sure data are most recent, otherwise download new file
		cmd = 'stat Data/heat_content_anomaly_0-700_seasonal.nc'
		proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
		(out, err) = proc.communicate()
		mydate = out.split('"')[3]
		mon = mydate.split(' ')[0]
		yyyy = mydate.split(' ')[4]
		dd = mydate.split(' ')[2]
		if(int(dd) < 10): dd = '0'+dd
		mydate = dd+'-'+mon+'-'+yyyy
	
		cmd = 'curl https://data.nodc.noaa.gov/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/NETCDF/heat_content/ | grep heat_content_anomaly_0-700_seasonal.nc'
		proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
		(out, err) = proc.communicate()
		remotedate = out.split(' ')[24]
	
		if(mydate == remotedate):
			print 'Sorry, no new data'
			sys.exit()
	
		if(mydate != remotedate):
			cmd = 'update_data.csh'
			subprocess.call(cmd, shell=True)



	if(len(sys.argv) > 1):
		pdate = sys.argv[1]

	#Set the AWS public key for the upload script
	pk = '/Users/belcher/AwsFiles/NewEarl.pem'
	
	#Make the CED map
	cmd = 'python SeasonalOHCcdf2cyl.py '+pdate
	subprocess.call(cmd, shell=True)
	
	if(len(pdate) == 6):
		isz = ['620', '1000', 'DIY', 'HD', 'HDSD']
		for i in xrange(len(isz)):
			cmd = ' python nodc_seasonal_driver.py '+pdate+' '+isz[i]
			subprocess.call(cmd, shell=True)
		cmd = "UploadNODCImages.csh "+pk
		subprocess.call(cmd, shell=True)
		
	if(len(pdate) == 4):
		isz = ['620', '1000', 'DIY', 'HD', 'HDSD']
		for i in xrange(len(isz)):
			cmd = ' python nodc_yearly_driver.py '+pdate+' '+isz[i]
			subprocess.call(cmd, shell=True)
		cmd = "UploadNODCImages.csh "+pk
		subprocess.call(cmd, shell=True)