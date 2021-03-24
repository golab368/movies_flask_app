from flask import Flask, request, render_template, redirect, flash,url_for
from tmdb_client import get_single_movie
import tmdb_client
from flask import request
from  database import show_favorite,insert_data,delete_from_favorite
import os
from dotenv import load_dotenv

app = Flask(__name__, template_folder='template')
load_dotenv()
app.secret_key = os.environ['SECRET_KEY']

@app.route('/')
def homepage():

    selected_list = request.args.get('list_type', "popular")


    buttons = [
        {"list_type": "now_playing", "active": "", "display_text": "now playing"},
        {"list_type": "popular", "active": "", "display_text": "popular"},
        {"list_type": "upcoming", "active": "", "display_text": "upcoming"},
        {"list_type": "top_rated", "active": "", "display_text": "top rated"},
        {"list_type": "favorites", "active": "", "display_text": "favorites"},
    ]

    """if selected_list not in ["now_playing", "upcoming", "top_rated","favorites"]:
        selected_list = "popular"""


    for button in buttons:
        if button['list_type'] == selected_list:
            button['active'] = 'active'

    if selected_list =="favorites":
        favorite_list = show_favorite()
        list_of_favorites = [get_single_movie(i) for i in favorite_list]
        if not favorite_list:
            flash("You dont have favorites movies", "alert-danger")
            return redirect(url_for("homepage"))
        return render_template("homepage.html",current_list=selected_list,buttons=buttons, list_of_favorites=list_of_favorites)

    else:
        movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
        return render_template("homepage.html",current_list=selected_list,buttons=buttons, movies=movies)

  
@app.route("/add_to_favorites/<favorite_movie>", methods=["GET", "POST"])
def add_to_favorites(favorite_movie):
    
    if request.method == "POST":
        try:
            favorite_list = show_favorite()
            if favorite_movie in favorite_list:
                flash("You already added this movie", "alert-danger")
                return redirect(request.referrer)
            else:
                insert_data(favorite_movie)
                flash("Successfully added!", "alert-success")
                return redirect(request.referrer)
        except:
            flash("There was an error try againg", "alert-danger")
            


@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    backdrop_path = details["backdrop_path"]
    base_url_for_backdrop_path = "https://image.tmdb.org/t/p/w500/"
    ready_backdrop_path = f"{base_url_for_backdrop_path}{backdrop_path}"
    cast = tmdb_client.get_single_movie_cast(movie_id)
    return render_template("movie_details.html", movie=details, ready_backdrop_path=ready_backdrop_path, cast=cast)


@app.route("/favorites")
def show_favorites():

    favorite_list = show_favorite()
    list_of_favorites = [get_single_movie(i) for i in favorite_list]
    if not favorite_list:
        flash("You don have favorites movies yet")
        return redirect(url_for('homepage'))
        
    return render_template("favorites.html", list_of_favorites=list_of_favorites)

@app.context_processor
def utility_processor():
    def tmdb_image_url(path):
        return tmdb_client.get_poster_url(path)
    return {"tmdb_image_url": tmdb_image_url}

@app.route('/about')
def about():

    return render_template("about.html")

@app.route('/contact')
def contact():

    return render_template("contact.html")

@app.route("/delete/<favorite_movie>", methods=["GET", "POST"])
def delete(favorite_movie):
    

    
    favorite_list = show_favorite()

    if favorite_movie in favorite_list:
            delete_from_favorite(favorite_movie)
            flash("Successfully deleted!", "alert-success")
            return redirect(request.referrer)



if __name__ == '__main__':
    app.run(debug=True)
