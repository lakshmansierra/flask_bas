import uuid
from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

from db import stores, users

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)

# ---------------- AUTHENTICATION ----------------
@app.post("/login")
def login():
    json_body = request.get_json()
    username = json_body["username"]
    password = json_body["password"]

    user = users[json_body["username"]]
    if not user or user["password"] != password:
        return {"msg": "Invalid username or password"}

    access_token = create_access_token(identity=username)
    return {"access token" : access_token}

# ---------------- USER ROUTES ----------------
@app.get("/user_list")
def user_list():
    return users

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