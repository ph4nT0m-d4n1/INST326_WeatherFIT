"""WeatherFIT, an INST326 project
Group Members:
    Danny Mallya
    Bella Konrad
    Jaden Shin
    Marvin Gomez Molina

Instructor: Professor Cruz
Assignment: Final Project
Date: 05/10/2025

This program reads data from a weather api and determines the upcoming forecast. 
The app will then suggest clothing that would be appropriate for the weather condtions.
"""
#install the following required packages: use pip or pip3 depending on your system
#pip install openmeteo-requests
#pip install requests-cache retry-requests

# import libraries for API requests and caching
import openmeteo_requests  # library for accessing the Open-Meteo weather API
import requests_cache      # library for caching API requests to avoid rate limiting
import requests      

# import libraries for command line argument parsing and system interactions
import argparse
import sys

# import libraries for retry functionality and date handling
from retry_requests import retry  # handles retrying failed requests automatically
from datetime import datetime

class Forecast():
    """This class is used to get the weather forecast for a given location and date.
        Attributes:
            date (str): the date and time for the forecast in format YYYY-MM-DD, HH:MM
            temperature (float): the temperature in fahrenheit for the day
            feels_like (float): what the temperature feels like due to humidity, wind, etc.
            humidity (float): the humidity percentage for the day
            precipitation_chance (float): chance of precipitation for the day as a percentage
            cloud_coverage (float): percentage of cloud coverage for the day
            wind_speed (float): the wind speed in miles per hour for the day
            rain (float): amount of rain in inches
            showers (float): amount of showers in inches
            snowfall (float): amount of snowfall in inches
    """
    def __init__(self, 
                date=None, 
                temperature=None,
                max_temperature=None,
                min_temperature=None,
                feels_like=None,
                max_feels_like=None,
                min_feels_like=None,
                humidity=None, 
                precipitation_chance=None, 
                cloud_coverage=None, 
                wind_speed=None,
                rain=None,
                showers=None,
                snowfall=None
            ):
        self.date = date
        self.temperature = temperature
        self.max_temperature = max_temperature
        self.min_temperature = min_temperature
        self.feels_like = feels_like
        self.max_feels_like = max_feels_like
        self.min_feels_like = min_feels_like
        self.humidity = humidity
        self.precipitation_chance = precipitation_chance
        self.cloud_coverage = cloud_coverage
        self.wind_speed = wind_speed
        self.rain = rain
        self.showers = showers
        self.snowfall = snowfall
    
    def __repr__(self):
        # basic weather information
        weather_info = (f"Date & Time: {self.date}\n\
                \nThe current weather:\
                \nTemperature: {round(self.temperature)}°F\nFeels Like: {round(self.feels_like)}°F\nHumidity: {round(self.humidity)}%\
                \nPrecipitation Chance: {round(self.precipitation_chance)}%\nWind Speed: {round(self.wind_speed)} mph\
                \nCloud Coverage: {round(self.cloud_coverage)}%\n \
                \nToday's High: {round(self.max_temperature)}°F\nToday's Low: {round(self.min_temperature)}°F\
                \nFeels Like High: {round(self.max_feels_like)}°F\nFeels Like Low: {round(self.min_feels_like)}°F\n")
        
        # only add precipitation information if it exists
        if self.rain > 0:
            weather_info += f"Rain: {self.rain} inches\n"
        if self.showers > 0:
            weather_info += f"Showers: {self.showers} inches\n"
        if self.snowfall > 0:
            weather_info += f"Snowfall: {self.snowfall} inches\n"
        return weather_info

    def get_forecast(self, latitude, longitude):
        """Fetches the current weather forecast data from Open-Meteo API.

        This method makes an API call to Open-Meteo with the given coordinates,
        then populates the Forecast object's attributes with the retrieved data.

        Args:
            latitude (float): the latitude of the location
            longitude (float): the longitude of the location
        """
        # the code below is provided by the Open-Meteo API documentation
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600) # cache requests for 1 hour to reduce API calls
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2) # retry up to 5 times if a request fails
        openmeteo = openmeteo_requests.Client(session = retry_session)
        
        # define the API endpoint and parameters
        # the order of variables in the "current" list is important as they map to Variables(index)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "models": "best_match",  # using the best available weather model
            "current": ["temperature_2m",
                        "relative_humidity_2m",
                        "precipitation_probability",
                        "wind_speed_10m",
                        "cloud_cover",
                        "apparent_temperature",
                        "rain",
                        "showers",
                        "snowfall"
                    ],
            "daily": ["temperature_2m_max",
                      "temperature_2m_min",
                      "apparent_temperature_max",
                      "apparent_temperature_min"
                    ], 
            "timezone": "auto",  # automatically detect timezone based on coordinates
            "forecast_days": 1,  # only retrieve forecast for today
            "wind_speed_unit": "mph",
            "temperature_unit": "fahrenheit",
            "precipitation_unit": "inch"
        }
        
        responses = openmeteo.weather_api(url, params=params) # make the API request
        response = responses[0] # process the first response (only one location was requested)

        print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}\n") # print the timezone information
        
        current = response.Current() # extract current weather data
        daily = response.Daily() # extract daily weather data
        
        self.date = datetime.now().strftime("%Y-%m-%d, %H:%M") # get and set the current date and time
        
        # assign all weather variables from the API response
        # the index corresponds to the order in the "current" list in params
        self.temperature = current.Variables(0).Value()
        self.humidity = current.Variables(1).Value()
        self.precipitation_chance = current.Variables(2).Value()
        self.wind_speed = current.Variables(3).Value()
        self.cloud_coverage = current.Variables(4).Value()
        self.feels_like = current.Variables(5).Value()
        self.rain = current.Variables(6).Value()
        self.showers = current.Variables(7).Value() 
        self.snowfall = current.Variables(8).Value()
        # the index corresponds to the order in the "daily" list in params
        # using [0] to get the first value since daily returns a numpy array
        self.max_temperature = daily.Variables(0).ValuesAsNumpy()[0]
        self.min_temperature = daily.Variables(1).ValuesAsNumpy()[0]
        self.max_feels_like = daily.Variables(2).ValuesAsNumpy()[0]
        self.min_feels_like = daily.Variables(3).ValuesAsNumpy()[0]
    
    def get_weather_summary(self):
        """Generates a summary of the current weather conditions.
        
        Returns:
            str: a simple readable summary of the current weather conditions.
        """
        pass
    
    def get_comfort_index(self):
        """Calculates a comfort index based on temperature, humidity, and wind speed.
        
        Returns:
            float: a comfort index value that indicates how comfortable the weather is.
        """
        pass
    
    def compare_with_yesterday(self, yesterday_forecast):
        """Compares today's forecast with yesterday's forecast.
        
        Args:
            past_weather (Forecast): a Forecast object containing yesterday's weather data.
        
        Returns:
            str: a comparison of today's weather with yesterday's weather.
        """
        pass
        


def get_location(city:str, state:str=None, max_results=10):
    """Gets the geographic coordinates for a given city and (optionally) state.
    
    This function makes a request to the Open-Meteo geocoding API to convert
    a city name (and optionally a state name) into latitude and longitude coordinates.
    
    Args:
        city (str): the name of the city
        state (str, optional): the name of the State. Defaults to None.
        max_results (int, optional): the maximum number of results to return. Defaults to 10.
    
    Returns:
        tuple: A tuple containing (latitude, longitude) coordinates, or None if failed
    """
    # replace spaces with plus signs for the URL
    city = city.replace(" ", "+")
    
    geo_request = (f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count={max_results}&language=en&format=json")
    geo_location = requests.get(geo_request)
    
    # check if the request was successful
    if geo_location.status_code == 200:
        # parse the JSON response
        data = geo_location.json()
        
        # if a state was specified, try to find a match with both city and state
        for result in data['results']:
            if state != None and result['admin1'] == state:
                latitude = result['latitude']
                longitude = result['longitude']
                print(f"Location: {result['name']}, {result['admin1']}")
                return latitude, longitude
        
        # if no specific match or no state was specified, use the first result
        first_result = data['results'][0]
        latitude = first_result['latitude']
        longitude = first_result['longitude']
        
        print(f"First Location: {first_result['name']}, {first_result['admin1']}")
        return latitude, longitude
        
    elif geo_location.status_code != 200:
        # handle API errors
        print(f"Error: {geo_location.status_code}")
        return None

if __name__ == "__main__":
    # create a new Forecast object
    weather = Forecast()
    
    location = get_location("College Park", "Maryland") # example location, can be replaced with user input
    weather.get_forecast(location[0], location[1]) # fetch the current weather forecast for the location
    
    print(weather)
