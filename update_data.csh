#!/bin/csh


cd ./Data

rm *.nc

wget http://data.nodc.noaa.gov/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/NETCDF/heat_content/heat_content_anomaly_0-700_yearly.nc

wget http://data.nodc.noaa.gov/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/NETCDF/heat_content/heat_content_anomaly_0-700_seasonal.nc
