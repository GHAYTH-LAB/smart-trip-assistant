from langchain.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from dotenv import load_dotenv 
import os
from pydantic import BaseModel,Field
from typing import List
load_dotenv()
GET_TOURIST_PLACES_API_KEY=os.getenv("GET_PLACES_API_KEY")
@tool
def get_places()
