import pandas as pd
import streamlit as st
import pickle
import requests #to hit api



def fetch_poster(movie_id):
    response =requests.get('https://api.themoviedb.org/3/movie/{}?api_key=2022ba15ee845f44a82673c2b9f55a5e'.format(movie_id))
    data=response.json() # we have json
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path'] #provide poster path

def recommend(movie):
    movie_index= movies[movies['title'] == movie].index[0] # give index value
    distances= similarity[movie_index] #similarty
    movie_list= sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6] # give top 5 movie
    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movies.pkl','rb')) # Deserialization (unpickling) converts the byte stream back into the original Python object.
movies = pd.DataFrame(movies_dict) # dict to df

similarity= pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommendation')

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)  # Create 5 columns dynamically
    for i, col in enumerate(cols):  # Iterate through columns and recommendations
    # Create columns and populate with movie details
    #for i in range(5):  # 5 recommendations
    #    with st.columns(5)[i]:  # Access the ith column
         with col:
            st.text(names[i])
            st.image(posters[i])