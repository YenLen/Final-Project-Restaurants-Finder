# from final import API_KEY
import pandas as pd
import numpy as np
import requests
import googlemaps
import json
import time
from datetime import datetime
from pprint import pprint
from geopy.geocoders import Nominatim



#GOOGLE MAP
GOOGLE_API_KEY = 'AIzaSyBaGXPgQsHYD4jlpgsQ5SzbptWLw6VPvn8'
map_clinet = googlemaps.Client(GOOGLE_API_KEY)

#YELP FUSION
YELP_API_KEY = "88C2OoOFgFaZGrlTPb6U9b5CIypKY9e-yz74Lh9RS1Ja6w_f_cudHi6FVS8L-OzwWsxSC0_vyHORkx2d_tCl2VFxSloBXKQLw5nk7IX_MJvYcru-P2GIcb0Q1MJcYnYx"
ENDPOINT = 'https://api.yelp.com/v3/businesses/search' #search business information
HEADERS = {'Authorization': 'bearer %s' %YELP_API_KEY}

   
def save_cache(cache, filename):
    """
    Saves the dic of restaurant list
    """
    cache_file = open(filename, 'w')
    file_contents = json.dumps(cache)
    cache_file.write(file_contents)
    cache_file.close()



def travel_time(user_loaction, restaurants):
    """
    Print the travel time from user's input address to the chosen restaurant 
    """
    # user input the address
    # user_loaction = input('enter a location \n')
    user_loaction_url = user_loaction.replace(' ', '+')

    # the output of the restaurants
    # restaurants = input('enter a restaurant \n')
    restaurants_url = restaurants.replace(' ', '+')

    # base google map url
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&'

    # get response
    r = requests.get(url + "origins=" + user_loaction_url +
                     "&destinations=" + restaurants_url + "&key=" + GOOGLE_API_KEY)

    # return time as text a
    travel_time = r.json()['rows'][0]['elements'][0]['duration']['text']

    # print the travel_time
    print(f'\nThe total travel time from {user_loaction} to {restaurants} is', travel_time)


def coordinate_generator(address):
    """
    Transfer input address to coordinate for Google Map API
    """
    geolocator = Nominatim(user_agent="my app")
    location = geolocator.geocode(address)
    print('\nThe location you are search is ' + location.address)
    print('\nThe coordinates used for restaurant search: ')
    print(location.latitude, location.longitude)
    return location



# location = ('-8.705833, 115.261377')
# location = (coordinate_generator('ann arbor'))
def restaurant_review(place_id):
        detail_url = "https://maps.googleapis.com/maps/api/place/details/json?place_id="
        response = requests.get(detail_url + place_id + '&rating=5&key=' + GOOGLE_API_KEY)
        results = response.json()
        restaurant_review = []

        for i in range(len(results['result']['reviews'])):
            review_rating = results['result']['reviews'][i]['rating']
            text = results['result']['reviews'][i]['text']
            restaurant_review.append(
                {
                    'rating': review_rating,
                    'text': text
                }
            )
        # df = pd.DataFrame(restaurant_review) #list the review in table
        return restaurant_review 



def restaurant_list(location):
    """
    Generate restaurant list from Google Map API
    """
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="

    googlemap_data = []  # list of restaurants in near the location within 1 km
    response = requests.get(url + location + '&radius=1000&type=restaurant&key=' + GOOGLE_API_KEY)
    results = response.json()

    for result in results['results']:
        restaurant_info = {}
        restaurant_info['price_level'] = result['price_level']
        restaurant_info['name'] = result['name']
        restaurant_info['rating'] = result['rating']
        restaurant_info['lat'] = result['geometry']['location']['lat']
        restaurant_info['lng'] = result['geometry']['location']['lng']
        restaurant_info['place_id'] = result['place_id']
        googlemap_data.append(restaurant_info)
    return googlemap_data


def yelp_restaurant_list(location):
    """
    Generate restaurant list from Yelp Fusion API
    """
    #define parameters
    PARAMETERS = {'term':'restaurant',
    'limit': 50,
    'radius': 1000,
    'location': location.replace(' ', '+')
    }

    response = requests.get(url = ENDPOINT, params= PARAMETERS, headers= HEADERS) #搜business資料
    yelp_results = response.json()

    yelp_data = []
    for yelp_result in yelp_results['businesses']:
        yelp_restaurant_info = {}
        yelp_restaurant_info['name'] = yelp_result['name']
        yelp_restaurant_info['rating'] = yelp_result['rating']
        yelp_data.append(yelp_restaurant_info)
    return yelp_data



    
def main():

    # Ask the user to enter a city
    address = input("Enter a city: ")
    address_laglug = coordinate_generator(address)
    
    yelp_restaurants = yelp_restaurant_list(address)
    # Save Yelpp data
    save_cache(yelp_restaurants, 'Yelp_' + address + '.json')

    #Transfer address to coordinate for Google Map API
    coordinate_str = str(address_laglug.latitude) + ', '+  str(address_laglug.longitude)
    restaurants = restaurant_list(coordinate_str)
    for restaurant in restaurants:
        review = restaurant_review(restaurant['place_id'])
        restaurant['review'] = review
        # print(restaurant['name'])
    # Save Google Map data
    save_cache(restaurants, 'GoogleMap_' + address + '.json') 


    # Ask Goolge Map or Yelp?
    preference = input('Choose a source between Google Map or Yelp? (Google/Yelp) ')
    if preference == 'Yelp':
        print('\n$')
        for restaurant in yelp_restaurants:
            print(restaurant['name'] + ' rating: ' + str(restaurant['rating']))
    else:
        price_level_exist = False
        print('\n$')
        for restaurant in restaurants:
            if restaurant['price_level'] == 1: #print price_level = 1
                price_level_exist = True
                print(restaurant['name'] + ' rating: ' + str(restaurant['rating']))
        if price_level_exist == False:
            print('No restaurant found.')


        price_level_exist = False
        print('\n$$') 
        for restaurant in restaurants:
            if restaurant['price_level'] == 2: #print price_level = 2
                price_level_exist = True
                print(restaurant['name'] + ' rating: ' + str(restaurant['rating']))
        if price_level_exist == False:
            print('No restaurant found.')


        price_level_exist = False
        print('\n$$$') 
        for restaurant in restaurants:
            if restaurant['price_level'] == 3: #print price_level = 3
                price_level_exist = True
                print(restaurant['name'] + ' rating: ' + str(restaurant['rating']))
        if price_level_exist == False:
            print('No restaurant found.')

        price_level_exist = False
        print('\n$$$$') 
        for restaurant in restaurants:
            if restaurant['price_level'] == 4: #print price_level = 4
                price_level_exist = True
                print(restaurant['name'] + ' rating: ' + str(restaurant['rating']))
        if price_level_exist == False:
            print('No restaurant found.')


        want_restaurant = input('Which restaurant would you like to go? ') # Ask user to type in a restaurant name from the list
        for restaurant in restaurants:
            if want_restaurant == restaurant['name']:
                print('==========================================================')
                travel_time(address, want_restaurant)
                print('==========================================================')
                print('Here are some reviews: ')
                for reviews in restaurant['review']:
                    print('【Rating: ' + str(reviews['rating']) + '】\n'+ reviews['text'] + '\n')
                


if __name__ == '__main__':
    main()