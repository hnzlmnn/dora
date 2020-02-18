from datetime import datetime

from flask import jsonify, request

from swiper import Swiper
from . import app


@app.route("/context", methods=["GET"])
def utils_context():
    return jsonify(dict(
        ok=True,
        data=Swiper.instance().generate_context()
    ))


@app.route("/dig", methods=["GET"])
def utils_dig():
    context = request.args.get("context", type=str)
    if not context:
        return jsonify(dict(
            ok=False,
            error="Invalid context"
        ))
    cmd = request.args.get("cmd", type=str)
    meta = request.args.get("meta", type=bool)
    return jsonify(dict(
        ok=True,
        data=Swiper.instance().generate_dig(context, payload=cmd, metadata=meta)
    ))
