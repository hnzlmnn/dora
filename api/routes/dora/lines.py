from datetime import datetime

from flask import jsonify, request
from peewee import DoesNotExist

from . import app
from db import Entry, Line


@app.route("/lines/<context>", methods=["GET"])
def lines_list(context: str):
    line = request.args.get("line", type=int)
    if not context:
        return jsonify(dict(
            ok=False,
            error="Invalid context"
        ))
    if line:
        entries = list(map(lambda e: e.to_json(), Line.select().where(Line.context == context, Line.line == line)))
    else:
        entries = list(map(lambda e: e.to_json(), Line.select().where(Line.context == context)))
    return jsonify(dict(
        ok=True,
        data=entries
    ))


@app.route("/lines", methods=["POST"])
def lines_select():
    data = request.get_json(True, True)
    context = data.get("context", None)
    line = data.get("line", None)
    id = data.get("id", None)
    if not context:
        return jsonify(dict(
            ok=False,
            error="Invalid context"
        ))
    if not line or type(line) != int:
        return jsonify(dict(
            ok=False,
            error="Invalid line"
        ))
    if not id or type(id) != int:
        return jsonify(dict(
            ok=False,
            error="Invalid id"
        ))
    try:
        entry = Entry.get_by_id(id)
    except DoesNotExist:
        return jsonify(dict(
            ok=False,
            error="Invalid id"
        ))
    if not entry.line == line:
        return jsonify(dict(
            od=False,
            error="Invalid line"
        ))
    Line.insert(
        context=context,
        line=line,
        entry=entry.id,
        selected_at=datetime.now()
    ).on_conflict_replace().execute()
    return jsonify(dict(
        ok=True
    ))
