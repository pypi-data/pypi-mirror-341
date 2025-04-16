# MovieApp Command-Line Tool

This is a command-line tool for searching movies, TV series, and episodes using the OMDB API. The program allows you to search for movies or series, retrieve detailed information, and save the results to a file. It is designed to be run from the terminal and accepts several arguments to customize the search.

## Setup

1. Make sure you have Python installed.
2. Install the `requests` library if not already installed:
   ```bash
   pip install requests
   ```
3. Navigate to the project folder and install dependencies using Poetry:

   ```bash
   cd /path/to/your/project
   poetry install
    ```
4. Clone or download this repository.

## How to Use

To use the command-line tool, you can run the program with different arguments depending on what you want to do.

The program expects at least one argument: a **search query**. The search query is the name of the movie, TV series, or episode you are looking for.

### Search for Movies or Series

To search for movies, TV series, or episodes, run the following command:

```bash
poetry run movinf "Movie Name"
```