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
        outfit = []
        temp = self.forecast.temperature
        humidity = self.forecast.humidity 
        wind = self.forecast.wind_speed
        rain_chance = self.forecast.precipitation_chance
        
        if temp < 40:
            outfit += ['sweater','pants','scarf']
        elif temp < 60:
            outfit += ['shirt','pants']
        elif temp < 75:
            outfit += ['T-shirt','shorts']
        else:
            outfit += ['T-shirt','shorts','sandals']
            
        if wind > 20:
            outfit.append('coat')
            
        if humidity > 80 and temp > 70:
            outfit.append('wear clothing that prevents heat strokes')

        if rain_chance > 50:
            outfit+=['umbrella','rain jacket']
        elif rain_chance == 'snow':
            outfit +=['snow coat','gloves','scarf','snow pants']
            
        return f"Recommended outfit: {', '.join(outfit)}"

if __name__ == "__main__":
    weather = w.Forecast()
    weather.get_current_forecast(38.9807, -76.9369)
    print (weather)
    
    outfit = Outfits(weather)
    outfit = outfit.outfit_options()
    print(outfit)
    
       