import uuid
from flask import Flask, request
from db import stores

app = Flask(__name__)

@app.get("/all_stores")
def all_stores():
    return stores

@app.post("/add_store")
def add_store():
    json_body = request.get_json()
    store_id = uuid.uuid4().hex
    stores[store_id] = {**json_body, "id":store_id}
    return stores[store_id]

@app.get("/specific_store/<id>")
def specific_store(id):
    return stores[id]

@app.put("/update_store/<id>")
def update_store(id):
    json_body = request.get_json()
    stores[id]["name"] = json_body["name"]
    return stores[id]

@app.delete("/delete_store/<id>")
def delete_store(id):
    stores.pop(id)
    return {"msg":"Store Deleted"}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')