"""WeatherFIT, an INST326 project
Group Members:
    Danny Mallya
    Bella Konrad
    Jaden Shin
    Marvin Gomez Molina
 
Instructor: Professor Cruz
Assignment: Final Project
Date: 05/16/2025
 
This program reads data from a weather API and determines the upcoming forecast.
The app will then suggest clothing that would be appropriate for the weather conditions.
"""
#import libraries for weather forecast and outfit recommendations
import outfit as fit
import weather as w

# import libraries for command line argument parsing and system interactions
import argparse
import sys

def parse_args(args_list):
    """Parses command line arguments.
    
    This function creates an argument parser to handle the command line
    arguments provided by the user when running the script.
    
    Args:
        args_list (list): the list of command line arguments
    
    Returns:
        argparse.Namespace: An object containing the parsed arguments
            with attributes 'city' (required) and 'state' (optional)
    """
    parser = argparse.ArgumentParser(description="Get weather forecast for a specified city")
    
    parser.add_argument("city", type=str, help="The name of the city to get the weather for")
    parser.add_argument("--state", type=str, help="The name of the state that the city is in")
    parser.add_argument("--country", type=str, help="The name of the countr the city is in")
    
    args = parser.parse_args(args_list)
    
    return args

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    
    location = w.get_location(args.city, args.state) # get coordinates for the specified location
    weather = w.Forecast(location[0], location[1])
    
    comfort_index = weather.get_comfort_index()
    comparison = weather.compare_with_yesterday(weather.get_past_forecast(location[0], location[1]))
    summary = weather.get_weather_summary(weather)
    
    print(weather)
    print(comfort_index)
    print(summary)
    print(comparison)
    
    
    outfit = fit.Outfits(weather) # create an Outfits object with the provided weather forecast
    
    if (input("Do you want to customize your outfit? ").lower() == "yes"):
        customized_outfit = outfit.customize_outfit({
        'clothing style': input("Choose an Outfit Style (casual, formal, or active): "),
        'fabric': input("Choose a Fabric Type (breathable, warm, waterproof): "),
        'activity_type': input("Choose an Activity Type (gym, formal): ")
    })
        print(customized_outfit) # print the recommended and customized outfit suggestion
    else:
        outfit.outfit_options() # print the recommended outfit suggestion
    
