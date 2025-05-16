"""Tests for WeatherFIT's outfit module
Group Members:
    Danny Mallya
    Bella Konrad
    Jaden Shin
    Marvin Gomez Molina

Instructor: Professor Cruz
Assignment: Final Project
Date: 05/10/2025

This module contains unit tests for the outfit.py module.
"""

from outfit import Outfits
import weather
import pytest


class MockForecast:
    def __init__(self, temperature=70, max_temperature=75, min_temperature=65,
                 humidity=50, wind_speed=5, precipitation_chance=0,
                 rain=0, showers=0, snowfall=0, cloud_coverage=50, uv_index_max=5):
        self.temperature = temperature
        self.max_temperature = max_temperature
        self.min_temperature = min_temperature
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.precipitation_chance = precipitation_chance
        self.rain = rain
        self.showers = showers
        self.snowfall = snowfall
        self.cloud_coverage = cloud_coverage
        self.uv_index_max = uv_index_max

# Tests for different weather scenarios
def very_cold_weather():
    # temp < 32
    return MockForecast(temperature=20, max_temperature=25, min_temperature=15, 
                        humidity=20, wind_speed=10, precipitation_chance=0, 
                        rain=0, showers=0, snowfall=0, cloud_coverage=80, uv_index_max=1)

def mild_weather():
    # 50 <= temp < 60
    return MockForecast(temperature=55, max_temperature=60, min_temperature=50, 
                        humidity=50, wind_speed=15, precipitation_chance=0, 
                        rain=0, showers=0, snowfall=0, cloud_coverage=50, uv_index_max=3)

def hot_weather():
    # temp >= 75
    return MockForecast(temperature=85, max_temperature=90, min_temperature=80, 
                        humidity=80, wind_speed=5, precipitation_chance=0, 
                        rain=0, showers=0, snowfall=0, cloud_coverage=30, uv_index_max=8)


# Tests for Outfits.outfit_options()
def test_outfit_options_very_cold():
    forecast = very_cold_weather()
    recommender = Outfits(forecast)
    outfit = recommender.outfit_options()
    expected = ['puffer jacket', 'sweater', 'thermals', 'thick pants', 'boots']
    assert outfit == expected


def test_outfit_options_mild():
    forecast = mild_weather()
    recommender = Outfits(forecast)
    outfit = recommender.outfit_options()
    expected = ['light sweater', 'jeans', 'sneakers']
    assert outfit == expected


def test_outfit_options_hot():
    forecast = hot_weather()
    recommender = Outfits(forecast)
    outfit = recommender.outfit_options()
    expected = ['T-shirt', 'shorts', 'sandals', 'lightweight/breathable clothing']
    assert outfit == expected

def test_customize_outfit(self):
    clothing_style = {
        'clothing style:' 'active', 
        'fabric:' 'breathable',
        'activity type:''gym'}
    
    result = self.outfit.customize_outfit(clothing_style)
    assert 'shorts' in result 
    assert 'lightsweater' in result 
    assert 'jeans' not in result


    
