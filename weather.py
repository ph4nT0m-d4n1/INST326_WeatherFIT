"""Weather App (Check in 1)
Danny Mallya
Bella Konrad
Jaden Shin
Marvin Gomez Molina

Professor Cruz
4/20/25

This program reads data from a weather api and determines the upcoming forecast. 
The app will then suggest clothing that would be appropriate for the weather condtions.
""""

class Forecast:
    """This class 
    """
    
    def __init__(self, date, temperature, humidity, precipitation_chance, precipitation_type, cloud_coverage, wind_speed):
        """This function initializes key attributes

            Attributes:
                date: the day
                temperature: temperature in fahrenheit for the day
                humidity: humidity percentage for the day
                precipitation_chance: chance of precipitation for the day
                precipitation_type: type of precipitation for the day (if any)
                cloud_coverage: percentage of cloud coverage for the day
                wind_speed: The wind speed in miles per hour for the day
        """
        self.date = date
        self.temperature = temperature
        self.humidity = humidity
        self.precipitation_chance = precipitation_chance
        self.precipitation_type = precipitation_type
        self.cloud_coverage = cloud_coverage
        self.wind_speed = wind_speed
    
    def get_data(self, weather_api):
        """This function gets the data from the api

            Attributes:
                weather_api: the
        """
        pass
    
    
    
    def __repr__(self):
        return f"The forecast for {self.date}:\nTemperature: {self.temperature}\nHumidity: {self.humidity}\nPrecipitation: {self.precipitation}\nCloud Coverage: {self.cloud_coverage}"