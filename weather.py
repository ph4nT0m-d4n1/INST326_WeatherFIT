"""WeatherFit, an INST326 project
Group Members:
    Danny Mallya
    Bella Konrad
    Jaden Shin
    Marvin Gomez Molina

Professor Cruz
4/20/25

This program reads data from a weather api and determines the upcoming forecast. 
The app will then suggest clothing that would be appropriate for the weather condtions.
"""
#install the following required packages: use pip or pip3 depending on your system
#pip install openmeteo-requests
#pip install requests-cache retry-requests numpy pandas

import openmeteo_requests

import requests_cache
import requests
from retry_requests import retry


class Forecast():
    """This class is used to get the weather forecast for a given location and date.
        Attributes:
            date (str): the date for the forecast
            temperature (float): the temperature in fahrenheit for the day
            humidity (float): the humidity percentage for the day
            precipitation_chance (float): chance of precipitation for the day
            precipitation_type (str): type of precipitation for the day (if any)
            cloud_coverage (float): percentage of cloud coverage for the day
            wind_speed (float): The wind speed in miles per hour for the day
    """
    
    def __init__(self, date=None, temperature=None, humidity=None, precipitation_chance=None, cloud_coverage=None, wind_speed=None):
        self.date = date
        self.temperature = temperature
        self.humidity = humidity
        self.precipitation_chance = precipitation_chance
        self.cloud_coverage = cloud_coverage
        self.wind_speed = wind_speed
    
    def __repr__(self):
        return f"The current forecast: \
                \nTemperature: {self.temperature}\nHumidity: {self.humidity}\nPrecipitation: {self.precipitation_chance}\
                \nWind Speed: {self.wind_speed}\nCloud Coverage: {self.cloud_coverage}\n"

    def get_current_forecast(self, latitude, longitude):
        """This function gets the data from the api

            Args:
                latitude (float): the latitude of the location
                longitude (float): the longitude of the location
        """
        # setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)
        
        # the order of variables in hourly or daily is important to assign them correctly
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "models": "best_match",
            "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m", "cloud_cover"],
            "timezone": "auto",
            "forecast_days": 1,
            "wind_speed_unit": "mph",
            "temperature_unit": "fahrenheit",
            "precipitation_unit": "inch"
        }
        responses = openmeteo.weather_api(url, params=params)
        
        response = responses[0]
        # print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}\n")
        
        current = response.Current()
        
        self.temperature = current.Variables(0).Value()
        self.temperature = current.Variables(0).Value()
        self.humidity = current.Variables(1).Value()
        self.precipitation_chance = current.Variables(2).Value()
        self.wind_speed = current.Variables(3).Value()
        self.cloud_coverage = current.Variables(4).Value()
        
def get_location(city:str, state:str=None, max_results=10):
    """This function gets the location from the user
        Args:
            city (str): the name of the city
            max_results (int): the maximum number of results to return
            state (str): the name of the State
        Returns:
            latitude (float): the latitude of the location
            longitude (float): the longitude of the location
    """
    city = city.replace(" ", "+")
    geo_location = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count={max_results}&language=en&format=json")
    
    if geo_location.status_code == 200:
        print("Location found!")
        data = geo_location.json()
        for result in data['results']:
            if state != None and result['admin1'] == state:
                latitude = result['latitude']
                longitude = result['longitude']
                print(f"Location coordinates: {latitude}°N {longitude}°E")
                return latitude, longitude
    
        first_result = data['results'][0]
        latitude = first_result['latitude']
        longitude = first_result['longitude']
        
        print(f"Coordinates for first result: {latitude}°N {longitude}°E")
        return latitude, longitude
        
    elif geo_location.status_code != 200:
        print(f"Error: {geo_location.status_code}")
        return None

if __name__ == "__main__":
    weather = Forecast()
    location = get_location("College Park", "Maryland") 
    weather.get_current_forecast(location[0], location[1]) 
    print(weather)
