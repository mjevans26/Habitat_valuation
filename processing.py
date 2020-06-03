# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 15:38:25 2019

@author: MEvans
"""

import pandas as pd
import rasterio as rio

con = pd.read_csv("C:/Users/mevans/OneDrive - Defenders of Wildlife/repos/Tortoise_Prioritization/data/raw/connectivity_varlands.txt", header = 1, sep = ",")
suit = pd.read_csv("C:/Users/mevans/OneDrive - Defenders of Wildlife/repos/Tortoise_Prioritization/data/raw/suithab_varlands.txt", header = 1, sep = ",")

suit.columns = ["ID", "SuitabilityTif", "X", "Y", 'Suitability']
con.columns = ["ID", "ConnectivityTif", "X", "Y", "Connectivity"]

join = con.join(suit, on = "ID", how = 'left', lsuffix = 'conn', rsuffix = 'suit')

minimum = join['Connectivity'].min()
maximum = join['Connectivity'].max()

join.assign(ScaledConn = (join['Connectivity'] - minimum)/(maximum - minimum))

print(join.head())

del([con, suit, maximum, minimum])

habsuit = rio.open("H:/Shared drives/Center_Conservation_Innovation/Projects/Desert_Tortoise/Extract_HabSuit1.tif").read(masked = True)
connect = rio.open("H:/Shared drives/Center_Conservation_Innovation/Projects/Desert_Tortoise/Extract_Connectivity1.tif").read(masked = True)
min_conn = connect.min()

max_conn = connect.max()
scaledconn = (connect - min_conn)/(max_conn - min_conn)   
print(min_conn)

    