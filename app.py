from flask import Flask, request, render_template, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "dwc.json"

def load_entries():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_entry(entry):
    entries = load_entries()
    entries.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(entries, f, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    if request.remote_addr != "127.0.0.1":
        return jsonify({"status": "unauthorized"}), 403

    identifier = request.form.get("identifier")
    reason = request.form.get("reason")
    if identifier and reason:
        save_entry({"identifier": identifier, "reason": reason})
        return jsonify({"status": "success"})
    return jsonify({"status": "invalid"}), 400

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").strip().lower()
    entries = load_entries()
    for entry in entries:
        if query == entry["identifier"].lower():
            return jsonify({"status": "found", "entry": entry})
    return jsonify({"status": "not_found"})

if __name__ == "__main__":
    # Fix for Render deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
