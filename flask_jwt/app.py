import uuid
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, 
)
from db import stores

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # change in production
jwt = JWTManager(app)

# Fake user database
users = {
    "admin": {"username": "admin", "password": "secret"}
}

# ---------------- AUTHENTICATION ----------------
@app.post("/login")
def login():
    json_body = request.get_json()
    username = json_body.get("username")
    password = json_body.get("password")

    user = users.get(username, None)
    if not user or user["password"] != password:
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# ---------------- STORE ROUTES ----------------
@app.get("/all_stores")
@jwt_required()
def all_stores():
    return stores

@app.post("/add_store")
@jwt_required()
def add_store():
    json_body = request.get_json()
    store_id = uuid.uuid4().hex
    stores[store_id] = {**json_body, "id":store_id}
    return stores[store_id]

@app.get("/specific_store/<id>")
@jwt_required()
def specific_store(id):
    return stores[id]

@app.put("/update_store/<id>")
@jwt_required()
def update_store(id):
    json_body = request.get_json()
    stores[id]["name"] = json_body["name"]
    return stores[id]

@app.delete("/delete_store/<id>")
@jwt_required()
def delete_store(id):
    stores.pop(id)
    return {"msg":"Store Deleted"}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')