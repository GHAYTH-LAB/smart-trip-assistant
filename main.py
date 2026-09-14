import requests
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
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
@tool("get_hotels",description="find hotles in a specificated place also their ratings and their prices",return_direct=False)
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
@tool("visa_requirements",description="get visa requirements for the destination country",return_direct=False)
def get_visa_requirements(departure_country:str,destination_country:str)->str:
    URL=f"https://restcountries.com/v3.1/name/{destination_country}?fields=name,cca2"
    response=requests.get(url=URL)
    data=response.json()
    destination_code=data[0]["cca2"]
    URL=f"https://restcountries.com/v3.1/name/{departure_country}?fields=name,cca2"
    response=requests.get(url=URL)
    data=response.json()
    departure_code=data[0]["cca2"]
    URL=f"https://rough-sun-2523.fly.dev/visa/{departure_code}/{destination_code}"
    data=requests.get(url=URL).json()
    if data["category"]["code"]=="VF":
        return f"Visa is not required from {departure_country} to {destination_country}"
    else:
        return f"Visa is required you must appply for it and its duration is {data["dur"]}"
class DayPlan(BaseModel):
    day_number:int=Field(description="Day of the trip, starting from 1")    
    activities:List[str]=Field(description="List of activities or attractions planned for this day")
class TripItinerary(BaseModel):
    departure_city:str=Field(description="city the traveler is parting from(departure city)")
    destination_city: str = Field(description="City the traveler is visiting")
    flight_info: str = Field(description="Summary of the best flight found: airports, times, duration, airline, aircraft, class, and flight number")
    hotel_infos:List[str]=Field(description="Summary of the best flight found: airports, times, duration, airline, aircraft, class, and flight number")
    visa_info: str = Field(description="Visa requirement details: whether a visa is needed and the allowed stay duration")

    days: List[DayPlan] = Field(description="Day-by-day plan covering the full length of the trip, distributing attractions across days without repeats")
LLM=ChatGroq(
    model="openai/gpt-oss-120b"
    ,temperature=0
)
print("Hello Ghayth! JourneyGo is here To assist Today,I am your guide for programming Good Trips ,Just Give me where You wanna go and from where also after how many days you are willing to flight and how much are you willing to stay and I WILL PROGRAMM EVRYTHING FOR YOU!")
agent=create_agent(
    model=LLM
    ,tools=[get_visa_requirements,hotels_finder,fetch_flights,get_places]
    ,response_format=TripItinerary
    ,system_prompt="""You are JourneyGo, a trip-planning assistant. Given a departure city, destination city, how many days until departure, and trip length, you must build a complete trip plan using the tools available to you.
Tools available:
- get_visa_requirements(departure_country, destination_country): checks whether a visa is needed between two countries and the allowed stay duration. Always call this FIRST, using the countries (not cities) that correspond to the departure_city and destination_city.
- fetch_flights(departure_city, arrival_city, delay_before_flight, trip_period_to_stay): finds the best round-trip flight.
- hotels_finder(city, delay_before_flight, trip_period_to_stay): finds hotel options at the destination for the trip dates.
- get_places(city): finds tourist attractions in the destination city.
Rules:
1. Always check visa requirements before anything else. If a visa is required, still continue building the rest of the plan, but make sure the visa_info field clearly states that a visa is required and must be arranged before departure.
2. Call fetch_flights and hotels_finder using the destination and departure cities exactly as given by the user, along with delay_before_flight and trip_period_to_stay.
3. Call get_places using the destination city to gather a list of attractions.
4. Distribute the attractions returned by get_places evenly across the days of the trip (trip_period_to_stay days total) — do not repeat the same attraction on multiple days, and do not leave any day empty if enough attractions are available.
5. Fill in every field of the response schema. Do not leave a field empty or vague if a tool successfully returned data for it.
6. If a tool call fails or returns no data, state that clearly and specifically in the relevant field (e.g. "No hotels found for these dates") instead of guessing or inventing values.
CRITICAL: You must actually CALL the tools get_visa_requirements, fetch_flights, hotels_finder, and get_places using their function-calling mechanism. Do NOT write the tool name as a string value in any field. Only use the real data returned by each tool call to fill in flight_info, hotel_infos, and visa_info.

"""
)
Query=input("\n press q in the keyboard to leave JourneyGo")
intermediate_response=agent.invoke({
        "messages":[
            {
                "role":"user"
                ,"content":Query
                }
        ]
    })  
Response=intermediate_response["structured_response"]
formatting_template=ChatPromptTemplate.from_messages([
    ("system", "You are a warm travel writer. Write one flowing paragraph, no bullet points, no headers."),
    ("user", "Trip data:\n{trip_data}")
]
)
chain=formatting_template|LLM|StrOutputParser()
Final_response=chain.invoke({"trip_data": Response.model_dump_json(indent=2)})
print(Final_response)