from datetime import datetime

from flask import jsonify, request
from peewee import DoesNotExist, JOIN, fn

from . import app
from db import Entry, Line, Meta


@app.route("/line/<context>", methods=["GET"])
def line_list(context: str):
    line = request.args.get("line", type=int)
    if not context:
        return jsonify(dict(
            ok=False,
            error="Invalid context"
        ))
    if line:
        lines = list(map(lambda l: l.to_json(), Line.select().where(Line.context == context, Line.line == line)))
    else:
        lines = list(map(lambda l: l.to_json(), Line.select().where(Line.context == context)))
    return jsonify(dict(
        ok=True,
        data=lines
    ))


@app.route("/line", methods=["POST"])
def line_select():
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


@app.route("/line/auto", methods=["POST"])
def line_select_auto():
    data = request.get_json(True, True)
    context = data.get("context", None)
    if not context:
        return jsonify(dict(
            ok=False,
            error="Invalid context"
        ))
    # Select all missing lines
    try:
        meta = Meta.get(Meta.context == context)
    except DoesNotExist:
        return jsonify(dict(
            ok=False,
            error="No metadata exist"
        ))
    missing = meta.get_missing()
    remaining = missing[:]
    for line in missing:
        print("testing", line)
        # First check if all entries are the same
        lines = list(Entry.select(Entry.id, fn.Count(Entry.id), Entry.data).where(Entry.context == context, Entry.line == line).group_by(Entry.data).tuples())
        print(lines)
        if len(lines) == 0:
            # If none are found we don't know what to do
            continue
        if len(lines) == 1:
            # If all entries contain the same data, just choose at random
            print("using", lines[0][0])
            Line.insert(
                context=context,
                line=line,
                entry=lines[0][0],
                selected_at=datetime.now()
            ).on_conflict_replace().execute()
            remaining.remove(line)
        else:
            # If there are different data check if only one is decodable
            print("MULTIPLE VALUES")
            pass

    print(remaining)
    return jsonify(dict(
        ok=True,
        data=remaining
    ))
