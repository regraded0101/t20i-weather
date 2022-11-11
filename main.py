import sys
from weather_au import api

from datetime import datetime
from meteostat import Point, Daily

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="my_request")

import pandas as pd

def read_t20_matches(data_filepath = 't20i-matches.csv'):

    matches_df = pd.read_csv(data_filepath)
    matches_df = matches_df[['Date', 'Stadium']]
    matches_df['Date'] = pd.to_datetime(matches_df['Date'], format = '%d-%b-%Y')
    return matches_df

def get_lat_long():
        
    location_dict = {}
    matches_df = read_t20_matches()
    for i, ground in enumerate(matches_df['Stadium'].unique()):
        location = geolocator.geocode(ground)  
        location_dict[ground] = [location.latitude, location.longitude]  


    location_df = pd.DataFrame.from_dict(location_dict, orient = 'index').reset_index()
    location_df.columns = ['Stadium', 'latitude', 'longitude']

    return location_df    

def get_prcp_data():
    
    matches_df = read_t20_matches()
    location_df = get_lat_long()

    matches_df = matches_df.merge(location_df, how = 'left', on = 'Stadium')

    prcp_list = []

    for i in range(0,len(matches_df)):
        start_date = matches_df['Date'][i]
        end_date = start_date
        latitude = matches_df['latitude'][i]
        longitude = matches_df['longitude'][i]

        ground_point = Point(latitude, longitude)
        data = Daily(ground_point, start_date, end_date)

        prcp_value = data.fetch()['prcp'][0]
        prcp_list.append([matches_df['Stadium'][i], start_date, prcp_value])
        

    prcp_df = pd.DataFrame(prcp_list)
    prcp_df.columns = ['Ground', 'Date', 'Precipitation']

    return(prcp_df)

if __name__ == '__main__':
    out = get_prcp_data()
    print(out)
    out