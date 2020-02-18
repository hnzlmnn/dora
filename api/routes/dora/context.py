from flask import jsonify, request
from peewee import JOIN, fn

from . import app
from db import Entry, Line


@app.route("/context", methods=["GET"])
def context_list():
    contexts = list(Entry.select(Entry.context, fn.Count(Entry.id).alias("entries"), fn.Count(fn.Distinct(Entry.line)).alias("lines")).group_by(Entry.context).dicts())
    print(contexts)
    return jsonify(dict(
        ok=True,
        data=contexts
    ))
