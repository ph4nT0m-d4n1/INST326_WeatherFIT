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
                 humidity=50, wind_speed=10, precipitation_chance=0,
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
                        humidity=20, wind_speed=10, precipitation_chance=70, 
                        rain=0, showers=0, snowfall=0.5, cloud_coverage=80, uv_index_max=1)

def mild_weather():
    # 50 <= temp < 60
    return MockForecast(temperature=55, max_temperature=60, min_temperature=50, 
                        humidity=50, wind_speed=15, precipitation_chance=10, 
                        rain=0, showers=0, snowfall=0, cloud_coverage=50, uv_index_max=3)

def hot_weather():
    # temp >= 75
    return MockForecast(temperature=85, max_temperature=90, min_temperature=80, 
                        humidity=80, wind_speed=5, precipitation_chance=0, 
                        rain=0, showers=0, snowfall=0, cloud_coverage=30, uv_index_max=8)

def hot_humid_weather():
    # temp > 70 and humidity >= 80
    return MockForecast(temperature=80, max_temperature=85, min_temperature=75, 
                        humidity=85, wind_speed=5, precipitation_chance=0, 
                        rain=0, showers=0, snowfall=0, cloud_coverage=30, uv_index_max=7)

def rainy_weather():
    #rain > 0
    return MockForecast(temperature=60, max_temperature=65, min_temperature=55, 
                        humidity=70, wind_speed=10, precipitation_chance=80, 
                        rain=0.5, showers=0.1, snowfall=0, cloud_coverage=90, uv_index_max=3)

def windy_weather():
    # wind > 20
    return MockForecast(temperature=60, max_temperature=65, min_temperature=55, 
                        humidity=60, wind_speed=25, precipitation_chance=10, 
                        rain=0, showers=0, snowfall=0, cloud_coverage=50, uv_index_max=4)
    
def steady_weather():
    # 50 <= temp < 55
    return MockForecast(temperature=55, max_temperature=55, min_temperature=50, 
                        humidity=50, wind_speed=15, precipitation_chance=10, 
                        rain=0, showers=0, snowfall=0, cloud_coverage=50, uv_index_max=3)

def extreme_weather():
    # 40 <= temp < 65
    return MockForecast(temperature=55, max_temperature=65, min_temperature=40, 
                        humidity=50, wind_speed=15, precipitation_chance=10, 
                        rain=0, showers=0, snowfall=0, cloud_coverage=50, uv_index_max=3)
    


# Helper to build expected outfit list for outfit_options
def build_expected_outfit(forecast, base_items):
    expected = list(base_items)
    if forecast.wind_speed > 20:
        expected.append('windbreaker coat')
    if forecast.humidity >= 80 and forecast.temperature > 70:
        expected.append('lightweight/breathable clothing')
    if forecast.precipitation_chance > 50:
        expected.append('umbrella')
    if forecast.rain > 0:
        expected.append('rain boots')
    if forecast.showers > 0:
        expected.append('rain jacket')
    if forecast.snowfall > 0:
        expected.append('snow boots')
    return expected

# Tests for Outfits.outfit_options()
def test_outfit_options_very_cold():
    recommender = Outfits(very_cold_weather)
    outfit = recommender.outfit_options()
    base = ['puffer jacket', 'sweater', 'thermals', 'thick pants', 'boots']
    expected = build_expected_outfit(very_cold_weather, base)
    assert outfit == expected


def test_outfit_options_mild():
    recommender = Outfits(mild_weather)
    outfit = recommender.outfit_options()
    base = ['light sweater', 'jeans', 'sneakers']
    expected = build_expected_outfit(mild_weather, base)
    assert outfit == expected


def test_outfit_options_hot():
    recommender = Outfits(hot_weather)
    outfit = recommender.outfit_options()
    base = ['T-shirt', 'shorts', 'sandals']
    expected = build_expected_outfit(hot_weather, base)
    assert outfit == expected

def test_outfit_options_hot_humid():
    recommender = Outfits(hot_humid_weather)
    outfit = recommender.outfit_options()
    base = ['T-shirt', 'shorts', 'shoes'] # Base for temp 80
    expected = build_expected_outfit(hot_humid_weather, base)
    assert outfit == expected

def test_outfit_options_rainy():
    recommender = Outfits(rainy_weather)
    outfit = recommender.outfit_options()
    base = ['T-shirt', 'shorts', 'breatheable sneakers'] # Base for temp 60
    expected = build_expected_outfit(rainy_weather, base)
    assert outfit == expected

def test_outfit_options_windy():
    recommender = Outfits(windy_weather)
    outfit = recommender.outfit_options()
    base = ['T-shirt', 'shorts', 'breatheable sneakers'] # Base for temp 60
    expected = build_expected_outfit(windy_weather, base)
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

#layering tests
def test_layering_too_warm():
    tester = Outfits(hot_weather)
    layer = tester.layering_recommendations()
    
    assert layer == """Weather is considerably warm all day. Wear something
                    loose and light on top if you want to cover up."""
                    
def test_layering_small_difference():
    tester = Outfits(steady_weather)
    layer = tester.layering_recommendations()
    assert layer == """Weather will remain constant throughout the day 
                    (within 5\xb0F). Layering Optional."""

def test_layering_extreme_difference():
    tester = Outfits(extreme_weather)
    layer = tester.layering_recommendations()
    assert layer == f"Drastic variety in temperature today (over 25\xb0F).\
                \nBe prepared to layer, making sure you have on a lighter outfit\
                \nfor the high temperature of {round(tester.self.high_temp)}\xb0F\
                \nand warmer outerwear for the low temperature of\
                    \n{round(tester.self.low_temp)}\xb0F.\n"
                    
    
    
