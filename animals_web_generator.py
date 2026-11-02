import html
import json


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


def main():
    """Generate animals.html based on selected skin type."""
    animals_data = load_data("animals_data.json")
    skin_types = get_available_skin_types(animals_data)

    print("Available skin types:")
    for skin_type in skin_types:
        print(f"- {skin_type}")

    selected_skin_type = input("Enter a skin type: ").strip()
    filtered_animals = filter_by_skin_type(animals_data, selected_skin_type)

    if filtered_animals:
        animals_output = serialize_animals(filtered_animals)
    else:
        animals_output = (
            '<li class="cards__item">'
            '<div class="card__title">No animals found</div>'
            '<div class="card__text">'
            '<ul class="animal-details">'
            '<li class="animal-details__item">'
            'Try another skin type.'
            "</li>"
            "</ul>"
            "</div>"
            "</li>"
        )

    template = read_template("animals_template.html")
    final_html = template.replace("__REPLACE_ANIMALS_INFO__", animals_output)
    write_html("animals.html", final_html)

    print("animals.html was created successfully.")


if __name__ == "__main__":
    main()