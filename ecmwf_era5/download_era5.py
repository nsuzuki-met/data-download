#!/usr/bin/env python
'''
  download_era5.py
    2025.08.08  Nobuyasu Suzuki
'''
#######################################
import os, datetime , cdsapi
#######################################



### SET START/END DATETIME (yyyymmdd) ###
start_date   = 20250531 #19910101
end_date     = 20250531 #20250131
#########################################


c            = cdsapi.Client()

area         = [ 120, 60, 20, 160 ]     # [North, West, South, East]

sdate        = datetime.datetime.strptime( str( start_date ) , '%Y%m%d' )
edate        = datetime.datetime.strptime( str( end_date )   , '%Y%m%d' )



while sdate <= edate:

    year     = sdate.strftime( '%Y' )
    month    = sdate.strftime( '%m' )
    day      = sdate.strftime( '%d' )

    out_path = './ERA5/' + sdate.strftime( '%Y%m' )
    os.makedirs( out_path, exist_ok = True )

    pl_data  = out_path + '/e5.pl.' + sdate.strftime( '%Y%m%d' ) + '.grb'
    sl_data  = out_path + '/e5.sl.' + sdate.strftime( '%Y%m%d' ) + '.grb'


#------------------------------------------------------------------------------
#   Download pressure level analysis data
#------------------------------------------------------------------------------
    print( pl_data )

    try:
        dataset = "reanalysis-era5-pressure-levels"
        request = {
            'product_type': ['reanalysis'],
            'variable': ['geopotential', 'relative_humidity', 'specific_humidity', 'temperature', 'u_component_of_wind', 'v_component_of_wind'],
            'year': [ year ],
            'month': [ month ],
            'day': [ day ],
            'time': [ '00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
                      '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
                      '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
                      '18:00', '19:00', '20:00', '21:00', '22:00', '23:00' ],
            'pressure_level': [ '1',   '2',   '3',   '5',   '7',
                                '10',  '20',  '30',  '50',  '70',
                                '100', '125', '150', '175', '200',
                                '225', '250', '300', '350', '400',
                                '450', '500', '550', '600', '650',
                                '700', '750', '775', '800', '825',
                                '850', '875', '900', '925', '950',
                                '975', '1000' ],
            'data_format': 'grib',
            'download_format': 'unarchived',
            'area': area
        }

        client = cdsapi.Client()
        client.retrieve( dataset, request, pl_data )

    except:
        print( f'  Download Failure : {pl_data} ' )


#------------------------------------------------------------------------------
#   Download single level analysis data
#------------------------------------------------------------------------------
    print( sl_data )

    try:
        dataset = "reanalysis-era5-single-levels"
        request = {
            'product_type': ['reanalysis'],
            'variable': [
                    '10m_u_component_of_wind','10m_v_component_of_wind','2m_dewpoint_temperature',
                    '2m_temperature','land_sea_mask','mean_sea_level_pressure',
                    'sea_ice_cover','sea_surface_temperature','skin_temperature',
                    'snow_depth','soil_temperature_level_1','soil_temperature_level_2',
                    'soil_temperature_level_3','soil_temperature_level_4','surface_pressure',
                    'volumetric_soil_water_layer_1','volumetric_soil_water_layer_2','volumetric_soil_water_layer_3',
                    'volumetric_soil_water_layer_4'
            ],
            'year': [ year ],
            'month': [ month ],
            'day': [ day ],
            'time': [ '00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
                      '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
                      '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
                      '18:00', '19:00', '20:00', '21:00', '22:00', '23:00' ],
            'data_format': 'grib',
            'download_format': 'unarchived',
            'area': area
        }

        client = cdsapi.Client()
        client.retrieve( dataset, request, sl_data )
    except:
        print( f'  Download Failure : {sl_data} ' )


#--- move forward by 1 day
    sdate = sdate + datetime.timedelta( days = 1 )
