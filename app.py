from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data (no database)
projects = [
    {"id": 1, "name": "Bridge Project", "budget": 500000},
    {"id": 2, "name": "Road Project", "budget": 200000},
]

@app.get("/")
def home():
    return "Construction Service Running 🚧"

@app.get("/health")
def health():
    return jsonify({"status": "UP"}), 200

@app.get("/projects")
def get_projects():
    return jsonify(projects), 200

@app.post("/projects")
def create_project():
    data = request.get_json(silent=True) or {}

    # basic validation
    if "name" not in data or "budget" not in data:
        return jsonify({"error": "name and budget are required"}), 400

    new_id = max([p["id"] for p in projects], default=0) + 1
    project = {"id": new_id, "name": data["name"], "budget": data["budget"]}
    projects.append(project)

    return jsonify(project), 201

@app.put("/projects/<int:pid>")
def update_project(pid):
    data = request.get_json(silent=True) or {}

    for p in projects:
        if p["id"] == pid:
            # allow partial updates
            if "name" in data:
                p["name"] = data["name"]
            if "budget" in data:
                p["budget"] = data["budget"]
            return jsonify(p), 200

    return jsonify({"error": "project not found"}), 404

@app.delete("/projects/<int:pid>")
def delete_project(pid):
    global projects
    before = len(projects)
    projects = [p for p in projects if p["id"] != pid]

    if len(projects) == before:
        return jsonify({"error": "project not found"}), 404

    return jsonify({"message": "deleted"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)