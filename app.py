from tmdbv3api import Movie
import streamlit as st

from time import time
import pandas as pd
import numpy as np
import datetime

import second


output = st.sidebar.radio("Nevigation", ["Movie", "Popular", "Top Rated", "Recently Released", "Rate the Movie"])

if output == "Movie":
    selected_movie_name = second.title('Movie')     # to take input(movie name) from user

    if st.button("Recommend"):
        recommendations = second.recommend(selected_movie_name)

        list = []
        list.append(selected_movie_name)

        second.movie_details(list) # it will show the selected movie details

        second.side_bar_poster(recommendations) # to display the Poster of recommended movies in sidebar

        # to show the details of recommended movies
        st.header("Recommendations")
        second.movie_details(recommendations)


elif output == "Popular":
    second.title('Popular')
    genre = second.get_genre()  # to get the genre of the movie from user

    if st.button("Recommend") or st.sidebar.button("Recommend", key="pop"):
        data = pd.read_csv("users_movie_rating.csv")
        recommendations = second.movie_genre(genre, data)

        # if no movie is found
        if len(recommendations) == 0:
            st.error("No recommendations found")
            st.sidebar.error("No recommendations found")
        else:
            second.side_bar_poster(recommendations)  # if movie is found then get the posters then display in sidebar

            # to show the details of recommended movies
            st.header("Recommendations")
            second.movie_details(recommendations)


elif output == "Top Rated":
    second.title('Top Rated')

    movie = Movie()
    top_rated_movies = movie.top_rated()
    movie_list = []

    for i in range(len(top_rated_movies)):
        movie_list.append(top_rated_movies[i].title)

    second.side_bar_poster(movie_list)
    second.movie_details(movie_list)


elif output == "Recently Released":
    second.title('Recently Released')

    movie = Movie()
    upcoming_movies = movie.upcoming()
    movie_list = []
    for i in range(len(upcoming_movies)):
        movie_list.append(upcoming_movies[i].title)

    second.side_bar_poster(movie_list)
    second.movie_details(movie_list)


elif output == "Rate the Movie":

    data = pd.read_csv("users_movie_rating.csv")
    movie_name = second.title('Rate the Movie')
    st.subheader("Rating of the movie: " + movie_name)

    try:
        second.movie_current_rating(movie_name, data)
    except:
        pass

    rating = st.slider("Rate the movie", 1, 10)  # slider to get the rating of the movie

    date = datetime.datetime.now().strftime("%d-%m-%Y")  # date of last rating

    time = datetime.datetime.now().strftime("%H:%M:%S")  # time of last rating

    user = st.text_input("Enter your name:")

    if st.button("Rate"):

        for i in range(len(data)):

            # check movie_title matches with movie name
            if data["movie_title"].values[i] == movie_name:

                # check if value is nan
                if np.isnan(data["rating"].values[i]):
                    data["rating"].values[i] = 0.0

                if np.isnan(data['vote_count'].values[i]):
                    data['vote_count'].values[i] = 0.0

                data["rating"].values[i] = second.avg_rating(data, rating, i)
                data["date"].values[i] = date
                data["time"].values[i] = time
                data["user"].values[i] = user
                data['vote_count'].values[i] += 1

                # write the data to csv file
                data.to_csv("users_movie_rating.csv", index=False)
                break

        second.success_message(data, movie_name)