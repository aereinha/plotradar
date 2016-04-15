'''
Created on Jun 17, 2015

@author: TONY REINHART
@license: MIT
'''

import numpy as np
import matplotlib.pyplot as plt
import pyart
import glob
import json
import urllib2
import urllib
import os.path
import zipfile
#
# def getradar(location,amika2):
#
#
#    if amika2:
#        while True:
#            ip = '192.168.0.228'
#    else:
#        while True:
#          ip = '192.168.0.208'
#     user = "operator"
#     remote = '/usr/iris_data/product_raw/'
#         #inputs = np.loadtxt('/Users/radar/kadata/operator.txt',dtype=np.str)
#     cmd = ["scp",\
#            +user, ip+":"+remote, location+'/.'
#


def loadradar(location='/Users/aereinha/radars'):

    '''Grab last raw file in location directory then load it using pyart.
    loadradar(locaiton)
    '''

    filenames = sorted(glob.glob(location))
    filename = filenames[-1]
    karadar = pyart.io.read(location)

    return karadar


def georeferenceradar(karadar,lat,lon,rot):

    '''Apply the new lat,lon, and azimuth to the radar data.
    georeferenceradar(radarobject,lat,lon,rot)
    '''

    karadar.longitude['data'] = np.array([lon])
    karadar.latitude['data']  = np.array([lat])
    karadar.azimuth['data'] = karadar.azimuth['data']+rot

    return karadar


def plotradar(karadar,countycode):

    '''Plot the radar data with shapefile as the background.
    plotradar(radarobject,countycode)
    '''

    shapefilepath="./shapefiles/"
    display = pyart.graph.RadarMapDisplay(karadar)

    display.plot_ppi_map('reflectivity', 0, vmin=0, vmax=70,
                     min_lon=karadar.longitude['data'][0]-1., max_lon=karadar.longitude['data'][0]+1.,
                     min_lat=karadar.latitude['data'][0]-1., max_lat=karadar.latitude['data'][0]+1.,
                     lat_0=karadar.latitude['data'][0],
                     lon_0=karadar.longitude['data'][0],shapefile=shapefilepath+'tl_2014_'+countycode+'_roads/tl_2014_'+countycode+'_roads')


    display.plot_range_ring(20., line_style='k-')
    display.plot_range_ring(40., line_style='k--')
    display.plot_range_ring(60., line_style='k-')
    display.plot_point(karadar.longitude['data'][0], karadar.latitude['data'][0])

    plt.show()

    return 0

def getcountycode(lon,lat):
    
    '''Get the fips county code for tiger road name. Requires internet connection.
    getcountycode(lon,lat)
    '''

    url = "http://data.fcc.gov/api/block/find?format=json&latitude="+str(lat)+"&longitude="+str(lon)

    response = urllib2.urlopen(url)

    response_dict = json.load(response)
    countycode= response_dict['County']['FIPS']

    return countycode

def checkcountyshapeexists(countycode):

    '''Checks for the tiger road shapfile. If it does not exists then it will download to use. Requires internet connection.
    checkcountyshapeexists(countycode)
    '''

    shapefilepath="./shapefiles/"
    if not(os.path.isdir(shapefilepath+'tl_2014_'+countycode+'_roads')):

        url = 'ftp://ftp2.census.gov/geo/tiger/TIGER2014/ROADS/tl_2014_'+countycode+'_roads.zip'
        filenames = urllib.urlretrieve(url,shapefilepath+'tl_2014_'+countycode+'_roads.zip')
        temp = zipfile.ZipFile(shapefilepath+'tl_2014_'+countycode+'_roads.zip')
        temp.extractall(shapefilepath+'tl_2014_'+countycode+'_roads')
        os.remove(shapefilepath+'tl_2014_'+countycode+'_roads.zip')


    return 0

def runplotting(location,lat,lon,rot):

    '''Runs the main part of the code
    runplotting(location of radar data, lat, lon, rot)
    '''

    karadar = loadradar(location)
    countycode = getcountycode(lon, lat)
    shapeexists = checkcountyshapeexists(countycode)
    karadar = georeferenceradar(karadar, lat, lon, rot)

    plotradar(karadar,countycode)
