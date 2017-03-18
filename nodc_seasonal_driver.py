#!/usr/bin/python

import matplotlib as mpl
mpl.use('Agg')
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os, datetime, sys, glob, subprocess
import numpy as np

if __name__ == '__main__':

	imgDate = sys.argv[1] #Expects integer year and month (e.g., 201401)
						  #NOTE: month must be: 01, 04, 07, or 10 only since these are 
						  #seasonal data
	yyyy = imgDate[0:4]
	mm = imgDate[4:6]

	if(int(mm) == 2 or int(mm) == 3 or int(mm) == 5 or int(mm) == 6 or int(mm) == 8
		or int(mm) == 9 or int(mm) == 11 or int(mm) == 12):
		print ' '
		print 'You entered an incorrect month!'
		print 'Plese select one of: 01, 04, 07, or 10'
		sys.exit()

	monStr=0
	if(int(mm) == 1): monStr = u'Jan\u2013Mar' ###NOTE, the \u2013 is a unicode en-dash
	if(int(mm) == 4): monStr = u'Apr\u2013Jun'
	if(int(mm) == 7): monStr = u'Jul\u2013Sep'
	if(int(mm) == 10): monStr = u'Oct\u2013Dec'
	if(int(mm) == 0): monStr = ''

	labeldate = monStr+', '+yyyy
	if(int(yyyy) == 0): labeldate = 'No Data'

	imgsize = sys.argv[2]  #(expects 620, 1000, DIY, HD, or HDSD )

	if(imgsize != 'DIY'): figdpi = 72
	if(imgsize == 'DIY'): figdpi = 300

	path2orig = './Images/Seasonal/Orig/'
	infile = glob.glob(path2orig+'heat_content_anomaly_0-700_'+yyyy+'-'+mm+'.png')
	if(len(infile) == 0):
		print ' '
		print 'Sorry, data are not available for '+yyyy+'-'+mm
		sys.exit()


	cmd = "python ./nodc_seasonal_map.py "+imgDate+" "+imgsize
	subprocess.call(cmd,shell=True)

	if(imgsize == '620' or imgsize == '1000' or imgsize == 'DIY'):
		cmd = "python ./nodc_seasonal_colorbar.py "+imgDate+" "+imgsize
		subprocess.call(cmd,shell=True)

	if not os.path.isdir('./Images/Seasonal'):
		cmd = 'mkdir ./Images/Seasonal'
		subprocess.call(cmd,shell=True)
	if not os.path.isdir('./Images/Seasonal/'+imgsize):
		cmd = 'mkdir ./Images/Seasonal/'+imgsize.lower()
		subprocess.call(cmd,shell=True)


	if(imgsize == '620' or imgsize == '1000'):
		im1 = Image.open("temporary_map.png")
		im2 = Image.open("temporary_cbar.png")
		im3 = Image.new('RGBA', size = (im1.size[0], im1.size[1]+im2.size[1]))
		im3.paste(im2, (0,im1.size[1]))
		im3.paste(im1, (0,0))
		imgw = str(im3.size[0])
		imgh = str(im3.size[1])
		img_path = './Images/Seasonal/'+imgsize+'/'
		img_name = 'heatcontentanomaly-seasonal-ncei--'+imgw+'x'+imgh+'--'+yyyy+'-'+mm+'-00.png'
		pngfile = img_path+img_name
		print "Saving "+pngfile
		im3.save(pngfile)


	if(imgsize == 'DIY'):
		im1 = "./temporary_map.png"
		imgs = Image.open(im1)
		imgw = str(imgs.size[0])
		imgh = str(imgs.size[1])
		img_path = './Images/Seasonal/'+imgsize.lower()+'/'
		img_name = 'heatcontentanomaly-seasonal-ncei--'+imgw+'x'+imgh+'--'+yyyy+'-'+mm+'-00.png'
		tifimg_name = 'heatcontentanomaly-seasonal-ncei--981x490--'+yyyy+'-'+mm+'-00.tif'
		cmd = 'mv '+im1+' '+img_name
		subprocess.call(cmd,shell=True)
		im2 = "./temporary_cbar.eps"
		cbar_name = 'heatcontentanomaly-seasonal-ncei--'+yyyy+'-'+mm+'-00_colorbar.eps'
		cmd = 'mv '+im2+' '+cbar_name
		subprocess.call(cmd,shell=True)		
		origfile = glob.glob(path2orig+'heat_content_anomaly_0-700_'+yyyy+'-'+mm+'.png')[0]
		cmd = 'gdal_translate -of GTiff -a_srs WGS84 -a_ullr -180.0000 90.0000 180.0000 -90.0000 '+origfile+' tmp.tif'
		subprocess.call(cmd,shell=True)
		cmd = 'mv tmp.tif '+tifimg_name
		subprocess.call(cmd,shell=True)	
		cmd1 = 'zip heatcontentanomaly-seasonal-ncei--'+imgw+'x'+imgh+'--'+yyyy+'-'+mm+'-00.zip '+img_name+' '+tifimg_name+' '+cbar_name+' noaa_logo.eps '
		subprocess.call(cmd1,shell=True)
		cmd2 = 'mv heatcontentanomaly-seasonal-ncei--'+imgw+'x'+imgh+'--'+yyyy+'-'+mm+'-00.zip '+img_path
		subprocess.call(cmd2,shell=True)
		cmd3 = 'rm '+img_name+' '+cbar_name+' '+tifimg_name
		subprocess.call(cmd3,shell=True)
		
	if(imgsize == 'HD'):
		im1 = Image.open("temporary_map.png")
		imgw = str(im1.size[0])
		imgh = str(im1.size[1])
		draw = ImageDraw.Draw(im1)
		fntpath = './Fonts/Trebuchet_MS.ttf'
		fnt1 = ImageFont.truetype(fntpath, 25)
		draw.text((224,810), labeldate, (0,0,0), font=fnt1)
		fnt2 = ImageFont.truetype(fntpath, 14)
		#ttext = "Compared to 20th Century"
		#draw.text((224,838), ttext, (0,0,0), font=fnt2)
		
		#Add the colorbar
		cbar_orig = Image.open('NODC.colorbar_HD.png')
		bbox = (1,1,726,49)
		cbar_orig = cbar_orig.crop(bbox)
		old_size = cbar_orig.size
		new_size = (old_size[0]+2,old_size[1]+2)
		cbar_im = Image.new("RGB", new_size)
		cbar_im.paste(cbar_orig, ((new_size[0]-old_size[0])/2,
	                      (new_size[1]-old_size[1])/2))
		im1.paste(cbar_im, (596,865))
		
		fnt3 = ImageFont.truetype(fntpath, 48)
		text1 = "Cooler"
		text2 = "Warmer"
		draw.text((645,915), text1, (0,0,0), font=fnt3)
		draw.text((1100,915), text2, (0,0,0), font=fnt3)
		
		draw.polygon([(630,955), (615,945), (630,935)], fill="black", outline="black")
		draw.polygon([(1285,955), (1300,945), (1285,935)], fill="black", outline="black")
		
		img_path = './Images/Seasonal/'+imgsize.lower()+'/'
		img_name = 'heatcontentanomaly-seasonal-ncei--'+imgw+'x'+imgh+'hd--'+yyyy+'-'+mm+'-00.png'
		pngfile = img_path+img_name
		print "Saving "+pngfile
		im1.save(pngfile)
		
	
	if(imgsize == 'HDSD'):
		im1 = Image.open("temporary_map.png")
		imgw = str(im1.size[0])
		imgh = str(im1.size[1])
		draw = ImageDraw.Draw(im1)
		fntpath = './Fonts/Trebuchet_MS.ttf'
		fnt1 = ImageFont.truetype(fntpath, 25)
		draw.text((408,642), labeldate, (0,0,0), font=fnt1)
		fnt2 = ImageFont.truetype(fntpath, 14)
		#ttext = "Compared to 20th Century"
		#draw.text((408,670), ttext, (0,0,0), font=fnt2)
		
		#Add the colorbar
		cbar_orig = Image.open('NODC.colorbar_HD.png')
		bbox = (1,1,726,49)
		cbar_orig = cbar_orig.crop(bbox)
		old_size = cbar_orig.size
		new_size = (old_size[0]+2,old_size[1]+2)
		cbar_im = Image.new("RGB", new_size)
		cbar_im.paste(cbar_orig, ((new_size[0]-old_size[0])/2,
	                      (new_size[1]-old_size[1])/2))
		im1.paste(cbar_im, (596,740))
		
		fnt3 = ImageFont.truetype(fntpath, 48)
		text1 = "Cooler"
		text2 = "Warmer"
		draw.text((645,791), text1, (0,0,0), font=fnt3)
		draw.text((1100,791), text2, (0,0,0), font=fnt3)
		
		draw.polygon([(630,830), (615,820), (630,810)], fill="black", outline="black")
		draw.polygon([(1285,830), (1300,820), (1285,810)], fill="black", outline="black")
		
		img_path = './Images/Seasonal/'+imgsize.lower()+'/'
		img_name = 'heatcontentanomaly-seasonal-ncei--'+imgw+'x'+imgh+'hdsd--'+yyyy+'-'+mm+'-00.png'
		pngfile = img_path+img_name
		print "Saving "+pngfile
		im1.save(pngfile)