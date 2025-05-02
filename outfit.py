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

import weather as w

class Outfits():
    """This class will display outfits that reflect the forecast and user preferences.
    
    Args:
        forecast (Forecast): The weather forecast object containing weather details.
        user_preferences (dict): A dictionary of user preferences for clothing.
        activity_type (str): The type of activity (e.g., casual, formal, sports).
    
    Returns
        outfit (list): A list of clothing items suitable for the weather and user preferences.
    """
    
    def __init__(self,forecast:w.Forecast):
        self.forecast = forecast
        
    def outfit_options(self):
        """This function generates outfit options based on the weather forecast.
        
        Returns:
            str: A string listing recommended clothing items.
        """
        outfit = []
        accessories = []
        temp = self.forecast.temperature
        humidity = self.forecast.humidity 
        wind = self.forecast.wind_speed
        precipitation_chance = self.forecast.precipitation_chance
        rain = self.forecast.rain
        showers = self.forecast.showers
        snowfall = self.forecast.snowfall
        
        if temp < 40:
            outfit += ('sweater','pants','scarf')
        elif temp < 60:
            outfit += ('shirt','pants')
        elif temp < 75:
            outfit += ('T-shirt','shorts')
        else:
            outfit += ('T-shirt','shorts','sandals')
            
        if wind > 20:
            outfit.append('coat')
            
        if humidity > 80 and temp > 70:
            outfit.append('wear clothing that prevents heat strokes')

        if precipitation_chance > 50:
            outfit+=['umbrella']
        
        if rain > 0:
            outfit.append('rain boots')
        if showers > 0:
            outfit.append('rain jacket')
        if snowfall > 0:
            outfit.append('snow boots')
        
            
        return f"Recommended outfit: {', '.join(outfit)}"

if __name__ == "__main__":
    weather = w.Forecast()
    location = weather.get_location("College Park", "Maryland")  # example location
    weather.get_forecast(location[0], location[1])  # fetch the current weather forecast
    print (weather)
    
    outfit = Outfits(weather)
    outfit = outfit.outfit_options()
    print(outfit)
    
       