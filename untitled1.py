# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 16:03:52 2020

@author: MEvans
"""

import ee

service_account = 'acd-app@appspot.gserviceaccount.com'
key = 'C:/Users/mevans/Downloads/acd-app-04a10fe38611.json'
credentials = ee.ServiceAccountCredentials(service_account, key)
ee.Initialize(credentials)

geometry = ee.Geometry.Point([-111.54765625, 35.4227332452855])
imageCollection = ee.ImageCollection("COPERNICUS/S2")

filtered = imageCollection.filterBounds(geometry)
test = ee.Image(filtered.first())
print(test.bandNames().getInfo())