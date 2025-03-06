# Movie Recommendation System

This project implements a movie recommendation system using Flask, where users can select a movie from a dropdown, and the system recommends similar movies based on the user's choice. The recommendations are fetched using a pre-trained movie similarity model, and posters of the recommended movies are displayed.

## Features
- **Movie Selection**: Users can choose a movie from a dropdown menu.
- **Recommendations**: Once a movie is selected, the system recommends 4 similar movies based on content similarity.
- **Posters**: The posters of the recommended movies are fetched using the Movie Database API.
- **Error Handling**: In case of any errors, proper error messages are displayed.

## Technologies Used
- **Flask**: Web framework for the backend.
- **Pickle**: Used to load the pre-trained models (`movies_list.pkl` and `similarity.pkl`).
- **Requests**: For making API calls to fetch movie posters from The Movie Database API.
- **HTML/CSS**: For frontend rendering and styling.

![image](https://github.com/user-attachments/assets/33dd9eba-7dfd-4470-9687-9621e67cb099)
![image](https://github.com/user-attachments/assets/1ba1522d-9200-4a2f-bacc-ccd3ee84692c)

Download the dataset :https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_movies.csv

## Project Structure:
![WhatsApp Image 2025-01-17 at 02 35 32_68e32cd3](https://github.com/user-attachments/assets/d99dc56d-902a-4262-a580-27773fcff4d5)
## Deployed Website:
https://movie-recommendation-tstb.onrender.com/recommendation





