from flask import Blueprint

app = Blueprint('swiper', __name__)

from .utils import utils_context, utils_dig
