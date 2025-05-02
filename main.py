import outfit as fit
import weather as w
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
    args = parser.parse_args(args_list)
    
    return args

if __name__ == "__main__":
    weather = w.Forecast()
    args = parse_args(sys.argv[1:])
    
    location = w.get_location(args.city, args.state) # get coordinates for the specified location
    weather.get_forecast(location[0], location[1]) # fetch the current weather forecast for the location
    
    print(weather)
    
    outfit = fit.Outfits(weather) # create an Outfits object with the weather forecast
    outfit = outfit.outfit_options() # get the recommended outfit based on the weather
    
    print(outfit)
