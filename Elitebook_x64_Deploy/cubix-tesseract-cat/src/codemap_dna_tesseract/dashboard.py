# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
# This software is proprietary and subject to the terms of a specific License Agreement.

"""Simple Flask dashboard for viewing function library, data bindings, and manual control."""
from flask import Flask, jsonify, request, render_template_string

try:
    from .runtime.registry import build_registry
    from .data_binding import load_bindings, bind_data, unbind_data
    from .virtual_data_store import get_data
    from .runtime.host import stats
except Exception:
    from codemap_dna_tesseract.runtime.registry import build_registry
    from codemap_dna_tesseract.data_binding import load_bindings, bind_data, unbind_data
    from codemap_dna_tesseract.virtual_data_store import get_data
    from codemap_dna_tesseract.runtime.host import stats

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<title>CubixOS Dashboard</title>
<h1>CubixOS Dashboard</h1>
<p><a href="/functions">Functions</a> | <a href="/bindings">Data Bindings</a> | <a href="/stats">Runtime Stats</a></p>
<hr>
{% block body %}{% endblock %}
"""


@app.route("/")
def index():
    return render_template_string(TEMPLATE + "<p>Welcome to CubixOS dashboard.</p>")


@app.route("/functions")
def functions():
    reg = build_registry()
    return jsonify(reg)


@app.route("/bindings")
def bindings():
    b = load_bindings()
    return jsonify(b)


@app.route("/bind", methods=["POST"])
def bind():
    data = request.get_json() or {}
    did = data.get("data_id")
    addr = data.get("address")
    desc = data.get("description", "")
    if not did or not addr:
        return jsonify({"error": "data_id and address required"}), 400
    bind_data(did, addr, desc)
    return jsonify({"status": "ok"})


@app.route("/unbind", methods=["POST"])
def unbind():
    data = request.get_json() or {}
    did = data.get("data_id")
    if not did:
        return jsonify({"error": "data_id required"}), 400
    unbind_data(did)
    return jsonify({"status": "ok"})


@app.route("/data/<data_id>")
def data_view(data_id):
    try:
        res = get_data(data_id)
        return jsonify({"data": res})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/stats")
def runtime_stats():
    return jsonify(stats())


if __name__ == "__main__":
    app.run(port=5000)
