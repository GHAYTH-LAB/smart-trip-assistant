import requests
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from dotenv import load_dotenv 
import os
from pydantic import BaseModel,Field
from typing import List
load_dotenv()
GET_TOURIST_PLACES_API_KEY=os.getenv("GET_PLACES_API_KEY")
@tool("attractions_finder",description="Find tourist attractions in a given city. Takes a city name and returns a list of tourist attraction names (e.g. landmarks, monuments, points of interest) located in or near that city, using geocoding to locate the city and then searching for nearby attractions",return_direct=False)
def get_places(city:str)->str:
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

