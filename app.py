from flask import Flask, request, render_template
import pickle
import requests
import pandas as pd
import os

app = Flask(__name__)

# Google Drive File ID for similarity.pkl
DRIVE_FILE_ID = "126jQebNH7l-GeGaBCJR3_ruuDXNCfjpo"

# Ensure Model folder exists
MODEL_DIR = os.path.join(os.path.dirname(__file__), "Model")
os.makedirs(MODEL_DIR, exist_ok=True)

# Paths for model files
MOVIES_PATH = os.path.join(MODEL_DIR, "movies_list.pkl")
SIMILARITY_PATH = os.path.join(MODEL_DIR, "similarity.pkl")


def download_similarity():
    """Download similarity.pkl from Google Drive if it doesn't exist."""
    if not os.path.exists(SIMILARITY_PATH):
        print("Downloading similarity.pkl from Google Drive...")
        url = f"https://drive.google.com/uc?id={DRIVE_FILE_ID}"
        response = requests.get(url)
        
        with open(SIMILARITY_PATH, "wb") as f:
            f.write(response.content)
        
        print("Download complete.")


# Download similarity.pkl if missing
download_similarity()

# Load movie data and similarity matrix
try:
    with open(MOVIES_PATH, "rb") as f:
        movies = pickle.load(f)
except FileNotFoundError:
    print(f"Error: {MOVIES_PATH} not found! Ensure it exists in the Model folder.")
    exit(1)

try:
    with open(SIMILARITY_PATH, "rb") as f:
        similarity = pickle.load(f)
except FileNotFoundError:
    print(f"Error: {SIMILARITY_PATH} not found! Ensure it exists in the Model folder.")
    exit(1)


# Function to fetch movie posters from TMDb API
def fetch_poster(movie_name):
    api_key = "450be0533dbb55a44add322a9abdbcb4"
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"
    response = requests.get(url).json()
    
    if 'results' in response and len(response['results']) > 0:
        poster_path = response['results'][0].get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    
    return "https://via.placeholder.com/500x750?text=Poster+Not+Found"


# Function to recommend movies
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        sorted_movies = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

        recommended_movies = []
        recommended_posters = []

        for i in sorted_movies[1:6]:  # Get top 5 recommendations
            movie_title = movies.iloc[i[0]].title
            recommended_posters.append(fetch_poster(movie_title))
            recommended_movies.append(movie_title)

        return recommended_movies, recommended_posters
    except Exception as e:
        print(f"Error in recommendation: {e}")
        return [], []


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

    if request.method == "POST":
        try:
            movie_name = request.form.get('movies')
            recommended_movies, recommended_posters = recommend(movie_name)
            status = True

            return render_template(
                "recommendation.html",
                movies_name=recommended_movies,
                poster=recommended_posters,
                movies_list=movie_list,
                status=status,
                selected_movie=movie_name
            )
        except Exception as e:
            return render_template(
                "recommendation.html",
                error={"error": str(e)},
                movies_list=movie_list,
                status=False
            )

    return render_template("recommendation.html", movies_list=movie_list, status=status)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get port dynamically for deployment
    app.run(host='0.0.0.0', port=port, debug=True)
