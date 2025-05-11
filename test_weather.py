"""Tests for WeatherFIT's weather module
Group Members:
    Danny Mallya
    Bella Konrad
    Jaden Shin
    Marvin Gomez Molina

Instructor: Professor Cruz
Assignment: Final Project
Date: 05/10/2025

This module contains unit tests for the weather.py module.
"""

import weather as w

def test_forecast():
    """Test the Forecast class and its methods."""
    # Create a mock forecast object with sample data
    forecast = w.Forecast(
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
    
    # Test the attributes of the forecast object
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

