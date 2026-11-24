from flask import Flask, jsonify, request

app = Flask(__name__)

employees = [
    {"id": 1, "name": "Asha", "role": "Engineer"},
    {"id": 2, "name": "Ravi", "role": "Designer"},
]


@app.route("/")
def index():
    return jsonify(message="Welcome to WorkforceHub", version="1.0.0")


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


@app.route("/api/employees", methods=["GET"])
def list_employees():
    return jsonify(employees)


@app.route("/api/employees", methods=["POST"])
def add_employee():
    data = request.get_json(silent=True) or {}
    if not data.get("name") or not data.get("role"):
        return jsonify(error="name and role are required"), 400
    new = {
        "id": max((e["id"] for e in employees), default=0) + 1,
        "name": data["name"],
        "role": data["role"],
    }
    employees.append(new)
    return jsonify(new), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)