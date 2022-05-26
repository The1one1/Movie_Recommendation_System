from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel

from tmdbv3api import Movie, TMDb

import streamlit as st
from time import time

import pandas as pd
import numpy as np

import datetime
import requests

# from sklearn.metrics.pairwise import cosine_similarity


tmdb = TMDb()
tmdb.api_key = 'ef64cf7279087f589625d4f3e0ef5378'

data = pd.read_csv("movie_data.csv")


def title(nevigation):
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
    # sim = cosine_similarity(count_matrix, count_matrix)
    sim = linear_kernel(count_matrix, count_matrix)
    return data, sim


def recommend(m):
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


def ListOfGenres(genre_json):
    if genre_json:
        genres = []
        genre_str = ", "
        for i in range(0, len(genre_json)):
            genres.append(genre_json[i]['name'])
        return genre_str.join(genres)


def date_convert(s):
    MONTHS = ['January', 'February', 'Match', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    y = s[:4]
    m = int(s[5:-3])
    d = s[8:]
    month_name = MONTHS[m-1]

    result = month_name + ' ' + d + ' ' + y
    return result


def MinsToHours(duration):
    if duration % 60 == 0:
        return "{:.0f} hours".format(duration/60)
    else:
        return "{:.0f} hours {} minutes".format(duration/60, duration % 60)


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
        movie_name = result[0].title

        # making API call
        response = requests.get(
            'https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id, tmdb.api_key))
        data_json = response.json()
        imdb_id = data_json['imdb_id']
        poster = data_json['poster_path']
        img_path = 'https://image.tmdb.org/t/p/original{}'.format(poster)

        # getting list of genres form json
        genre = ListOfGenres(data_json['genres'])
        # getting votes with comma as thousands separators
        vote_count = "{:,}".format(result[0].vote_count)

        # convert date to readable format (eg. 10-06-2019 to June 10 2019)
        try:
            rd = date_convert(result[0].release_date)
        except:
            pass

        # convert minutes to hours minutes (eg. 148 minutes to 2 hours 28 mins)
        runtime = MinsToHours(data_json['runtime'])

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


output = st.sidebar.radio("Nevigation", ["Movie", "Popular", "Top Rated", "Recently Released", "Rate the Movie"])

if output == "Movie":
    # to take input(movie name) from user
    selected_movie_name = title('Movie')

    if st.button("Recommend"):
        recommendations = recommend(selected_movie_name)
        posters = get_posters(recommendations)

        list = []
        list.append(selected_movie_name)
        # it will show the selected movie details
        movie_details(list)     

        # to display the Poster of recommended movies in sidebar
        st.sidebar.subheader("Recommendations")
        st.sidebar.image(posters)

        # to show the details of recommended movies
        st.header("Recommendations")
        movie_details(recommendations)


elif output == "Popular":
    title('Popular')

    # get popular movies on the basis of genre
    genre = st.sidebar.selectbox("Select Genre", ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Family",
                                                "Fantasy", "History", "Horror", "Music", "Mystery", "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"])

    genre_id = {"Action": 28, "Adventure": 12, "Animation": 16, "Comedy": 35, "Crime": 80, "Documentary": 99, "Drama": 18, "Family": 10751, "Fantasy": 14, "History": 36,
                "Horror": 27, "Music": 10402, "Mystery": 9648, "Romance": 10749, "Science Fiction": 878, "TV Movie": 10770, "Thriller": 53, "War": 10752, "Western": 37}

    if st.button("Recommend") or st.sidebar.button("Recommend", key="pop"):
        tmdb_movie = Movie()
        result = tmdb_movie.popular()

        recommendations = []
        # from all popular movies get the movies of selected genre
        for i in range(len(result)):
            # check if the movie is of selected genre
            if genre_id[genre] in result[i]['genre_ids']:
                recommendations.append(result[i].title)

        if len(recommendations) == 0:
            # if no movie is found
            st.error("No recommendations found")
            st.sidebar.error("No recommendations found")
        else:
            # if movie is found then get the posters then display in sidebar
            posters = get_posters(recommendations)
            st.sidebar.subheader("Recommendations")
            st.sidebar.image(posters)

            # to show the details of recommended movies
            st.header("Recommendations")
            movie_details(recommendations)


elif output == "Top Rated":
    title('Top Rated')

    movie = Movie()
    top_rated_movies = movie.top_rated()
    movie_list = []

    for i in range(len(top_rated_movies)):
        movie_list.append(top_rated_movies[i].title)

    movie_details(movie_list)


elif output == "Recently Released":
    title('Recently Released')

    movie = Movie()
    upcoming_movies = movie.upcoming()
    movie_list = []
    for i in range(len(upcoming_movies)):
        movie_list.append(upcoming_movies[i].title)

    movie_details(movie_list)


elif output == "Rate the Movie":

    movie_name = title('Rate the Movie')

    st.subheader("Rating of the movie: " + movie_name)

    # slider to get the rating of the movie
    rating = st.slider("Rate the movie", 1, 10)

    # date of last rating
    date = datetime.datetime.now().strftime("%d-%m-%Y")

    # time of last rating
    time = datetime.datetime.now().strftime("%H:%M:%S")

    # name of last user who rated the movie
    user = st.text_input("Enter your name:")

    if st.button("Rate"):

        data = pd.read_csv("users_movie_rating.csv")

        # add the data to particular row and particular column of csv file
        for i in range(len(data)):

            # check movie_title matches with movie name
            if data["movie_title"].values[i] == movie_name:

                # check if value is nan
                if np.isnan(data["rating"].values[i]):
                    data["rating"].values[i] = 0.0

                if np.isnan(data['vote_count'].values[i]):
                    data['vote_count'].values[i] = 0.0

                x = ((data["rating"].values[i] * data['vote_count'].values[i]) + float(rating)) / (data['vote_count'].values[i] + 1.0)

                data["rating"].values[i] = x
                data["date"].values[i] = date
                data["time"].values[i] = time
                data["user"].values[i] = user
                data['vote_count'].values[i] += 1

                # write the data to csv file
                data.to_csv("users_movie_rating.csv", index=False)
                break

        st.success("Data Submitted")
        st.write("Thanks for rating the movie")
        st.write("Your contribution will help us to improve our app")


        # to display the rating of the movie in sidebar
        st.sidebar.subheader("Movie: " + movie_name)
        # show rating of the movie movie_name
        st.sidebar.write("Rating = ", data[data["movie_title"] == movie_name]["rating"].values[0])

        # no of votes of the movie movie_name
        st.sidebar.write("No of Votes = ", int(data[data["movie_title"] == movie_name]["vote_count"].values[0]))