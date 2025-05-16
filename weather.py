"""WeatherFIT, an INST326 project
Group Members:
    Danny Mallya
    Bella Konrad
    Jaden Shin
    Marvin Gomez Molina

Instructor: Professor Cruz
Assignment: Final Project
Date: 05/10/2025

This module reads data from a weather API and determines the upcoming forecast. 
"""
# install the following required packages: use pip or pip3 depending on your system
# pip install openmeteo-requests
# pip install requests-cache retry-requests

# import libraries for API requests and caching
import openmeteo_requests  # library for accessing the Open-Meteo weather API
import requests_cache      # library for caching API requests to avoid rate limiting
import requests            # library for making HTTP requests

# import libraries for retry functionality and date handling
from retry_requests import retry  # handles retrying failed requests automatically
from datetime import datetime

_bold = "\033[1m" # ANSI escape code for bold text
bold_ = "\033[0;0m" # ANSI escape code to reset text formatting

class Forecast():
    """This class is used to get the weather forecast for a given location and date.
        Args:
            latitude (float): the latitude of the location
            longitude (float): the longitude of the location
            
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
            uv_index_max (float): highest uv index rating for the day
        
        Side Effects:
            makes a request to the Open-Meteo weather API
    """
    def __init__(self, latitude, longitude):
        # the three lines of code below are provided directly by the Open-Meteo API documentation
        # additionally, much of the structure of the code in this function follows conventions outlined in the Open-Meteo API docs
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600) # cache requests for 1 hour to reduce API calls
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2) # retry up to 5 times if a request fails
        openmeteo = openmeteo_requests.Client(session = retry_session)
        
        # define the API endpoint and parameters
        # the order of variables in the "current" list is important as they map to Variables(index)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude, # use the latitude and longitude from the get_location function
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
                      "apparent_temperature_min",
                      "uv_index_max"
                    ], 
            "timezone": "auto",  # automatically detect timezone based on coordinates
            "forecast_days": 1,  # retrieve forecast for today
            "wind_speed_unit": "mph", # adjust wind speed unit to miles per hour
            "temperature_unit": "fahrenheit", # adjust temperature unit to fahrenheit
            "precipitation_unit": "inch" # adjust precipitation unit to inches
        }
        
        responses = openmeteo.weather_api(url, params=params) # make the API request
        response = responses[0] # process the first response (only one location was requested)
        
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
        self.uv_index_max = daily.Variables(4).ValuesAsNumpy()[0]
    
    def __repr__(self):
        """This function prints out the weather statistics that were initialized in the init function

            Returns:
                A string of the weather statistics like temperature, precipitation chance, etc
        """
        # basic weather information
        weather_info = (f"{_bold}Date & Time:{bold_} {self.date}\n\
                \n{_bold}The Current Weather:{bold_}\
                \nTemperature: {round(self.temperature)}°F\nFeels Like: {round(self.feels_like)}°F\nHumidity: {round(self.humidity)}%\
                \nPrecipitation Chance: {round(self.precipitation_chance)}%\nWind Speed: {round(self.wind_speed)} mph\
                \nCloud Coverage: {round(self.cloud_coverage)}%\n \
                \nToday's High: {round(self.max_temperature)}°F\nToday's Low: {round(self.min_temperature)}°F\
                \nFeels Like High: {round(self.max_feels_like)}°F\nFeels Like Low: {round(self.min_feels_like)}°F\
                \nUV Index: {round(self.uv_index_max)}\n")
        
        # only add precipitation information if it exists
        if self.rain > 0:
            weather_info += f"Rain: {self.rain} inches\n"
        if self.showers > 0:
            weather_info += f"Showers: {self.showers} inches\n"
        if self.snowfall > 0:
            weather_info += f"Snowfall: {self.snowfall} inches\n"
            
        return weather_info

    def get_past_forecast(self, latitude, longitude):
        """Fetches the current weather forecast data from Open-Meteo API.

        This method makes an API call to Open-Meteo with the given coordinates,
        then populates the Forecast object's attributes with the retrieved data.

        Args:
            latitude (float): the latitude of the location
            longitude (float): the longitude of the location
        
        Returns:
            tuple: a tuple containing various weather variables for yesterday's weather
            
        Side Effects:
            makes a request to the Open-Meteo weather API
        """
        # the three lines of code below are provided directly by the Open-Meteo API documentation
        # additionally, much of the structure of the code in this function follows conventions outlined in the Open-Meteo API docs
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600) # cache requests for 1 hour to reduce API calls
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2) # retry up to 5 times if a request fails
        openmeteo = openmeteo_requests.Client(session = retry_session)
        
        # define the API endpoint and parameters
        # the order of variables in the "current" list is important as they map to Variables(index)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude, # use the latitude and longitude from the get_location function
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
                      "apparent_temperature_min",
                      "uv_index_max"
                    ], 
            "timezone": "auto",  # automatically detect timezone based on coordinates
            "past_days": 1, # retrieve data for the past day for comparison
            "forecast_days": 1,  # retrieve forecast for today
            "wind_speed_unit": "mph", # adjust wind speed unit to miles per hour
            "temperature_unit": "fahrenheit", # adjust temperature unit to fahrenheit
            "precipitation_unit": "inch" # adjust precipitation unit to inches
        }
        
        responses = openmeteo.weather_api(url, params=params) # make the API request
        response = responses[0] # process the first response (only one location was requested)

        daily = response.Daily() # extract daily weather data
        
        # match the daily data with variables for yesterday's data
        yesterday_max_temperature = round(daily.Variables(0).ValuesAsNumpy()[0])
        yesterday_min_temperature = round(daily.Variables(1).ValuesAsNumpy()[0])
        yesterday_max_feels_like = round(daily.Variables(2).ValuesAsNumpy()[0])
        yesterday_min_feels_like = round(daily.Variables(3).ValuesAsNumpy()[0])
        yesterday_uv_index_max = round(daily.Variables(4).ValuesAsNumpy()[0])
        
        return (yesterday_max_temperature, yesterday_min_temperature, yesterday_max_feels_like, yesterday_min_feels_like, yesterday_uv_index_max)
    
    
    def get_weather_summary(self, forecast):
        """Generates a summary of the current weather conditions.

            Returns:
                summary (str): a simple readable summary of the current weather conditions.
        """
        summary = ""

        # temperature summary
        summary += f"Current temperature is {_bold}{round(self.temperature)}°F{bold_}\n"
        
        if self.feels_like > self.temperature:
            summary += f"It feels about {_bold}{round(self.feels_like - self.temperature)}° warmer{bold_}\n"
        elif self.feels_like < self.temperature:
            summary += f"It feels about {_bold}{round(self.temperature - self.feels_like)}° cooler{bold_}\n"
        else:
            summary += f"It feels about the {_bold}same as the temperature{bold_}\n"
            
        # max and min temperature summary
        summary += f"Today's temperature range is from {_bold}{round(self.min_temperature)}° to {round(self.max_temperature)}°{bold_}\n"
        summary += f"It feels like {_bold}{round(self.min_feels_like)}° to {round(self.max_feels_like)}°{bold_}\n"
        
        # conditions summary
        if self.cloud_coverage < 30:
            summary += f"It is currently {_bold}mostly sunny{bold_}\n"
        elif self.cloud_coverage < 60:
            summary += f"It is currently {_bold}partly cloudy{bold_}\n"
        elif self.cloud_coverage < 90:
            summary += f"It is currently {_bold}mostly cloudy{bold_}\n"
        
        return summary
        
    
    def get_comfort_index(self):
        """Calculates a comfort index based on temperature, humidity, and wind speed. Comfort scale goes from 1-10
        
        Side Effects:
            prints a string describing how comfortable the weather is based on the weather variables
        
        Returns:
            comfort (int): the comfort index
        """
        comfort = 10
        reasons = []
        
        # temperature deductions
        if self.temperature > 95 or self.feels_like > 95 or self.temperature < 20 or self.feels_like < 20:
            comfort -= 3
            reasons.append("extreme temperatures")
        elif self.temperature > 85 or self.feels_like > 85 or self.temperature < 32 or self.feels_like < 32:
            comfort -= 2
            reasons.append("uncomfortable temperatures")
        elif self.temperature < 50 or self.feels_like < 50:
            comfort -= 1
            reasons.append("quite chilly")
            
        # precipitation deductions
        if self.precipitation_chance > 80:
            comfort -= 3
            reasons.append("high chance of precipitation")
        elif self.precipitation_chance > 50:
            comfort -= 2
            reasons.append("good chance of precipitation")
        elif self.precipitation_chance > 30:
            comfort -= 1
            reasons.append("possible chance of precipitation")
        
        # wind speed deductions
        if self.wind_speed > 20:
            comfort -= 2
            reasons.append("strong winds")
        elif self.wind_speed > 15:
            comfort -= 1
            reasons.append("moderate wind speeds")
        
        # humidity deductions    
        if self.humidity < 15:
            comfort -= 1
            reasons.append("dry air")
        elif self.humidity > 55:
            comfort -= 2
            reasons.append("moderately high humidity")
        elif self.humidity > 80:
            comfort -= 3
            reasons.append("very high humidity")
        
        if comfort >= 9:
            description = "very comfortable"
        elif comfort >= 7:
            description = "comfortable"
        elif comfort >= 4:
            description = f"uncomfortable due to {', '.join(reasons)}"
        elif comfort >= 2:
            description = f"very uncomfortable due to {', '.join(reasons)}"
        
        print (f"{_bold}Daily Summary{bold_}\nToday's weather is {description} with a comfort index of {comfort} \n")
        return comfort
        
        
    def compare_with_yesterday(self, yesterday_forecast):
        """Compares today's forecast with yesterday's forecast.
        
        Args:
            past_weather (Forecast): a Forecast object containing yesterday's weather data.
        
        Returns:
            str: a list of comparisons between today's weather with yesterday's weather.
        """
        past_weather_info = (f"Yesterday's High: {yesterday_forecast[0]}°F\n\
                Yesterday's Low: {yesterday_forecast[1]}°F\n\
                Yesterday's Feels Like High: {yesterday_forecast[2]}°F\n\
                Yesterday's Feels Like Low: {yesterday_forecast[3]}°F\n\
                Yesterday's UV Index: {yesterday_forecast[4]}\n")
        
        comparisons = ""
        
        # temperature comparison
        temp_diff = self.max_temperature - yesterday_forecast[0]
        if abs(temp_diff) >= 5:
            if temp_diff > 0:
                comparisons += f"The high temperature today is {_bold}{abs(round(temp_diff))}° warmer{bold_} than yesterday's temperature of {yesterday_forecast[0]}\n"
            else:
                comparisons += f"The high temperature today is {_bold}{abs(round(temp_diff))}° cooler{bold_} than yesterday's temperature of {yesterday_forecast[0]}\n"
        else:
            comparisons += f"Today's maximum temperatures are {_bold}similar{bold_} to yesterday's\n"
        
        # feels like comparison
        feels_like_diff = self.max_feels_like - yesterday_forecast[2]
        if abs(feels_like_diff) >= 5:
            if feels_like_diff > 0:
                comparisons += f"The high feels like temperature today is {_bold}{abs(round(feels_like_diff))}° warmer{bold_} than yesterday's temperature of {yesterday_forecast[2]}\n"
            else:
                comparisons += f"The high feels like temperature today is {_bold}{abs(round(feels_like_diff))}° cooler{bold_}  than yesterday's temperature of {yesterday_forecast[2]}\n"
        else:
            comparisons += f"Today's maximum feels like temperatures are {_bold}similar{bold_} to yesterday's\n"
        
        # uv index comparison
        uv_diff = self.uv_index_max - yesterday_forecast[4]
        if abs(uv_diff) >= 1:
            if uv_diff > 0:
                comparisons += f"The peak UV index today is {_bold}{abs(round(uv_diff))} points higher{bold_} than yesterday's index of {round(yesterday_forecast[4])}\n"
            else:
                comparisons += f"The peak UV index today is {_bold}{abs(round(uv_diff))} points lower{bold_}  than yesterday's index of {round(yesterday_forecast[4])}\n"
        else:
            comparisons += f"The UV index today is {_bold}similar{bold_} to yesterday's\n"
        
        return comparisons
        

def get_location(city:str, state:str=None, country:str=None, max_results=10):
    """Gets the geographic coordinates for a given city and (optionally) state.
    
    This function makes a request to the Open-Meteo geocoding API to convert
    a city name (and optionally a state and/or country name) into latitude and longitude coordinates.
    
    Args:
        city (str): the name of the city
        state (str, optional): the name of the State. Defaults to None.
        country (str, optional): the name of the country. Defaults to None.
        max_results (int, optional): the maximum number of results to return. Defaults to 10.
    
    Returns:
        tuple: A tuple containing (latitude, longitude) coordinates or None if failed
        
    Side Effects:
        makes a request to the Open-Meteo geocoding API
    """
    # replace spaces with plus signs for the URL
    city = city.replace(" ", "+")

    geo_request = (f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count={max_results}&language=en&format=json")
    geo_location = requests.get(geo_request)
    
    # check if the request was successful
    if geo_location.status_code == 200:
        # parse the JSON response
        data = geo_location.json()
        
        # check if the "results" key exists in the returned data
        if 'results' in data:
        # if a state was specified, try to find a match with both city and state
            for result in data['results']:
                if (state != None and result['admin1'] == state) or (country != None and result['country'] == country):
                    latitude = result['latitude']
                    longitude = result['longitude']
                    print(f"{_bold}Location{bold_}: {result['name']} - {result['admin1']}, {result['country']}")
                    print(f"{_bold}Timezone{bold_}: {result['timezone']}\n")
                    return latitude, longitude
            
            # if no specific match or no state/country was specified, use the first result
            first_result = data['results'][0]
            latitude = first_result['latitude']
            longitude = first_result['longitude']
            
            print(f"{_bold}First Location{bold_}: {first_result['name']} - {first_result['admin1']}, {first_result['country']}")
            print(f"{_bold}Timezone{bold_}: {first_result['timezone']}\n")
            
            return latitude, longitude
        
        else:
            # handle non existent cities
            print(f"The city {city} does not exist")
            return None
    else:
        # handle API errors
        print(f"Status Code: {geo_location.status_code}")
        quit()

if __name__ == "__main__":
    print("Welcome to the WeatherFIT app!")
    
    location = get_location(input("Enter a city: ")) # asks the user to input a city to get the weather information
    # create a new Forecast object
    weather = Forecast(location[0], location[1]) # fetch the current weather forecast for the location
    
    comfort_index = weather.get_comfort_index()
    
    comparison = weather.compare_with_yesterday(weather.get_past_forecast(location[0], location[1]))
    
    summary = weather.get_weather_summary(weather)
    
    # prints all the forecast details of the location entered by the user
    print(weather)
    print(comfort_index)
    print(summary)
    print(comparison)
    
    
