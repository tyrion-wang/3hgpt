from flask import Blueprint

bp = Blueprint('writer', __name__)

from app.writer import routes