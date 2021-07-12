from flask import Blueprint

from ..extensions import mongo

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return 'home'

