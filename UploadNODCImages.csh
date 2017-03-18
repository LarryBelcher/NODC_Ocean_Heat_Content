#!/bin/csh

setenv pk $argv


cd ./Images/Seasonal/

#Upload all of the images
scp -i $pk ./620/* ubuntu@107.20.157.228:/var/www/Images/heatcontentanomaly-seasonal-ncei/620/
scp -i $pk ./1000/* ubuntu@107.20.157.228:/var/www/Images/heatcontentanomaly-seasonal-ncei/1000/
scp -i $pk ./diy/* ubuntu@107.20.157.228:/var/www/Images/heatcontentanomaly-seasonal-ncei/diy/
scp -i $pk ./hd/* ubuntu@107.20.157.228:/var/www/Images/heatcontentanomaly-seasonal-ncei/hd/
scp -i $pk ./hdsd/* ubuntu@107.20.157.228:/var/www/Images/heatcontentanomaly-seasonal-ncei/hdsd/

#Now for local cleanup
rm ./*/heatcontentanomaly*


cd ../Yearly/

#Upload all of the images
scp -i $pk ./620/* ubuntu@107.20.157.228:/var/www/Images/heatcontentanomaly-annual-ncei/620/
scp -i $pk ./1000/* ubuntu@107.20.157.228:/var/www/Images/heatcontentanomaly-annual-ncei/1000/
scp -i $pk ./diy/* ubuntu@107.20.157.228:/var/www/Images/heatcontentanomaly-annual-ncei/diy/
scp -i $pk ./hd/* ubuntu@107.20.157.228:/var/www/Images/heatcontentanomaly-annual-ncei/hd/
scp -i $pk ./hdsd/* ubuntu@107.20.157.228:/var/www/Images/heatcontentanomaly-annual-ncei/hdsd/

#Now for local cleanup
rm ./*/heatcontentanomaly*

endif
exit