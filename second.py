import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from tmdbv3api import Movie, TMDb
import streamlit as st
import pandas as pd

import Converter
import requests

tmdb = TMDb()
tmdb.api_key = 'ef64cf7279087f589625d4f3e0ef5378'


def title(nevigation):
    data = pd.read_csv("movie_data.csv")
    if nevigation == 'Movie':
        st.title('Movie Recommender')
        return st.selectbox("Enter the movie:(Release till 2016)", data["movie_title"].values)
    elif nevigation == 'Popular':
        st.title('Popular Movies')
    elif nevigation == 'Top Rated':
        st.title('Top Rated Movies')
    elif nevigation == 'Rate the Movie':
        st.title('Give Rating')
        return st.selectbox("Enter the movie:(Release till 2016)", data["movie_title"].values)
    else:
        st.title('Recently Released Movies')


def create_sim():
    data = pd.read_csv('movie_data.csv')
    # creating a count matrix
    cv = CountVectorizer(stop_words='english')

    count_matrix = cv.fit_transform(data['comb'])
    # creating a similarity score matrix
    sim = linear_kernel(count_matrix, count_matrix)
    return data, sim


def get_posters(r):
    poster = []
    tmdb_movie = Movie()
    for movie_title in r:
        list_result = tmdb_movie.search(movie_title)
        movie_id = list_result[0].id
        response = requests.get(
            'https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id, tmdb.api_key))
        data_json = response.json()
        poster.append(
            'https://image.tmdb.org/t/p/original{}'.format(data_json['poster_path']))
    return (poster)


def movie_details(recommendations):

    for selected_movie_name in recommendations:
        tmdb_movie = Movie()
        result = tmdb_movie.search(selected_movie_name)

        # get movie id and movie title
        movie_id = result[0].id
        # movie_name = result[0].title

        # making API call
        response = requests.get(
            'https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id, tmdb.api_key))
        data_json = response.json()
        poster = data_json['poster_path']
        img_path = 'https://image.tmdb.org/t/p/original{}'.format(poster)

        # getting list of genres form json
        genre = Converter.ListOfGenres(data_json['genres'])

        # getting votes with comma as thousands separators
        vote_count = "{:,}".format(result[0].vote_count)

        # convert date to readable format (eg. 10-06-2019 to June 10 2019)
        try:
            rd = Converter.date_convert(result[0].release_date)
        except:
            pass

        # convert minutes to hours minutes (eg. 148 minutes to 2 hours 28 mins)
        runtime = Converter.MinsToHours(data_json['runtime'])

        col1, col2 = st.columns(2)
        with col1:
            st.image(img_path)
        with col2:
            st.subheader("TITLE: " + selected_movie_name.upper())
            st.write(result[0].overview)
            st.write(result[0].vote_average, "("+vote_count+"votes)")
            st.write(genre)
            st.write("Release Date: " + rd)
            st.write("Runtime: "+runtime)


def side_bar_poster(movie_list):
    posters = get_posters(movie_list)
    st.sidebar.subheader("Recommendations")
    st.sidebar.image(posters)


def recommend(m):
    data = pd.read_csv("movie_data.csv")
    m = m.lower()
    try:
        data.head()
        sim.shape
    except:
        data, sim = create_sim()
    if m not in data['movie_title'].unique():
        return('Sorry! The movie your searched is not in our database. Please check the spelling or try with some other movies')
    else:
        i = data.loc[data['movie_title'] == m].index[0]
        lst = list(enumerate(sim[i]))
        lst = sorted(lst, key=lambda x: x[1], reverse=True)

        lst = lst[1:20]
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['movie_title'][a])
        unique_lst = []
        for x in l:
            if x not in unique_lst:
                unique_lst.append(x)
        unique_lst = unique_lst[:11]
        return unique_lst


def get_genre():
    genre = st.sidebar.selectbox("Select Genre", ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Family",
                "Fantasy", "History", "Horror", "Music", "Mystery", "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"])
    return genre


def success_message(data, movie_name):
    st.success("Data Submitted")
    st.write("Thanks for rating the movie")
    st.write("Your contribution will help us to improve our app")

    # to display the rating of the movie in sidebar
    st.sidebar.subheader("Movie: " + movie_name)

    # show rating of the movie movie_name
    st.sidebar.write(
        "Rating = ", data[data["movie_title"] == movie_name]["rating"].values[0])

    # no of votes of the movie movie_name
    st.sidebar.write("No of Votes = ", int(
        data[data["movie_title"] == movie_name]["vote_count"].values[0]))


def avg_rating(data, rating, i):
    # average of rating
    total_rating = (data["rating"].values[i] * data['vote_count'].values[i])

    # after adding new rating
    total_rating += rating

    # average of rating
    return total_rating / (data['vote_count'].values[i] + 1.0)


# select the genre of the movie from the database
def movie_genre(movie_genre, data):

    genre = data["genres"]
    movie_names = data["movie_title"]
    genre_list = genre.str.split(' ')
    # remove empty string's from genre_list
    # genre_list = genre_list.apply(lambda x: [i for i in x if i != ''])

    # dictionary of genre and movie names
    genre_dict = dict(zip(movie_names, genre_list))

    recommendation = []

    for key, value in genre_dict.items():
        if movie_genre in value:
            recommendation.append(key)
        if len(recommendation) > 15:
            break

    return recommendation


def movie_current_rating(movie_name, data):
    # show rating of the movie movie_name in same line

    if np.isnan(data[data["movie_title"] == movie_name]["rating"].values[0]):
        st.write("Current Rating = ", "Not Rated")
    else:
        st.write("Current Rating = ",
                data[data["movie_title"] == movie_name]["rating"].values[0])

    if np.isnan(data[data["movie_title"] == movie_name]["vote_count"].values[0]):
        st.write("No of Votes = ", 0)
    else:
        st.write("No of Votes = ",
                data[data["movie_title"] == movie_name]["vote_count"].values[0])