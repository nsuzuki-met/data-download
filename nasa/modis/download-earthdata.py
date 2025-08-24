#!/usr/bin/env python
'''
  download-earthdata.py
    2025.08.19  Nobuyasu Suzuki
'''
#######################################
import os, datetime
from   dateutil.relativedelta import relativedelta
import earthaccess
import geopandas              as     gpd
from   shapely.geometry       import box
#######################################




#==============================================================================
#
#   main
#
#==============================================================================
def main( shortname        : str   = "MOD21A2"
        , start_date       : str   = "2000-01-01"
        , end_date         : str   = "2025-08-17"
        , west             : float =  92.0
        , east             : float = 142.0
        , south            : float = -12.0
        , north            : float =  29.0
        , output_directory : str   = './output'
        ) -> None:

    aoi            = box( west, north, east, south )
    gdf            = gpd.GeoDataFrame( { "geometry" : [ aoi ] }, crs = "EPSG:4326" )

    earthaccess.login()

    search         = earthaccess.search_data( short_name   = shortname
                                            , bounding_box = aoi.bounds
                                            , temporal     = ( start_date, end_date )
                                            )
                                            #, provider = "LP DAAC"

    earthaccess.download( search , output_directory )



#==============================================================================
if __name__ == "__main__":

    '''
    Setting Parameter
    '''
    shortName      = "MYD21A1D" #"MOD09A1"
    dir_path       = '/work10/Share/Satellite_data/NASA/MODIS'  # save directory
    start_year     = 2011
    end_year       = 2025

    ''' Write the end date here. In the loop process, if that date is exceeded, it will be automatically replaced and the loop will be terminated. '''
    start_date     = datetime.datetime( 2000,  2, 25 )
    end_date       = datetime.datetime( 2025,  5, 31 )
    ''' '''

    for year in range( start_year, end_year+1 ):        # Start loop
        sdate      = datetime.datetime( year,  1,  1 )  # target start date
        sdate      = start_date if sdate < start_date else sdate
        edate      = datetime.datetime( year, 12, 31 )  # target end date
        edate      = end_date if edate > end_date or sdate > edate else edate
        print( f'   DATE : {sdate} - {edate}' )
        main( shortname        = shortName
            , start_date       = sdate
            , end_date         = edate
            , west             = 78.0   # 92.00
            , east             = 85.0   #142.00
            , south            =  5.0   #-12.00
            , north            = 10.0   # 29.00
            , output_directory = f'{dir_path}/{shortName}/{sdate.strftime( "%Y" )}'
            )
