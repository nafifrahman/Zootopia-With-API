import html
import json
import os
import requests

def load_data(file_path):
    """Load a JSON file and return its contents."""
    with open(file_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def read_template(file_path):
    """Read and return the HTML template."""
    with open(file_path, "r", encoding="utf-8") as handle:
        return handle.read()


def write_html(file_path, content):
    """Write the generated HTML to a file."""
    with open(file_path, "w", encoding="utf-8") as handle:
        handle.write(content)


def get_available_skin_types(animals_data):
    """Return a sorted list of unique skin types."""
    skin_types = set()

    for animal in animals_data:
        characteristics = animal.get("characteristics", {})
        skin_type = characteristics.get("skin_type")

        if skin_type:
            skin_types.add(skin_type)

    return sorted(skin_types)


def filter_by_skin_type(animals_data, selected_skin_type):
    """Return animals that match the selected skin type."""
    filtered_animals = []

    for animal in animals_data:
        characteristics = animal.get("characteristics", {})
        skin_type = characteristics.get("skin_type")

        if skin_type and skin_type.lower() == selected_skin_type.lower():
            filtered_animals.append(animal)

    return filtered_animals


def serialize_animal(animal_obj):
    """Convert one animal object into an HTML card."""
    name = html.escape(animal_obj.get("name", "Unknown"))
    characteristics = animal_obj.get("characteristics", {})
    locations = animal_obj.get("locations", [])

    output = '<li class="cards__item">\n'
    output += f'  <div class="card__title">{name}</div>\n'
    output += '  <div class="card__text">\n'
    output += '    <ul class="animal-details">\n'

    if "diet" in characteristics:
        diet = html.escape(characteristics["diet"])
        output += (
            f'      <li class="animal-details__item">'
            f"<strong>Diet:</strong> {diet}</li>\n"
        )

    if locations:
        first_location = html.escape(locations[0])
        output += (
            f'      <li class="animal-details__item">'
            f"<strong>Location:</strong> {first_location}</li>\n"
        )

    if "type" in characteristics:
        animal_type = html.escape(characteristics["type"])
        output += (
            f'      <li class="animal-details__item">'
            f"<strong>Type:</strong> {animal_type}</li>\n"
        )

    if "skin_type" in characteristics:
        skin_type = html.escape(characteristics["skin_type"])
        output += (
            f'      <li class="animal-details__item">'
            f"<strong>Skin type:</strong> {skin_type}</li>\n"
        )

    output += "    </ul>\n"
    output += "  </div>\n"
    output += "</li>\n"

    return output


def serialize_animals(animals_data):
    """Convert all animal objects into one HTML string."""
    output = ""

    for animal in animals_data:
        output += serialize_animal(animal)

    return output


def fetch_animals(animal_name):
    """Fetch animals matching the given name from the API."""
    api_key = os.environ.get("ANIMALS_API_KEY")

    if not api_key:
        raise ValueError(
            "Set ANIMALS_API_KEY in the PyCharm run configuration."
        )

    response = requests.get(
        "https://api.api-ninjas.com/v1/animals",
        headers={"X-Api-Key": api_key},
        params={"name": animal_name},
        timeout=30,
    )
    response.raise_for_status()

    return response.json()


def main():
    """Generate a website for an animal name entered by the user."""
    animal_name = input("Enter a name of an animal: ").strip()

    if not animal_name:
        print("Please enter an animal name.")
        return

    try:
        animals_data = fetch_animals(animal_name)
    except (requests.exceptions.RequestException, ValueError) as error:
        print(f"Could not fetch animal data: {error}")
        return

    if animals_data:
        animals_html = serialize_animals(animals_data)
    else:
        safe_name = html.escape(animal_name)

        animals_html = (
            '<li class="cards__item">\n'
            '  <h2 class="card__title">'
            f'The animal "{safe_name}" doesn&#39;t exist.'
            "</h2>\n"
            '  <p class="card__text">'
            "No matching animals were found. Try another name."
            "</p>\n"
            "</li>\n"
        )
    template = read_template("animals_template.html")

    final_html = template.replace(
        "__REPLACE_ANIMALS_INFO__",
        animals_html,
    )

    write_html("animals.html", final_html)

    print(
        "Website was successfully generated "
        "to the file animals.html."
    )


if __name__ == "__main__":
    main()