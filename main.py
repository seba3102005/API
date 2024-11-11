import requests

# Define the API endpoint and parameters
url = "http://www.omdbapi.com/?i=tt3896198&apikey=7cf8845d"
params = {
    
    "t": "Inception"  # Title of the movie you want to search for
}

try:
    # Send a GET request to fetch movie data
    response = requests.get(url, params=params)
    response.raise_for_status()  # Check if the request was successful
    
    # Convert the response to JSON
    movie_data = response.json()
    
    # Display some movie details
    if movie_data["Response"] == "True":
        print(f"Title: {movie_data['Title']}")
        print(f"Year: {movie_data['Year']}")
        print(f"Genre: {movie_data['Genre']}")
        print(f"Director: {movie_data['Director']}")
        print(f"Plot: {movie_data['Plot']}")
    else:
        print("Movie not found!")

except requests.exceptions.RequestException as e:
    print("An error occurred:", e)
