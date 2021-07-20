from flask.helpers import url_for
from movieapp.settings import API_KEY, BASE_POPULAR_TV, BASE_URL, IMG_BASE_URL
from flask import Blueprint, render_template, redirect
from flask import request as req
import json
import urllib.request as request

from ..extensions import mongo

main = Blueprint('main', __name__)
tv_page = 1

@main.route('/')
def index():
    url = BASE_URL + API_KEY
    conn = request.urlopen(url)
    json_data = json.loads(conn.read())
    return render_template('index.html', data=json_data["results"])

@main.route('/movies')
def movies():
    return render_template('movie.html')

@main.route('/tv')
def tv():
    url = BASE_POPULAR_TV + API_KEY
    conn = request.urlopen(url)
    json_data = json.loads(conn.read())
    return render_template('tv.html', data=json_data["results"])

@main.route('/tvshows')
def tvshows():
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
    


