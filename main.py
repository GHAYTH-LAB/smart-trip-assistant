import requests
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from dotenv import load_dotenv 
import os
from pydantic import BaseModel,Field
from typing import List
from datetime import datetime,timedelta
load_dotenv()
GET_TOURIST_PLACES_API_KEY=os.getenv("GET_PLACES_API_KEY")
@tool("attractions_finder",description="Find tourist attractions in a given city. Takes a city name and returns a list of tourist attraction names (e.g. landmarks, monuments, points of interest) located in or near that city, using geocoding to locate the city and then searching for nearby attractions",return_direct=False)
def get_places(city:str)->List:
    key=GET_TOURIST_PLACES_API_KEY
    url="https://api.geoapify.com/v1/geocode/search"
    partial_params={
        "apiKey":key
        ,"text":city
    }
    response=requests.get(url=url,params=partial_params)
    data=response.json()
    place_id_extracted=data["features"][0]["propreties"]["place_id"]
    Link="https://api.geoapify.com/v2/places"
    params={
        "categories":"tourism.attraction"
        ,"apiKey":key
        ,"filter":f"place:{place_id_extracted}"
        ,"lang":"en"
   }
    response=requests.get(url=Link,params=params)
    final_data=response.json()
    attractions=[]
    for feature in final_data["features"]:
        properties=feature["properties"]
        categories =properties.get("categories", [])
        if "tourism.attraction" in categories:
             name = properties.get("name")
             if name:
                 attractions.append(name)
    return attractions
@tool("get_flights",description="""Find the best round-trip flight between two cities via Google Flights (SerpApi).

    Args:
        departure_city: City to fly from (e.g. "Paris").
        arrival_city: City to fly to (e.g. "Tunis").
        delay_before_flight: Days from today until the outbound flight.
        trip_period_to_stay: Days to stay before the return flight.

    Returns:
        A summary of the best flight found: airports, times, duration,
        airline, aircraft, class, and flight number.""",return_direct=False)
def fetch_flights(departure_city:str,arrival_city:str,delay_before_flight:int,trip_period_to_stay:int)->str:
    URL="https://serpapi.com/search?engine=google_flights_autocomplete"
    params={
        "q":departure_city
        ,"api_key":os.getenv("GET_FLIGHTS_API_KEY")
    }
    response=requests.get(url=URL
                          ,params=params)
    Airports_data=response.json()
    departure_Airport_id=Airports_data["suggestions"][0]["airports"][0]["id"]
    departure_Airport_name=Airports_data["suggestions"][0]["airports"][0]["name"]
    URL="https://serpapi.com/search?engine=google_flights_autocomplete"
    params={
            "q":arrival_city
            ,"api_key":os.getenv("GET_FLIGHTS_API_KEY")
        }
    response=requests.get(url=URL
                            ,params=params)
    Airports_data=response.json()
    arrival_city_Airport_id=Airports_data["suggestions"][0]["airports"][0]["id"]
    arrival_city_Airport_name=Airports_data["suggestions"][0]["airports"][0]["name"]
    URL="https://serpapi.com/search?engine=google_flights"
    outbound_date_date_not_formatted=datetime.now()+timedelta(days=delay_before_flight)
    outbound_date_formatted = outbound_date_date_not_formatted.strftime("%Y-%m-%d")
    departure_day_not_formatted=datetime.now()+timedelta(days=trip_period_to_stay+delay_before_flight)
    departure_day_formatted = departure_day_not_formatted.strftime("%Y-%m-%d")    
    params={
        "departure_id":departure_Airport_id
        ,"arrival_id":arrival_city_Airport_id
        ,"outbound_date": outbound_date_formatted
        ,"return_date":departure_day_formatted
        ,"api_key":os.getenv("GET_FLIGHTS_API_KEY")
    }
    response=requests.get(url=URL
                          ,params=params)
    data=response.json()
    return f"""Best flight available regarding your scheldue is from {data["best_flights"][0]["flights"][0]["departure_airport"]["name"]} to {data["best_flights"][0]["flights"][0]["arrival_airport"]["name"]} , The dparture Time is on {data["best_flights"][0]["flights"][0]["departure_airport"]["time"]} and the Arrival is on
     {data["best_flights"][0]["flights"][0]["arrival_airport"]["time"]} The duration will be approximatively {data["best_flights"][0]["flights"][0]["duration"]} minute,The Airplane is {data["best_flights"][0]["flights"][0]["airplane"]} and the airline is {data["best_flights"][0]["flights"][0]["airline"]} , The Travel class is {data["best_flights"][0]["flights"][0]["travel_class"]} and the flight_number is {data["best_flights"][0]["flights"][0]["flight_number"]}
     """
@tool("get_hotels",description="find hotles in a specificated place",return_direct=False)
def hotels_finder(city:str,delay_before_flight:int,trip_period_to_stay:int)->str:
    API_URL="https://serpapi.com/search?engine=google_hotels"
    day_of_the_flight_formatted = (datetime.now() + timedelta(days=delay_before_flight)).strftime("%Y-%m-%d")
    day_of_the_departure_formatted = (datetime.now() + timedelta(days=delay_before_flight + trip_period_to_stay)).strftime("%Y-%m-%d") 
    params={
        "q":f"{city} hotels"
        ,"check_in_date":day_of_the_flight_formatted
        ,"check_out_date":day_of_the_departure_formatted
        ,"api_key":os.getenv("GET_FLIGHTS_API_KEY")
    }
    response=requests.get(url=API_URL,params=params)
    if response.status_code != 200:
        return f"Error fetching hotels: {response.status_code} - {response.text}"
    data=response.json()
    properties = data.get("properties", [])
    if not properties:
        return f"No hotels found in {city} for the selected dates."
    results = []
    for hotel in properties[:3]:
        name = hotel.get("name", "Unknown hotel")
        rating = hotel.get("overall_rating", "N/A")
        price = hotel.get("rate_per_night", {}).get("lowest", "N/A")
        free_cancellation = hotel.get("free_cancellation", False)
        cancellation_note = "includes free cancellation" if free_cancellation else "does not include free cancellation"
        results.append(f"{name} — rated {rating}, {price}/night, {cancellation_note}")
    return "Here are some hotel options:\n" + "\n".join(f"- {r}" for r in results)
