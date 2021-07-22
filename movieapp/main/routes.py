from flask.helpers import url_for
from movieapp.settings import API_KEY, BASE_POPULAR_TV, BASE_TV_URL, BASE_URL, IMG_BASE_URL, SEARCH_URL
from flask import Blueprint, render_template, redirect
from flask import request as req
import json
import urllib.request as request

from ..extensions import mongo

main = Blueprint('main', __name__)
tv_page = 1
skip_limit=0
page_limit=20

@main.route('/', methods=['GET','POST'])
def index():
    if (req.method == "POST"):
        name = req.form.get('search')
        return redirect(url_for('main.search', file_name = name))
    img_data = mongo.db.images.find()
    img_data = list(img_data)

    movie_sorted = list(mongo.db.movies.find({'poster': {"$exists": True}}).sort("released", -1).limit(10))

    url = BASE_URL + API_KEY
    conn = request.urlopen(url)
    json_data = json.loads(conn.read())
    total_data = []
    total_data.append(img_data)
    total_data.append(json_data["results"])
    total_data.append(movie_sorted)
    return render_template('index.html', data=total_data)

@main.route('/search/<file_name>', methods=['GET','POST'])
def search(file_name):
    if (req.method == "POST"):
        name = req.form.get('search')
        return redirect(url_for('main.search', file_name = name))
    movie_sorted=list(mongo.db.movies.find({"title": {'$regex': file_name,'$options': "$i"}}).sort("released", -1).limit(8))
    url = SEARCH_URL + API_KEY + '&language=en-US&page=1&query='  + file_name + '&include_adult=false'
    conn = request.urlopen(url)
    json_data = json.loads(conn.read())
    total_data=[]
    total_data.append(movie_sorted)
    total_data.append(json_data['results'])
    return render_template('search.html', movie_sorted=total_data)


@main.route('/movies', methods=['GET','POST'])
def movies():
    if (req.method == "POST"):
        name = req.form.get('search')
        return redirect(url_for('main.search', file_name = name))
    movie_sorted = list(mongo.db.movies.find({'poster': {"$exists": True}}).sort("released", -1).limit(20))
    return render_template('movie.html', movie_sorted=movie_sorted)

@main.route('/movies/nextpage', methods=['GET','POST'])
def route1():
    if (req.method == "POST"):
        name = req.form.get('search')
        return redirect(url_for('main.search', file_name = name))
    global skip_limit
    global page_limit
    skip_limit = skip_limit + page_limit

    movie_sorted = list(mongo.db.movies.find({'poster': {"$exists": True}}).sort("released", -1).skip(skip_limit).limit(page_limit))
    return render_template('movie.html', movie_sorted=movie_sorted)

@main.route('/movies/previouspage', methods=['GET','POST'])
def route2():
    if (req.method == "POST"):
        name = req.form.get('search')
        return redirect(url_for('main.search', file_name = name))
    global skip_limit
    global page_limit
    skip_limit = skip_limit - page_limit
    if(skip_limit<0):
        skip_limit=0
    movie_sorted = list(mongo.db.movies.find({'poster': {"$exists": True}}).sort("released", -1).skip(skip_limit).limit(page_limit))
    return render_template('movie.html', movie_sorted=movie_sorted)

@main.route('/movies/<int:imdb>')
#@app.route('/movies',methods=['GET','POST'])
def moviedetail(imdb):
    print(imdb)
    x=mongo.db.movies.find( {"imdb.id": imdb})
    return render_template('moviedetails.html',movie=x)

@main.route('/tv', methods=['GET','POST'])
def tv():
    if (req.method == "POST"):
        name = req.form.get('search')
        return redirect(url_for('main.search', file_name = name))
    
    url = BASE_POPULAR_TV + API_KEY
    conn = request.urlopen(url)
    json_data = json.loads(conn.read())
    return render_template('tv.html', data=json_data["results"])

@main.route('/tvshows', methods=['GET','POST'])
def tvshows():
    if (req.method == "POST"):
        name = req.form.get('search')
        return redirect(url_for('main.search', file_name = name))
    
    url = BASE_POPULAR_TV + API_KEY + '&page=' + str(tv_page)
    conn = request.urlopen(url)
    json_data = json.loads(conn.read())
    return render_template('tv.html', data=json_data["results"])


@main.route('/tv/nextpage')
def nextpage():
    global tv_page
    tv_page = tv_page + 1
    return redirect(url_for('main.tvshows'))

@main.route('/tv/prevpage')
def prevpage():
    global tv_page
    tv_page = tv_page - 1
    if (tv_page<1):
        tv_page = 1
    return redirect(url_for('main.tvshows'))

@main.route('/tvdetail/<int:tv_id>')
def tvdetail(tv_id):
    url = BASE_TV_URL + str(tv_id) + '?api_key=' + API_KEY
    conn = request.urlopen(url)
    json_data = json.loads(conn.read())
    return render_template('tvdetail.html',data = json_data)
    
# @main.route('/insert')
# def insertimg():
#     return render_template('test.html')

# @main.route('/create', methods = ['POST'])
# def create():
#     if 'img' in req.files:
#         prof_img = req.files['img']
#         name = req.form.get('name')
#         print(name)
#         mongo.save_file(prof_img.filename, prof_img)
#         print(prof_img.filename)
#         mongo.db.images.insert({'image_name':prof_img.filename})
#         return "doone"
        
#     return "prof"

@main.route('/getimage/<filename>')
def getimage(filename):
    return mongo.send_file(filename)


