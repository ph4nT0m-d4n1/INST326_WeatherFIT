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

def test_get_location():
    """Tests the get_location method in the weather.py module"""
    # using pre-tested coordinates to test the return values of some cities
    assert weather.get_location("Tokyo", country="Japan") == (35.6895, 139.69171)
    assert weather.get_location("College Park", "Maryland") == (38.98067, -76.93692)
    assert weather.get_location("San Francisco", "California", "United States") == (37.77493, -122.41942)
    assert weather.get_location("Melbourne", country="Australia", max_results=1) == (-37.814, 144.96332)
    assert weather.get_location("Athens") == (37.98376, 23.72784)
    

def test_forecast():
    """Test the Forecast class and its methods."""
    # create a mock forecast object with sample data
    forecast = weather.Forecast(
        date = weather.datetime.now().strftime("%Y-%m-%d, %H:%M"),
        temperature=75,
        max_temperature=80,
        min_temperature=70,
        humidity=50,
        wind_speed=10,
        precipitation_chance=20,
        rain=False,
        showers=False,
        snowfall=False,
        cloud_coverage=30,
        uv_index_max=5
    )
    # test the attributes of the forecast object
    assert forecast.date == weather.datetime.now().strftime("%Y-%m-%d, %H:%M")
    assert forecast.temperature == 75, "Temperature should be 75"
    assert forecast.max_temperature == 80, "Max temperature should be 80"
    assert forecast.min_temperature == 70, "Min temperature should be 70"
    assert forecast.humidity == 50, "Humidity should be 50"
    assert forecast.wind_speed == 10, "Wind speed should be 10"
    assert forecast.precipitation_chance == 20, "Precipitation chance should be 20"
    assert forecast.rain is False, "Rain should be False"
    assert forecast.showers is False, "Showers should be False"
    assert forecast.snowfall is False, "Snowfall should be False"
    assert forecast.cloud_coverage == 30, "Cloud coverage should be 30"
    assert forecast.uv_index_max == 5, "UV index max should be 5"
