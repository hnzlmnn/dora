from flask import Blueprint

app = Blueprint('dora', __name__)

from .entries import entries_list
from .lines import lines_list, lines_select
