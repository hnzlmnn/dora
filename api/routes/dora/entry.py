from flask import jsonify, request
from peewee import JOIN, DoesNotExist

from . import app
from db import Entry, Line, Meta


@app.route("/entry/<context>", methods=["GET"])
def entry_list(context: str):
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


@app.route("/entry/<context>/summary", methods=["GET"])
def entry_detail(context: str):
    if not context:
        return jsonify(dict(
            ok=False,
            error="Invalid context"
        ))
    if Entry.select().where(Entry.context == context).count() == 0:
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
    # missing = set(map(lambda e: e[0], Entry
    #                    .select(Entry.line)
    #                    .join(Line, JOIN.LEFT_OUTER, on=((Line.line == Entry.line) & (Line.context == Entry.context)))
    #                    .where(Entry.context == context, Line.selected_at != None)
    #                    .distinct()
    #                    .tuples()))
    try:
        meta = Meta.get(Meta.context == context)
    except DoesNotExist:
        return jsonify(dict(
            ok=False,
            error="No metadata exist"
        ))
    return jsonify(dict(
        ok=True,
        data=dict(
            lines=lines,
            missing=meta.get_missing()
        )
    ))

@app.route("/entry/<context>/export", methods=["GET"])
def entry_export(context: str):
    if not context:
        return jsonify(dict(
            ok=False,
            error="Invalid context"
        ))
    lines = list(map(lambda l: l.entry.data.decode("ascii"), Line
                     .select(Line.entry)
                     .where(Line.context == context)
                     .prefetch(Entry)))
    return jsonify(dict(
        ok=True,
        data=lines
    ))
