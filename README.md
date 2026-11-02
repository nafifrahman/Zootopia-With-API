# Zootopia With API

A Python project that fetches animal information from the API Ninjas
Animals API and generates a styled HTML website.

The user enters an animal name, and the program creates animal cards
containing the matching results. If no matching animals are found,
the website displays a helpful message.

This project was developed as part of the Masterschool software
development coursework to practise APIs, Python modules, HTML
templating, environment variables, and Git.

## Features

- Search for animals by name.
- Fetch animal information from an external API.
- Generate a website using an HTML template.
- Display available details such as diet, location, type, and skin type.
- Skip optional fields when they are missing.
- Display a message when no animals match the search.
- Keep API credentials outside the Python source code.
- Separate data fetching from website generation.

## Requirements

- Python 3
- An internet connection
- An API Ninjas account and an API key with access to the Animals API

## Installation

### 1. Clone the repository

```bash
git clone [https://github.com/nafifrahman/Zootopia-With-API.git](https://github.com/nafifrahman/Zootopia-With-API.git)
cd Zootopia-With-API
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it using the command for your terminal.

Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

The project uses:

- `requests` for HTTP requests.
- `python-dotenv` for loading local environment variables.

### 4. Configure the API key

Create a file named `.env` in the project's root directory.

Add your own API Ninjas key:

```dotenv
API_KEY='YOUR_API_NINJAS_KEY'
```

Replace the placeholder with your actual key.

The `.env` file is ignored by Git and must not be committed.
It is a plain-text local configuration file, not encrypted storage.

## Usage

Run the website generator from the project's root directory:

```bash
python animals_web_generator.py
```

Enter an animal name when prompted:

```text
Enter a name of an animal: Fox
Website was successfully generated to the file animals.html.
```

Open `animals.html` in your browser to view the results.

Run the program again with a different animal name, then refresh
the browser to see the newly generated website.

If the API returns no matches, the website displays a message
explaining that no matching animals were found.

If an API request fails, the program prints an error in the terminal.
The previously generated HTML file is left unchanged.

## Project Structure

```text
Zootopia-With-API/
├── animals_web_generator.py
├── data_fetcher.py
├── animals_template.html
├── requirements.txt
├── README.md
└── .gitignore
```

Additional local or generated files:

- `.env`: stores the local API key; not included in Git.
- `animals.html`: the generated website.
- `api_test.py`: a script used to experiment with API requests.
- `animals_data.json`: original static data retained from the
  previous Zootopia project; not used by the API-based generator.

## How It Works

1. The generator asks the user for an animal name.
2. It calls `data_fetcher.fetch_data(animal_name)`.
3. The data fetcher sends an authenticated request to the Animals API.
4. The API response is converted into a list of animal dictionaries.
5. The generator converts those dictionaries into HTML cards.
6. The cards replace the placeholder in `animals_template.html`.
7. The completed page is saved as `animals.html`.

## Troubleshooting

### Missing API key

Check that `.env` is in the project root and contains a nonempty
`API_KEY` value.

### Missing Python packages

Install the dependencies using:

```bash
python -m pip install -r requirements.txt
```

### API request failure

Check your internet connection and the error message in the terminal.
Also verify that your API key is valid and that your account has
access to the requested API.

### Old results still appear

Run the generator successfully, then refresh the browser.
A failed request does not replace the existing HTML file.

## Credits

Animal data is provided by the
[API Ninjas Animals API](https://api-ninjas.com/api/animals).

Created by Syed Nafifur Rahman as a Masterschool learning project.