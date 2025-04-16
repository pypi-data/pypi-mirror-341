import argparse
import json
from requests import get

API_KEY = "cfc03e93"

# The three types that the OMDB API can search for
TYPES = ["movie", "series", "episode"]

def test_api_connection(apikey):
    """Checks if the provided API key successfully connects to the OMDB API."""
    try:
        response = get("http://www.omdbapi.com", params={"apikey": apikey, "s": "test"})
        if response.status_code == 200 and response.json().get("Response") == "True":
            return True
        return False
    except Exception as e:
        print(f"Error connecting to the API: {e}")
        return False

def search_movies(query, search_type="movie"):
    """Returns a list of OMDB items based on the search query and type."""
    if search_type not in TYPES:
        print(f"Invalid type: {search_type}. Valid types are {TYPES}.")
        return []

    params = {"apikey": API_KEY, "s": query, "type": search_type}
    try:
        response = get("http://www.omdbapi.com", params=params)
        if response.status_code == 200:
            data = response.json()
            if data["Response"] == "True":
                return data["Search"]
            else:
                print(f"No results found for query: {query}")
                return []
        else:
            print(f"Error fetching data: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error during the API request: {e}")
        return []

def get_movie_info(imdb_id):
    """Fetch detailed information for a movie or series based on IMDb ID."""
    params = {"apikey": API_KEY, "i": imdb_id}
    try:
        response = get("http://www.omdbapi.com", params=params)
        if response.status_code == 200:
            data = response.json()
            if data["Response"] == "True":
                return data
            else:
                print(f"Movie not found with IMDb ID: {imdb_id}")
                return {}
        else:
            print(f"Error fetching data: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Error during the API request: {e}")
        return {}

def save_to_file(filename, data):
    """Saves the data to a JSON file."""
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Results saved to {filename}")
    except Exception as e:
        print(f"Error writing to file: {e}")

def main():
    """Main function to handle user input and call necessary functions."""
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(description="Search for movies, series, or episodes on OMDB.")
    parser.add_argument("query", help="The search query (e.g. movie title or TV series name).")
    parser.add_argument("--type", choices=TYPES, default="movie", help="The type of media to search for (default: movie).")
    parser.add_argument("--output", help="Optional output file to save the results.")
    parser.add_argument("--info", help="Get detailed information about a specific movie/series by IMDb ID.")

    try:
        args = parser.parse_args()
    except SystemExit:
        print("Error: Invalid arguments or missing arguments.")
        parser.print_help()
        return

    # Check if the API key is valid
    if not test_api_connection(API_KEY):
        print("Invalid API key. Please check your API key and try again.")
        return

    if args.info:
        # Fetch detailed info for a movie/series using IMDb ID
        movie_info = get_movie_info(args.info)
        if movie_info:
            print(json.dumps(movie_info, indent=4))
    else:
        # Search for movies/series based on the query and type
        search_results = search_movies(args.query, args.type)
        if search_results:
            # If an output file is provided, save the results to that file
            if args.output:
                save_to_file(args.output, search_results)
            else:
                # Print the search results to the console
                print(json.dumps(search_results, indent=4))

if __name__ == "__main__":
    main()
