from flask import jsonify, request
from peewee import JOIN

from api.api import app
from db import Entry, Line


@app.route("/entries/<context>", methods=["GET"])
def entries_list(context: str):
    line = request.args.get("line", type=int)
    if not context:
        return jsonify(dict(
            ok=False,
            error="Invalid context"
        ))
    if line:
        entries = list(map(lambda e: e.to_json(), Entry.select().where(Entry.context == context, Entry.line == line)))
    else:
        entries = list(map(lambda e: e.to_json(), Entry.select().where(Entry.context == context)))
    if len(entries) == 0:
        return jsonify(dict(
            ok=False,
            error="Invalid context"
        ))
    return jsonify(dict(
        ok=True,
        data=entries
    ))


@app.route("/entries/<context>/summary", methods=["GET"])
def entries_detail(context: str):
    if not context:
        return jsonify(dict(
            ok=False,
            error="Invalid context"
        ))
    lines = {
        entry.line: entry.to_json() for entry in Line
        .select(Entry)
        .where(Entry.context == context)
        .join(Entry, JOIN.INNER)
        .objects(Entry)
    }
    missing = list(map(lambda e: e[0], Entry
                       .select(Entry.line)
                       .join(Line, JOIN.LEFT_OUTER, on=(Line.line == Entry.line))
                       .where(Entry.context == context, Line.selected_at == None)
                       .distinct()
                       .tuples()))
    return jsonify(dict(
        ok=True,
        data=dict(
            lines=lines,
            missing=missing
        )
    ))
