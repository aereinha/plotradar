import geopy as gp
import numpy as np
from geopy.distance import vincenty


def calcgrid(r1lat,r1lon,r2lat,r2lon,baselineangle):
    
    d= gp.distance.vincenty((r1lat,r1lon),(r2lat,r2lon))
    lengths=(d/2.)/np.cos(np.radians(45))
    r1 = gp.Point(r1lat,r1lon)
    finalp=lengths.destination(point=r1,bearing=baselineangle-45.0)
    
    return finalp.longitude,finalp.latitude
    