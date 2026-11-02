import html

import data_fetcher


def read_template(file_path):
    """Read and return the HTML template."""
    with open(file_path, "r", encoding="utf-8") as handle:
        return handle.read()


def write_html(file_path, content):
    """Write the generated HTML to a file."""
    with open(file_path, "w", encoding="utf-8") as handle:
        handle.write(content)


def serialize_animal(animal_obj):
    """Convert one animal dictionary into an HTML card."""
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
            '      <li class="animal-details__item">'
            f"<strong>Diet:</strong> {diet}</li>\n"
        )

    if locations:
        first_location = html.escape(locations[0])
        output += (
            '      <li class="animal-details__item">'
            f"<strong>Location:</strong> {first_location}</li>\n"
        )

    if "type" in characteristics:
        animal_type = html.escape(characteristics["type"])
        output += (
            '      <li class="animal-details__item">'
            f"<strong>Type:</strong> {animal_type}</li>\n"
        )

    if "skin_type" in characteristics:
        skin_type = html.escape(characteristics["skin_type"])
        output += (
            '      <li class="animal-details__item">'
            f"<strong>Skin type:</strong> {skin_type}</li>\n"
        )

    output += "    </ul>\n"
    output += "  </div>\n"
    output += "</li>\n"

    return output


def serialize_animals(animals_data):
    """Convert a list of animals into HTML cards."""
    output = ""

    for animal in animals_data:
        output += serialize_animal(animal)

    return output


def main():
    """Generate a website using data from the data fetcher."""
    animal_name = input("Enter a name of an animal: ").strip()

    if not animal_name:
        print("Please enter an animal name.")
        return

    try:
        animals_data = data_fetcher.fetch_data(animal_name)
    except (RuntimeError, ValueError) as error:
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
