"""Tests for WeatherFIT's weather module
Group Members:
    Danny Mallya
    Bella Konrad
    Jaden Shin
    Marvin Gomez Molina

Instructor: Professor Cruz
Assignment: Final Project
Date: 05/16/2025

This module contains unit tests for the weather.py module.
"""
import weather
import pytest
from unittest.mock import patch

def test_get_location():
    """Tests the get_location method in the weather.py module"""
    # using pre-checked coordinates to test the return values of some cities
    assert weather.get_location("Tokyo", country="Japan") == (35.6895, 139.69171)
    assert weather.get_location("College Park", "Maryland") == (38.98067, -76.93692)
    assert weather.get_location("San Francisco", "California", "United States") == (37.77493, -122.41942)
    assert weather.get_location("Melbourne", country="Australia", max_results=1) == (-37.814, 144.96332)
    assert weather.get_location("Athens") == (37.98376, 23.72784)
    
    # further testing with no state or country to ensure default behavior works
    assert isinstance(weather.get_location("Paris"), tuple)
    assert len(weather.get_location("Paris")) == 2
    
    # further testing with max_results parameter
    assert isinstance(weather.get_location("Springfield", max_results=5), tuple)
    
    # further testing handling of spaces in city names
    assert isinstance(weather.get_location("New York"), tuple)
    
    # testing for error handling for nonexistent cities
    assert weather.get_location("Nonexistent City") == None, "Should return None for failed API calls"

# setting up a pytest fixture to act as a reusable weather api response
@pytest.fixture
def mock_weather_api_response():
    """Creates a mock response for the OpenMeteo API"""
    # creating a mock response class structure to match what the code expects
    class MockVariables:
        def __init__(self, value):
            self.value = value
            
        def Value(self):
            return self.value
            
        def ValuesAsNumpy(self):
            return [self.value - 5, self.value]  # yesterday's value and today's value
    
    class MockCurrent:
        def Variables(self, index):
            # Return different values based on index to simulate different weather variables
            values = [75, 50, 20, 10, 30, 72, 0, 0, 0]
            return MockVariables(values[index])
    
    class MockDaily:
        def Variables(self, index):
            # return different values based on index to simulate daily variables
            values = [80, 70, 77, 68, 5]
            return MockVariables(values[index])
    
    class MockResponse:
        def Current(self):
            return MockCurrent()
            
        def Daily(self):
            return MockDaily()
            
        def Timezone(self):
            return "America/New_York"
            
        def TimezoneAbbreviation(self):
            return "EDT"
    
    class MockClient:
        def weather_api(self, url, params=None):
            return [MockResponse()]
    
    return MockClient()

def test_forecast(mock_weather_api_response):
    """Test the Forecast class and its methods."""
    # patch for datetime.now() to return a consistent date
    with patch('weather.datetime') as mock_datetime:
        mock_datetime.now.return_value.strftime.return_value = "2025-05-16, 12:00"
        
        # patch for the OpenMeteo client
        with patch('openmeteo_requests.Client', return_value=mock_weather_api_response):
            # testing initialization with Tokyo's coordinates
            forecast = weather.Forecast(35.6895, 139.69171)
            
            # check that the forecast object has the expected attributes
            assert forecast.date == "2025-05-16, 12:00", "Date should match the mocked datetime"
            assert forecast.temperature == 75, "Temperature should be 75"
            assert forecast.humidity == 50, "Humidity should be 50"
            assert forecast.precipitation_chance == 20, "Precipitation chance should be 20"
            assert forecast.wind_speed == 10, "Wind speed should be 10"
            assert forecast.cloud_coverage == 30, "Cloud coverage should be 30"
            assert forecast.feels_like == 72, "Feels like should be 72"
            assert forecast.rain == 0, "Rain should be 0"
            assert forecast.showers == 0, "Showers should be 0"
            assert forecast.snowfall == 0, "Snowfall should be 0"
            assert forecast.max_temperature == 80, "Max temperature should be 80"
            assert forecast.min_temperature == 70, "Min temperature should be 70"
            assert forecast.max_feels_like == 77, "Max feels like should be 77"
            assert forecast.min_feels_like == 68, "Min feels like should be 68"
            assert forecast.uv_index_max == 5, "UV index max should be 5"
            
            # testing the __repr__ method
            repr_str = repr(forecast)
            assert "Date & Time:" in repr_str, "Representation should include date and time"
            assert "Temperature: 75°F" in repr_str, "Representation should include temperature"
            assert "UV Index: 5" in repr_str, "Representation should include UV index"
            
            # testing the get_weather_summary method
            summary = forecast.get_weather_summary(forecast)
            assert "Current temperature is" in summary, "Weather summary should include current temperature"
            assert "Today's temperature range" in summary, "Weather summary should include temperature range"
            
            # testing the get_comfort_index method with mocked print to avoid output during tests
            with patch('builtins.print'):
                comfort_index = forecast.get_comfort_index()
                assert isinstance(comfort_index, int), "Comfort index should be an integer"
                assert 1 <= comfort_index <= 10, "Comfort index should be between 1 and 10"

def test_get_past_forecast(mock_weather_api_response):
    """Test the get_past_forecast method in the Forecast class."""
    # patch for the OpenMeteo client
    with patch('openmeteo_requests.Client', return_value=mock_weather_api_response):
        # create a Forecast object
        forecast = weather.Forecast(35.6895, 139.69171)
        
        # call the get_past_forecast method
        yesterday_forecast = forecast.get_past_forecast(35.6895, 139.69171)
        
        # check that the return value is a tuple with 5 elements
        assert isinstance(yesterday_forecast, tuple), "get_past_forecast should return a tuple"
        assert len(yesterday_forecast) == 5, "get_past_forecast should return 5 values"
        
        # check the values based on our mock response
        assert yesterday_forecast[0] == 75, "Yesterday's max temperature should be 75"
        assert yesterday_forecast[1] == 65, "Yesterday's min temperature should be 65"
        assert yesterday_forecast[2] == 72, "Yesterday's max feels like should be 72"
        assert yesterday_forecast[3] == 63, "Yesterday's min feels like should be 63"
        assert yesterday_forecast[4] == 0, "Yesterday's UV index max should be 0"
        
        # testing the compare_with_yesterday method
        comparison = forecast.compare_with_yesterday(yesterday_forecast)
        assert isinstance(comparison, str), "compare_with_yesterday should return a string"
        assert "temperature" in comparison.lower(), "Comparison should mention temperature"
        assert "uv index" in comparison.lower(), "Comparison should mention UV index"
