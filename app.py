import streamlit as st
import pickle
import pandas as pd
import requests

lis = pickle.load(open('moviesDf_Dict.pkl', 'rb'))
listOfMovies = pd.DataFrame(lis)

similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
def recommend(movie):
    index = listOfMovies[listOfMovies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_posters=[]
    for i in distances[1:6]:
        id = listOfMovies.iloc[i[0]].id
        recommended_posters.append(fetch_poster(id))
        recommended_movies.append(listOfMovies.iloc[i[0]].title)

    return recommended_movies, recommended_posters

st.title("Movie recommender system")
st.write("(Collaborative approach)")

option = st.selectbox('Enter a movie name and click recommend', listOfMovies['title'].values)

if st.button("Recommend", type="primary"):
    recommended_movies,recommended_movie_posters = recommend(option)
    num_columns = 3
    num_rows = (len(recommended_movies) + num_columns - 1) // num_columns
    columns = st.columns(num_columns)

    for row in range(num_rows):
        for col in range(num_columns):
            index = row * num_columns + col
            if index < len(recommended_movies):
                columns[col].image(recommended_movie_posters[index], width=125)
                columns[col].write(f"**{recommended_movies[index]}**")

