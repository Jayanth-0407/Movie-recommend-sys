import streamlit as st
import pandas as pd
import pickle
import requests
import joblib

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")


st.title('🎬 Movie Recommender System')

api_key=st.secrets["tmdb_api_key"]
# Load data
movie_list = pickle.load(open('movies.pkl', 'rb'))
similarity = joblib.load(open('similarity_compressed.pkl','rb'))
movies = pd.DataFrame(movie_list)

def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US")
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list_sorted = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list_sorted:
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movies.append(movies.iloc[i[0]]['title'])
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

selected_movie_name = st.selectbox('🎥 Enter the Movie Name:', movies['title'])

if st.button('Recommend'):

    names,posters=recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    
    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
