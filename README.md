# Movie_Recommendation_System

It is the Content Based Recommender System that recommends movies similar to the movie user likes.

In this recommender system the content of the movie (overview, cast, crew, keyword, tagline etc) is used to find its similarity with other movies. Then the movies that are most likely to be similar are recommended.

## Tech Stack
**Python Framework [Streamlit](https://streamlit.io/)<br>**
**[IMDb]( https://www.themoviedb.org/) API Key**
## How to get the API key?

Create an account in https://www.themoviedb.org/ 

click on the API link from the left hand sidebar in your account settings and fill all the details to apply for API key. 

If you are asked for the website URL, just give "NA" if you don't have one. You will see the API key in your API sidebar once your request is approved.


### Following functionalities can be performed by the user: <br>
• **Select the movie and it will Recommend all the related movies**<br>
• **Find movies according to genre**<br>
• **Top rated movies** <br>
• **Recently Released movies.** <br>
. **Give Rating to the movie.**

## How To Run ?
- clone it on your computer
- make a separate [python virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) or use the default one already installed on your machine
- run **``` pip install -r requirements.txt inside \movie-recommendation-system-master ```** directory
- Run **``` stramlit run app.py ```** inside **``` \movie-recommendation-system-master ```** directory to run the project
- Enjoy !

