import os
from pathlib import Path

import requests
from dotenv import load_dotenv


ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

API_URL = "https://api.api-ninjas.com/v1/animals"
API_KEY = os.getenv("API_KEY")
REQUEST_TIMEOUT = 30


def fetch_data(animal_name):
    """Fetch matching animals and return a list of dictionaries."""
    if not API_KEY:
        raise ValueError(
            "API_KEY is missing. Add it to the project's .env file."
        )

    try:
        response = requests.get(
            API_URL,
            headers={"X-Api-Key": API_KEY},
            params={"name": animal_name},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()

    except requests.exceptions.HTTPError as error:
        status_code = error.response.status_code

        raise RuntimeError(
            f"The API returned HTTP {status_code}."
        ) from error

    except requests.exceptions.Timeout as error:
        raise RuntimeError(
            "The API request timed out. Please try again."
        ) from error

    except requests.exceptions.ConnectionError as error:
        raise RuntimeError(
            "Could not connect to the API. "
            "Check your internet connection."
        ) from error

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            "The API request failed for another reason."
        ) from error

    try:
        animals_data = response.json()
    except ValueError as error:
        raise RuntimeError(
            "The API response could not be read as JSON."
        ) from error

    if not isinstance(animals_data, list):
        raise ValueError(
            "The API returned an unexpected data format."
        )

    return animals_data
