import flask
import json
from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

app = flask.Flask(__name__, template_folder='templates')

with open('./model/tmdb.json', 'r') as json_file:
    data = json.load(json_file)
df2 = pd.DataFrame(data)
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['soup'])

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

df2 = df2.reset_index()
indices = pd.Series(df2.index, index=df2['title'])
all_titles = df2['title'].tolist()

def get_recommendations(title):
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    tit = df2['title'].iloc[movie_indices]
    dat = df2['release_date'].iloc[movie_indices]
    rating = df2['vote_average'].iloc[movie_indices]
    moviedetails=df2['overview'].iloc[movie_indices]
    movietypes=df2['keywords'].iloc[movie_indices]
    movieid=df2['id'].iloc[movie_indices]

    return_df = pd.DataFrame(columns=['Title','Year'])
    return_df['Title'] = tit
    return_df['Year'] = dat
    return_df['Ratings'] = rating
    return_df['Overview']=moviedetails
    return_df['Types']=movietypes
    return_df['ID']=movieid
    return return_df

def get_suggestions():
    return df2['title'].str.capitalize().tolist()

@app.route("/")
@app.route("/index")
def index():
    NewMovies=[]
    new_movie = random.choice(all_titles)
    NewMovies.append([new_movie])
    m_name = new_movie.title()
    
    with open('movieR.json', 'a') as json_file:
        json.dump({'Movie': m_name}, json_file)
        
    result_final = get_recommendations(m_name)
    names = result_final['Title'].tolist()
    dates = result_final['Year'].tolist()
    ratings = result_final['Ratings'].tolist()
    overview = result_final['Overview'].tolist()
    types = result_final['Types'].tolist()
    mid = result_final['ID'].tolist()
    
    suggestions = get_suggestions()
    
    return render_template('index.html', suggestions=suggestions, movie_type=types[5:], movieid=mid,
                           movie_overview=overview, movie_names=names, movie_date=dates, movie_ratings=ratings,
                           search_name=m_name)

if __name__ == '__main__':
    app.run()
