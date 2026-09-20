<div align="center">
	<img src="assets/journeygo-icon.svg" alt="JourneyGo icon" width="96">
	<h1>JourneyGo</h1>
	<p>AI-powered trip planning for flights, stays, visas, and unforgettable days.</p>

	<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white" alt="Python 3.13"></a>
	<a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-1.60.0-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit 1.60.0"></a>
	<a href="https://www.langchain.com/"><img src="https://img.shields.io/badge/LangChain-1.3.17-1C3C3C?logo=langchain&logoColor=white" alt="LangChain 1.3.17"></a>
	<a href="https://groq.com/"><img src="https://img.shields.io/badge/Groq-1.1.3-F55036?logo=groq&logoColor=white" alt="Groq"></a>
	<a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-Python%203.13-2496ED?logo=docker&logoColor=white" alt="Docker"></a>
</div>

JourneyGo is an AI travel agent that helps you plan a complete trip from a simple chat request. Powered by LangChain and Groq, the Streamlit app finds destinations, flights, hotels, visa information, and local activities, then builds a practical day-by-day itinerary.

The application is fully Dockerized for consistent and portable deployment, and is available online through Render.

**Live app:** [journeygo.onrender.com](https://journeygo.onrender.com/)

You tell it where you are travelling from, where you want to go, how many days you have before departure, and how long you want to stay. JourneyGo then gathers the pieces of the trip for you:

- Visa requirements
- Round-trip flight information
- Hotel options, ratings, prices, and cancellation details
- Tourist attractions in the destination
- A day-by-day itinerary

LangChain coordinates the planning workflow through a Groq-hosted language model and travel APIs that provide live information.

## How it works

The Streamlit app welcomes you by name and then waits for a trip request such as:

```text
I want to travel from Paris to Tunis in 30 days and stay for 5 days.
```

The assistant uses the request to:

1. Check visa requirements between the two countries.
2. Find a round-trip flight using the requested cities and dates.
3. Search for hotels for the same travel dates.
4. Find attractions in the destination city.
5. Spread the activities across the days of the trip and display the final plan in the Streamlit chat interface.

## Requirements

- Python 3.10 or newer is recommended.
- An internet connection.
- API keys for Groq, Geoapify, SerpApi, and the visa services used by the project.

## Use the deployed app

Open the live JourneyGo app in your browser:

[https://journeygo.onrender.com/](https://journeygo.onrender.com/)

Enter your name, describe your trip in the chat box, and wait while JourneyGo prepares your flights, hotels, visa information, attractions, and itinerary.

## Installation

Clone or download the project, then open a terminal in its folder:

```powershell
cd "Tourist Guider"
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

On macOS or Linux, activate the environment with:

```bash
source .venv/bin/activate
```

## Docker

You can run JourneyGo in a container without creating a local virtual environment.

### Build the Docker image

From the project root, run:

```powershell
docker build -t journeygo:v2 .
```

### Run the container

Make sure a `.env` file is present in the project folder with the required API keys, then run:

```powershell
docker run --rm -it --env-file .env journeygo:v2
```

This starts the CLI in interactive mode, where you can enter your name and a travel request such as:

```text
I want to travel from Paris to Tunis in 30 days and stay for 5 days.
```

> The container uses the same `main.py` entry point as the local app, so the experience is the same as running it directly on your machine.

## Environment variables

Create a file named `.env` in the project folder. Add your API keys like this:

```env
GROQ_API_KEY=your_groq_api_key
GET_PLACES_API_KEY=your_geoapify_api_key
GET_FLIGHTS_API_KEY=your_serpapi_api_key
GET_CORDONATES=your_restcountries_api_key
```

The application currently expects the variable `GET_CORDONATES` exactly as written above. It is used for the country lookup step.

Do not commit `.env` or share its contents. A simple `.gitignore` entry is recommended:

```gitignore
.env
.venv/
__pycache__/
```

## Run the Streamlit application locally

Start the web app with:

```powershell
streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open it in your browser and enter your name and travel request.

## Run the command-line application

The original terminal interface is still available through `main.py`:

```powershell
python main.py
```

Then type a travel request at the prompt. For example:

```text
I am leaving from London, travelling to Rome in 45 days, and I want to stay for 4 days.
```

Press `q` to exit before submitting a request.

## API services used

| Service                  | Purpose                                                                   |
| ------------------------ | ------------------------------------------------------------------------- |
| Groq                     | Runs the language model that coordinates the trip planning tools.         |
| Geoapify                 | Locates a city and finds nearby tourist attractions.                      |
| SerpApi / Google Flights | Finds airports and round-trip flight details.                             |
| SerpApi / Google Hotels  | Finds hotel options for the selected dates.                               |
| RestCountries            | Converts country names into ISO alpha-3 country codes for the visa lookup. |
| Can I Enter API          | Checks visa requirements between the departure and destination countries. |

### Visa requirements API

The visa tool accepts departure and destination country names, converts them to
ISO alpha-3 codes through RestCountries, and sends a request to:

```text
GET https://api.canienter.com/free/check
```

The request includes these query parameters:

```text
passport=<departure-country-alpha-3>
destination=<destination-country-alpha-3>
```

The response is used to report the visa requirement label, allowed stay in days,
the official application URL when available, and passport-validity requirements.
If either country code cannot be found or the visa service is unavailable, the
assistant tells the user to verify the requirements with the relevant embassy.

## Project structure

```text
.
├── main.py              # Main CLI app and travel-planning logic
├── app.py               # Streamlit web app entry point
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container build definition for running the app in Docker
├── README.md            # Project documentation
├── LICENSE              # MIT License terms
├── .gitignore           # Excludes local secrets and generated files
├── .env                 # Local environment variables for API keys (not committed)
├── .venv/               # Local Python virtual environment (generated)
├── __pycache__/         # Python bytecode cache (generated)
├── .qodo/               # Local project assistant/config metadata
└── .dockerignore        # Optional Docker exclusion file (if present in your setup)
```

### Main files and folders

- `app.py` contains the Streamlit web interface and calls the shared travel-planning logic.
- `main.py` contains the core JourneyGo logic and the original CLI interface. It defines the travel tools, calls the external APIs, validates the itinerary response, and returns or prints the final plan.
- `requirements.txt` lists the packages required to run the app locally or in Docker.
- `Dockerfile` builds a container image that runs `python main.py` and makes deployment easier in Docker-based environments.
- `README.md` documents the project, setup steps, environment variables, deployment, and running instructions.
- `.gitignore` prevents secrets, local environment folders, and Python-generated files from being committed.
- `.env` stores your API keys locally and should never be shared or pushed to version control.
- `.venv/` and `__pycache__/` are generated local artifacts created during development.
- `.qodo/` contains local tooling metadata and is not part of the runtime logic.
- `LICENSE` contains the MIT license for the project.

## A few things to know

- Results depend on the availability and correctness of the external APIs.
- Flight and hotel searches use dates calculated from the current date, so the same request can produce different results later.
- API failures are not all handled uniformly yet. Missing keys, invalid cities, rate limits, or unexpected API responses may stop the program with an error.
- The application currently handles one request per run. Start it again to plan another trip.
- This is a planning assistant, not a booking service. Always verify flight times, hotel policies, visa rules, and entry requirements with the relevant official providers before travelling.

## Development notes

The itinerary returned by the language model is validated with Pydantic models. The model is instructed to call each travel tool and to avoid inventing information when a service does not return data.

The main application logic lives in `main.py`, while `app.py` provides the Streamlit interface. These are the best places to start when adding features such as multiple requests per session, stronger error handling, budget filters, or additional web UI features.

## License

---

[MIT License](LICENSE)

---

Issues and PRs are always welcome 💌

Feel free to open an issue or submit a pull request with improvements, ideas, or feedback for JourneyGo!
