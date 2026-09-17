# JourneyGo

JourneyGo is a small, command-line travel planner that turns a simple trip request into a practical itinerary.

You tell it where you are travelling from, where you want to go, how many days you have before departure, and how long you want to stay. JourneyGo then gathers the pieces of the trip for you:

- Visa requirements
- Round-trip flight information
- Hotel options, ratings, prices, and cancellation details
- Tourist attractions in the destination
- A day-by-day itinerary

The project uses a Groq-hosted language model to coordinate the planning process and calls travel APIs for live information.

## How it works

JourneyGo is a Python terminal application. When you run it, the program waits for one request such as:

```text
I want to travel from Paris to Tunis in 30 days and stay for 5 days.
```

The assistant uses the request to:

1. Check visa requirements between the two countries.
2. Find a round-trip flight using the requested cities and dates.
3. Search for hotels for the same travel dates.
4. Find attractions in the destination city.
5. Spread the attractions across the days of the trip and print the final plan.

## Requirements

- Python 3.10 or newer is recommended.
- An internet connection.
- API keys for Groq, Geoapify, SerpApi, and the visa services used by the project.

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

## Environment variables

Create a file named `.env` in the project folder. Add your API keys like this:

```env
GROQ_API_KEY=your_groq_api_key
GET_PLACES_API_KEY=your_geoapify_api_key
GET_FLIGHTS_API_KEY=your_serpapi_api_key
GET_CORDONATES=your_restcountries_api_key
GET_VISA_API_KEY=your_visa_api_key
```

The application currently expects the variable `GET_CORDONATES` exactly as written above. It is used for the country lookup step.

Do not commit `.env` or share its contents. A simple `.gitignore` entry is recommended:

```gitignore
.env
.venv/
__pycache__/
```

## Run the application

Start JourneyGo with:

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
| RestCountries            | Converts country names into country codes for the visa lookup.            |
| Orizn Visa API           | Checks visa requirements between the departure and destination countries. |

## Project structure

```text
.
├── main.py              # CLI application and trip-planning logic
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment-variable template
├── .gitignore           # Files excluded from version control
├── Readme.md            # Project documentation
├── LICENSE              # MIT License terms
├── .qodo/               # Local project-assistant configuration
├── .env                 # Local API keys; never commit this file
└── __pycache__/         # Python bytecode cache; generated automatically
```

### Main files and folders

- `main.py` contains the complete application. It defines the travel-search tools, calls the external APIs, validates the itinerary with Pydantic, and prints the final result.
- `requirements.txt` lists the Python packages needed to run the application.
- `.env.example` shows the environment variables that need to be configured. Copy it to `.env` and add your real API keys.
- `.gitignore` prevents secrets, virtual-environment files, temporary files, and Python cache files from being committed.
- `LICENSE` contains the MIT License for this project.
- `.qodo/` contains local tooling configuration and is not part of the application's runtime logic.
- `.env`, `venv/`, and `__pycache__/` are machine-specific or generated items. They are useful locally but should not be shared as part of the source code. The `venv/` folder appears after you create a virtual environment.

## A few things to know

- Results depend on the availability and correctness of the external APIs.
- Flight and hotel searches use dates calculated from the current date, so the same request can produce different results later.
- API failures are not all handled uniformly yet. Missing keys, invalid cities, rate limits, or unexpected API responses may stop the program with an error.
- The application currently handles one request per run. Start it again to plan another trip.
- This is a planning assistant, not a booking service. Always verify flight times, hotel policies, visa rules, and entry requirements with the relevant official providers before travelling.

## Development notes

The itinerary returned by the language model is validated with Pydantic models. The model is instructed to call each travel tool and to avoid inventing information when a service does not return data.

The main application logic lives in `main.py`, so that is the best place to start when adding features such as multiple requests per session, stronger error handling, budget filters, or a graphical interface.

## License

---

[MIT License](LICENSE)

---

Issues and PRs are always welcome 💌

Feel free to open an issue or submit a pull request with improvements, ideas, or feedback for JourneyGo!
