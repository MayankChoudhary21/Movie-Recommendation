from flask import Flask, request, render_template
import pickle
import requests
import pandas as pd

# Load movie data and similarity matrix
movies = pickle.load(open('C:\\Users\\mayan\\Videos\\Movie-Recommendation\\Model\\movies_list.pkl', 'rb'))
similarity = pickle.load(open('C:\\Users\\mayan\\Videos\\Movie-Recommendation\\Model\\similarity.pkl', 'rb'))

# Function to fetch the movie poster
def fetch_poster(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key=450be0533dbb55a44add322a9abdbcb4&query={movie_name}"
    response = requests.get(url).json()
    if 'results' in response and len(response['results']) > 0:
        poster_path = response['results'][0].get('poster_path')
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
            return full_path
    return "https://via.placeholder.com/500x750?text=Poster+Not+Found"

# Function to recommend movies
def recommend(Movie):
    index = movies[movies['title'] == Movie].index[0]
    l = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    rmn = []
    rmp = []
    for i in l[1:5]:
        movie_title = movies.iloc[i[0]].title
        rmp.append(fetch_poster(movie_title))
        rmn.append(movie_title)
    return rmn, rmp

app = Flask(__name__)

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
            if request.form:
                movies_name = request.form.get('movies')
                rmn, rmp = recommend(movies_name)
                status = True
                return render_template(
                    "recommendation.html", 
                    movies_name=rmn, 
                    poster=rmp, 
                    movies_list=movie_list, 
                    status=status,
                    selected_movie=movies_name  # Added the selected movie to keep it selected in the dropdown
                )
        except Exception as e:
            error = {"error": str(e)}
            status = False
            return render_template(
                "recommendation.html", 
                error=error, 
                movies_list=movie_list, 
                status=status
            )
    else:
        return render_template("recommendation.html", movies_list=movie_list, status=status)

if __name__ == "__main__":
    app.run(debug=True)
