import requests
import pyproj
import sys
import logging
import pandas as pd
import json
import time
import csv
import os
import numpy as np


logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

#logger.info("Get all data from listing api : SUCCESS")

file_path = "./2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv"
base_url_reverse_csv = "https://api-adresse.data.gouv.fr/reverse/csv/"

#compute lambert and wgs84
lambert = pyproj.Proj('+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs')
wgs84 = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

split_number = 8


def get_lat_long(X, Y, lambert, wgs84):
  lon, lat = pyproj.transform(lambert, wgs84, X, Y)
  return lon, lat

#get the name of the city from the response returned by the reverse api
def get_city(response_splitter, all_city):
    for index, element in enumerate(response_splitter):
        if 0 == index:
            continue
        city = element.split(',')[18]
        all_city.append(city)
        
    return all_city


def process_file(file_path):
    logger.info("Start process File...")     
    try:
        df = pd.read_csv(file_path, sep = ';')
    except FileNotFoundError:
        logger.error("File {} does not exist".format(file_path))
        raise
    except:
        logger.error("Error while reading {}".format(file_path))
        raise
    
    #remove lines with None value
    df = df.dropna()
    
    #create Lat and Lon columns
    lon_list = []
    lat_list = []
    for value_x, value_y in zip(df['X'], df['Y']):
        lon, lat = get_lat_long(value_x, value_y, lambert, wgs84)
        lon_list.append(round(lon, 3))
        lat_list.append(round(lat, 3))
     
    df['lat'] = lat_list
    df['lon'] = lon_list
    
    
    #split dataframe into chunck of dataframe
    chunks = np.array_split(df, split_number)
    
    i = 0    
    all_city = []
    for chunk in chunks:
        i +=1
        print("dataframe numero = ", i)
        chunk.to_csv('test.csv', sep=',', encoding='utf-8', index = False)
        
        files = {'dataa': open('test.csv', 'rb')}
        response = requests.post(base_url_reverse_csv, files=files)
        if response.status_code != 200:
            logger.error("Response NOT OK from the api reverse !")
            return 
        
        print("response ok")
        
        response_splitter = response.text.splitlines()
        all_city = get_city(response_splitter, all_city)
        
    df['city'] = all_city
    df.to_csv('operators.csv', sep=',', encoding='utf-8', index = False)
    logger.info("End process file !") 


process_file(file_path)