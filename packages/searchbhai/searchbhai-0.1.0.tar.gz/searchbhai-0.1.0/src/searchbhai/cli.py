import argparse
import requests
import json

def get_definition(word):
    """Fetches the definition of a word from the Free Dictionary API."""
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:    
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return f"Error connecting to the API: {e}"
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"Word '{word}' not found."
        else:
            return f"API error: {e}"
    except json.JSONDecodeError:
        return "Error decoding the API response."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def extract_definitions_from_json(data):
    """Parses the JSON response and extracts the first definition."""
    if isinstance(data, list) and data and data[0].get('meanings'):
        definitions = data[0]['meanings'][0].get('definitions', [])
        if definitions:
            return [definitions[0].get('definition', 'No definition found.')]
    return ["No definition found."]

def main():
    parser = argparse.ArgumentParser(description="Look up the definition of a word.")
    parser.add_argument("word", nargs='?', help="The word to define.")
    parser.add_argument("-o", "--output", help="Optional: Save output to a file.")
    args = parser.parse_args()
    word_to_lookup = args.word
    output_file = args.output

    if not word_to_lookup:
        word_to_lookup = input("Enter a word to look up: ")
        if not word_to_lookup:
            print("No word entered. Exiting.")
            return

    result = get_definition(word_to_lookup)

    if isinstance(result, list):
        definitions = extract_definitions_from_json(result)
        output_string = f"Definition of '{word_to_lookup}': {definitions[0]}\n"
    else:
        output_string = result + "\n"

    if output_file:
        try:
            with open(output_file, 'w') as f:
                f.write(output_string)
            print(f"Definition saved to '{output_file}'.")
        except IOError:
            print(f"Error writing to '{output_file}'.")
    else:
        print(output_string)

if __name__ == "__main__":
    main()