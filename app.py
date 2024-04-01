import streamlit as st
import pandas as pd
import pickle
import sklearn
import requests


def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=2182e16d650c9ae4f1b8af4b58952fae'.format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended, recommended_movies_posters


movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Determine the number of columns based on the length of recommendations
    num_columns = len(names)

    # Create columns to display posters dynamically
    cols = st.columns(num_columns)

    for i in range(num_columns):
        with cols[i].container():
            st.image(posters[i], caption=names[i], use_column_width=True, output_format="JPEG")
