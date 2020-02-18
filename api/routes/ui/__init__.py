from flask import Blueprint

app = Blueprint('ui', __name__, static_folder="../../../ui/public/", static_url_path="")

from .ui import index
