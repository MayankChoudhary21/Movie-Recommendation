from flask import Flask, request, render_template
import pickle
import requests
import pandas as pd
import os

# Get the base directory dynamically
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "Model")  # Model files are inside the "Model" folder

# Load movie data and similarity matrix with error handling
try:
    movies = pickle.load(open(os.path.join(MODEL_DIR, "movies_list.pkl"), "rb"))
    similarity = pickle.load(open(os.path.join(MODEL_DIR, "movies.pkl"), "rb"))  # Ensure this is the correct similarity matrix
except FileNotFoundError as e:
    print(f"Error: {e}. Ensure that 'movies_list.pkl' and 'movies.pkl' exist in the 'Model' folder.")
    exit(1)

# Function to fetch the movie poster
def fetch_poster(movie_name):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key=450be0533dbb55a44add322a9abdbcb4&query={movie_name}"
        response = requests.get(url).json()
        
        if 'results' in response and len(response['results']) > 0:
            poster_path = response['results'][0].get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
        return "https://via.placeholder.com/500x750?text=Poster+Not+Found"
    except Exception as e:
        print(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Poster"

# Function to recommend movies
def recommend(Movie):
    try:
        if Movie not in movies['title'].values:
            print(f"Movie '{Movie}' not found in database.")
            return [], []  # Return empty lists if movie not found

        index = movies[movies['title'] == Movie].index[0]
        
        if index >= len(similarity):
            print(f"Error: Index {index} out of bounds for similarity matrix.")
            return [], []

        sorted_movies = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

        recommended_movies = []
        recommended_posters = []

        for i in sorted_movies[1:6]:  # Recommend top 5 movies
            movie_title = movies.iloc[i[0]].title
            recommended_posters.append(fetch_poster(movie_title))
            recommended_movies.append(movie_title)

        return recommended_movies, recommended_posters
    except Exception as e:
        print(f"Error in recommendation function: {e}")
        return [], []

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/recommendation", methods=['GET', 'POST'])
def recommendation():
    movie_list = movies['title'].values
    status = False
    recommended_movies = []
    recommended_posters = []
    selected_movie = None
    error_message = None

    if request.method == "POST":
        movie_name = request.form.get('movies')

        if not movie_name:
            error_message = "Please select a movie."
        else:
            recommended_movies, recommended_posters = recommend(movie_name)
            selected_movie = movie_name
            status = bool(recommended_movies)  # Only set True if recommendations exist
            if not status:
                error_message = f"Could not find recommendations for '{movie_name}'."

        return render_template(
            "recommendation.html",
            movies_name=recommended_movies,
            poster=recommended_posters,
            movies_list=movie_list,
            status=status,
            selected_movie=selected_movie,
            error=error_message
        )

    return render_template("recommendation.html", movies_list=movie_list, status=status)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get port dynamically for Render
    app.run(host='0.0.0.0', port=port, debug=True)
