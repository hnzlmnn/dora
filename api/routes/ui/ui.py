import re

from flask import jsonify, request

from . import app

API_ROUTE = re.compile(r"^/(dora|swiper)")


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.errorhandler(404)
def page_not_found(e):
    if API_ROUTE.match(request.path):
        return jsonify(dict(ok=False, error=str(e))), 404
    return app.send_static_file("index.html")
