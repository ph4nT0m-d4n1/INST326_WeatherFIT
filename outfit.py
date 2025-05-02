"""WeatherFIT, an INST326 project
Group Members:
    Danny Mallya
    Bella Konrad
    Jaden Shin
    Marvin Gomez Molina
 
Instructor: Professor Cruz
Assignment: Final Project
Date: 05/10/2025
 
This program reads data from a weather API and determines the upcoming forecast.
The app will then suggest clothing that would be appropriate for the weather conditions.
"""
 
import weather as w
 
class Outfits():
    """This class will display outfits that reflect the forecast and user preferences.
     
    Args:
        forecast (Forecast): The weather forecast object containing weather details.
        user_preferences (dict): A dictionary of user preferences for clothing.
     
    Returns:
        outfit (list): A list of clothing items suitable for the weather and user preferences.
    """
     
    def __init__(self, forecast:w.Forecast,user_preferences=None):
        self.forecast = forecast
         
    def outfit_options(self):
        """This function generates outfit options based on the weather forecast.
         
        The function analyzes temperature, humidity, wind speed, and precipitation
        to recommend appropriate clothing items.
         
        Returns:
            str: A string listing recommended clothing items.
        """
        outfit = []  # list to store clothing recommendations
        
        # extract weather data from the forecast object
        temp = self.forecast.temperature
        humidity = self.forecast.humidity
        wind = self.forecast.wind_speed
        precipitation_chance = self.forecast.precipitation_chance
        rain = self.forecast.rain
        showers = self.forecast.showers
        snowfall = self.forecast.snowfall
         
        # temperature-based clothing recommendations
        if temp < 40:
            outfit += ['heavy sweater', 'pants', 'scarf']
        elif temp < 60:
            outfit += ['light sweater', 'pants']
        elif temp < 75:
            outfit += ['T-shirt', 'shorts']
        else:
            outfit += ['T-shirt', 'shorts', 'sandals']
             
        # wind-based recommendations
        if wind > 20:
            outfit.append('windbreaker coat')
             
        # humidity recommendations for hot, humid days
        if humidity > 80 and temp > 70:
            outfit.append('lightweight, breathable clothing')
        
        # precipitation recommendations
        if precipitation_chance > 50:
            outfit.append('umbrella')
             
        # specific precipitation type recommendations
        if rain > 0:
            outfit.append('rain boots')
        if showers > 0:
            outfit.append('rain jacket')
        if snowfall > 0:
            outfit.append('snow boots')
                      
        return f"Recommended outfit: {', '.join(outfit)}"
    
    def customize_outfit(self, user_preferences):
        """Customizes the outfit based on user preferences.
        
        Args:
            activity_type (str, optional): the type of activity (e.g., casual, formal, sports).
        
        Returns:
            user_preferences (dict): a dictionary of user preferences for clothing.
        """
        pass
        
    def layering_recommendations(self):
        """Provides layering recommendations based on temperature fluctuations.
        
        Returns:
            str: layering advice based on the difference between daily max and min temperatures.
        """
        pass
    
    def recommended_accessories(self):
        """Suggests accessories based on weather conditions.
        
        Returns:
            str: a string listing recommended accessories.
        """
        pass
 
if __name__ == "__main__":
    weather = w.Forecast()
    location = w.get_location("College Park", "Maryland")  # example location
    weather.get_forecast(location[0], location[1])
    print(weather)

    outfit_recommender = Outfits(weather)
    outfit_suggestion = outfit_recommender.outfit_options()
    print(outfit_suggestion)