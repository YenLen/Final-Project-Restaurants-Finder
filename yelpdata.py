from pydoc import describe
from urllib import response
import requests
import json
import pandas as pd
import numpy as np 



API_KEY = "88C2OoOFgFaZGrlTPb6U9b5CIypKY9e-yz74Lh9RS1Ja6w_f_cudHi6FVS8L-OzwWsxSC0_vyHORkx2d_tCl2VFxSloBXKQLw5nk7IX_MJvYcru-P2GIcb0Q1MJcYnYx"
ENDPOINT = 'https://api.yelp.com/v3/businesses/search' #搜business資料
HEADERS = {'Authorization': 'bearer %s' %API_KEY}

location = input("Enter a city")

#define parameters
PARAMETERS = {'term':'restaurant',
'limit': 50,
'radius': 1000,
'location': location.replace(' ', '+')
}

response = requests.get(url = ENDPOINT, params= PARAMETERS, headers= HEADERS) #搜business資料
# response = requests.get(url = ENDPOINT, headers= HEADERS)
business_data = response.json()
# print(business_data)
for business in business_data['businesses']:
    print(business) #print all the cafe in ann arbor #搜business資料


