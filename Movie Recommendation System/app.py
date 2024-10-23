from sqlalchemy import String
import streamlit as st
import pickle
import pandas as pd
import requests
import re

st.set_page_config(page_title="Movies Recommendation System")
st.title("Movie Recommended System")
movie_list = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = pd.DataFrame(movie_list)

Selected_movie_name = st.selectbox(
    'Select the Movie : ',
    movies['title'].values)


def fetch_poster(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=1e32074c3e6f19923a32e360d904dfd3&language=en-US".format(
            movie_id))
    data = response.json()
    # st.write("https://image.tmdb.org/t/p/original" + data['poster_path'])
    return "https://image.tmdb.org/t/p/original" + data['poster_path']


def recommend_movie(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movies = []
    recommend_movies_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        # poster fetching
        recommend_movies_poster.append(fetch_poster(movie_id))
        recommend_movies.append(movies.iloc[i[0]].title)
    return recommend_movies, recommend_movies_poster


def detail_movie(movie):
    movie_id = movies[movies['title'] == movie]['movie_id'].iloc[0]
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=5f0351ee87c6c492b41120ffd369c3c3&language=en-US".format(
            movie_id))
    data = response.json()
    st.subheader("Title : " + data['original_title'])
    st.image(fetch_poster(movie_id), width=200)
    imdb = data['imdb_id']
    st.subheader("Movie IMdb ID : "+imdb)
    st.subheader("Genres : ")
    for i in range(len(data['genres'])):
        st.markdown("- " + data['genres'][i]['name'])
    st.subheader("Overview : ")
    st.write(data['overview'])
    st.write("Release Date : "+re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', data['release_date']))
    st.write("Budget of the Movie : "+str(data['budget'])+" $")
    st.write("Popularity : "+str(data['popularity']))
    st.write("Revenue : "+str(data['revenue']))
    st.write('Movie Runtime : '+str(data['runtime'])+" Minutes")
    # cast_data = requests.get("https://api.themoviedb.org/3/movie/{}/credits?api_key=5f0351ee87c6c492b41120ffd369c3c3&language=en-US".format(movie_id)).json()
    # st.subheader("Actors : ")
    # castdata =  Convert1(cast_data['cast'])
    # for i in castdata:
    #       st.write(i)
    #       st.image()


# def Convert1(obj):
#     counter = 0
#     for i in obj: 
#         if counter!=5 and i is not None:
#             if i["known_for_department"]=="Acting":
#                     st.write(i['name'])
#                     st.image("https://image.tmdb.org/t/p/original" + i['profile_path'],width=100)
#             counter+=1
    

if st.button('Get Details'):
    detail_movie(Selected_movie_name)

if st.button('Recommend'):
    names, poster = recommend_movie(Selected_movie_name)
    st.subheader("Recommended Movies Are : ")
    # for i in names:
    #     st.write(i)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(poster[0])

    with col2:
        st.text(names[1])
        st.image(poster[1])

    with col3:
        st.text(names[2])
        st.image(poster[2])

    with col4:
        st.text(names[3])
        st.image(poster[3])

    with col5:
        st.text(names[4])
        st.image(poster[4])
