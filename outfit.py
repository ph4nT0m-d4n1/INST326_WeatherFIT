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
        self.temp = self.forecast.temperature
        self.high_temp = self.forecast.max_temperature
        self.low_temp = self.forecast.min_temperature
        self.humidity = self.forecast.humidity
        self.wind = self.forecast.wind_speed
        self.precipitation_chance = self.forecast.precipitation_chance
        self.rain = self.forecast.rain
        self.showers = self.forecast.showers
        self.snowfall = self.forecast.snowfall
        self.cloud_coverage = self.forecast.cloud_coverage
        self.uv_index_max = self.forecast.uv_index_max
         
    def outfit_options(self):
        """This function generates outfit options based on the weather forecast.
         
        The function analyzes temperature, humidity, wind speed, and precipitation
        to recommend appropriate clothing items.
         
        Returns:
            str: A string listing recommended clothing items.
        """
        outfit = []  # list to store clothing recommendations
        
        # extract weather data from the forecast object
        
         
        # temperature-based clothing recommendations
        if self.temp < 32:
            outfit += ['puffer jacket', 'sweater', 'thermals', 'thick pants']
        elif self.temp < 40:
            outfit += ['heavy sweater', 'sweatpants', ]
        elif self.temp < 60:
            outfit += ['light sweater', 'jeans']
        elif self.temp < 75:
            outfit += ['T-shirt', 'shorts']
        else:
            outfit += ['T-shirt', 'shorts', 'sandals']
             
        # wind-based recommendations
        if self.wind > 20:
            outfit.append('windbreaker coat')
             
        # humidity recommendations for hot, humid days
        if self.humidity >= 80 and self.temp > 70:
            outfit.append('lightweight/breathable clothing')
        
        # precipitation recommendations
        if self.precipitation_chance > 50:
            outfit.append('umbrella')
             
        # specific precipitation type recommendations
        if self.rain > 0:
            outfit.append('rain boots')
        if self.showers > 0:
            outfit.append('rain jacket')
        if self.snowfall > 0:
            outfit.append('snow boots')
                      
        return f"Recommended outfit: {', '.join(outfit)}"
    
    def customize_outfit(self, user_preferences):
        """Customizes the outfit based on user preferences.
        
        Args:
            activity_type (str, optional): the type of activity (e.g., casual, formal, sports).
        
        Returns:
            user_preferences (dict): a dictionary of user preferences for clothing.
        """
        outfit = self.outfit_options().replace("Recommend outfit: ","").split(" , ")
         
         #type of outfit based on the occasion 
        if 'clothing style' in user_preferences:
            style = user_preferences['clothing style']
            if style == 'casual':
                if 'button down shirt' in outfit:
                    outfit.remove('button down shirt')
                if 'T-shirt' not in outfit:
                    outfit.append('T-shirt')
            elif style == 'formal':
                if 'T-shirt' in outfit: 
                    outfit.remove('T-shirt')
                if 'button down shirt' not in outfit:
                    outfit.append('button down shirt')
            elif style == 'active':
                if 'jeans' in outfit:
                    outfit.remove('jeans')
                if 'shorts' not in  outfit:
                    outfit.append('shorts')
                    
        #type of fabric based on the weather             
        if 'fabric' in user_preferences:
            fabric = user_preferences['fabric']
            if fabric == 'breathable' and 'heavy sweater' in outfit:
                outfit.remove('heavy sweater')
                if 'light sweater' not in outfit:
                    outfit.append('light sweater')
            elif fabric == 'warm' and 'light sweater' in outfit:
                outfit.remove('light sweater')
                if 'wool sweater' not in outfit:
                    outfit.append('wool sweater')
            elif fabric == 'waterproof' and 'raincoat' not in outfit:
                outfit.append('waterproof raincoat')
                           
        # type of clothing based on activity         
        if 'activity_type' in user_preferences:
            activity = user_preferences['activity_type']
            if activity == 'gym':
                if 'jeans' in outfit:
                    outfit.remove('jeans')
                if 'shorts' not in outfit:
                    outfit.append('shorts')
            elif activity == 'formal':
                if 'T-shirt' in outfit:
                    outfit.remove('T-shirt')
                if 'button down shirt' not in outfit:
                    outfit.append('button down shirt')
                    
        return f"Customized outfit {', '.join(outfit)}"
        
    def layering_recommendations(self):
        """Provides layering recommendations based on temperature fluctuations.
        
        Returns:
            str: layering advice based on the difference between daily max and min temperatures.
        """
        difference = self.high_temp - self.low_temp
        
        #check if layering is irrelevant (too warm)
        if self.low_temp >= 70:
            return """Weather is considerably warm all day. Wear something
                    loose and light on top if you want to cover up."""
                    
        #checking all differences, where temp drops below 70 degrees            
        if difference <= 5:
            return """Weather will remain constant throughout the 
                        day (within 5\xb0F). Layering Optional."""
        elif difference <= 15:
            return """It could get cooler as the sun goes down. Bring a light
                        jacket in addition to your outfit."""
        elif difference <= 25:
            return """The temperature drops significantly, make sure to bring
                        a substantial jacket or a hoodie if you plan on staying
                        out late."""
        else:
            return f"""Drastic variety in temperature today (over 25\xb0F).
                    Be prepared to layer, making sure you have on a lighter
                    outfit for the high temperature of {self.high_temp}\xb0F 
                    and warmer outerwear for the low temperature of 
                    {self.low_temp}\xb0F."""
                                  
    def recommended_accessories(self):
        """Suggests accessories based on weather conditions.
        
        Returns:
            str: a string listing recommended accessories.
        """
        accessories = []
        
        #checking primarily for extreme weather that needs a special accessory
        if self.cloud_coverage == 0:
            accessories.append('sun hat')
        elif self.cloud_coverage < 0.5:
            accessories.append('sunglasses')
        
        if self.temp < 35:
            accessories.append('gloves')
            accessories.append('scarf')
            accessories.append('beanie')
        if self.temp >= 70 and self.cloud_coverage != 0:
            accessories.append('baseball cap')
                    
        if self.uv_index_max > 2 and self.uv_index_max < 6 and self.cloud_coverage < 0.5:
            accessories.append('30+ SPF sunscreen')
        elif self.uv_index_max <= 10 and self.cloud_coverage < 0.25:
            accessories.append('50+ SPF suncreen')
            
        if not accessories:
           return f"The weather is agreeable today. Your accessories are up to you!"
        
        return f"Recommended accessories: {', '.join(accessories)}"
            
        
    
 
if __name__ == "__main__":
    weather = w.Forecast()
    location = w.get_location("College Park", "Maryland")  # example location
    weather.get_forecast(location[0], location[1])
    print(weather)

    outfit_recommender = Outfits(weather)
    outfit_suggestion = outfit_recommender.outfit_options()
    print(outfit_suggestion)
    accessories_suggestion = outfit_recommender.recommended_accessories()
    print(accessories_suggestion)
