import streamlit as st
import pickle
import requests

# Load CSS styles
st.markdown('<style>' + open('styles.css').read() + '</style>', unsafe_allow_html=True)

# Load movie data and similarity matrix
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

# UI Setup
st.header("Movie Recommender System")
selectvalue = st.selectbox("Select movie from dropdown", movies_list)

# Function to fetch movie poster from an API
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=df3650663d6d7ad60457660b2f58e59f&language=en-US".format(movie_id)
    data=requests.get(url)
    data=data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path

# Function to recommend similar movies
def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_movie=[]
    recommend_poster=[]
    for i in distance[1:6]:
        movies_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie, recommend_poster

# Display recommended movies when button is clicked
if st.button("Show Recommended"):
    movie_name, movie_poster = recommend(selectvalue)
    col1,col2,col3,col4,col5=st.columns(5)

    # Display each recommended movie along with its poster
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
