import requests
import pyproj
import sys
import logging
import pandas as pd
import numpy as np
import os


logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

base_url_reverse_csv = "https://api-adresse.data.gouv.fr/reverse/csv/"

#compute lambert and wgs84
lambert = pyproj.Proj('+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs')
wgs84 = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

#Fix the number of dataframe chunk
split_number = 8

#Compute the latitude and the longitude
def get_lat_long(X, Y):
  lon, lat = pyproj.transform(lambert, wgs84, X, Y)
  return lon, lat

#get the name of the city from the response returned by reverse API
def get_city(response_splitter, all_city):
    for index, element in enumerate(response_splitter):
        if 0 == index:
            continue
        city = element.split(',')[18]
        all_city.append(city)
        
    return all_city

def process_file(input_file, output_file, df_chunk_file):
    logger.info("Start process File...")     
    try:
        df = pd.read_csv(input_file, sep = ';')
    except FileNotFoundError:
        logger.error("File {} does not exist".format(input_file))
        return
    except:
        logger.error("Error while reading {}".format(input_file))
        return
    
    #remove lines with None value
    df = df.dropna()
    
    #create Lat and Lon columns
    lon_list = []
    lat_list = []
    for value_x, value_y in zip(df['X'], df['Y']):
        lon, lat = get_lat_long(value_x, value_y)
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
        logger.info("Dataframe number : {} ".format(i))
        
        #save the chunk dataframe file (who will be sent to the API)
        chunk.to_csv(df_chunk_file, sep=',', encoding='utf-8', index = False)       

        try:
            files = {'data': open(df_chunk_file, 'rb')} 
        except FileNotFoundError:
            logger.error("Error while opening {}".format(df_chunk_file))
            return

        try:
            response = requests.post(base_url_reverse_csv, files=files)
        except:
            logger.error("Error while sending POST request to reverse api")
            return
            
        if response.status_code != 200:
            logger.info("Response NOT OK from API reverse !")
            logger.info("This is the response from API reverse : {}".format(response.text))
            return 
        else:
            logger.info("Response OK from API reverse !")
            response_splitter = response.text.splitlines()
            all_city = get_city(response_splitter, all_city)
        
    df['city'] = all_city
    df.to_csv(output_file, sep=';', encoding='utf-8', index = False)
    logger.info("End process file. The Output file is generated !")    
    return 1

