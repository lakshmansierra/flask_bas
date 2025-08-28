from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from db import users

app = Flask(__name__)
jwt = JWTManager(app)

app.config["JWT_SECRET_KEY"] = "my_secret_key"

@app.post("/login")
def login():
    json_body = request.get_json()
    username = json_body["username"]
    password = json_body["password"]

    user = users[username]

    if not user or user["password"] != password:
        return {"msg":"invalid username and password"} 
    
    access_token = create_access_token(identity=username)
    return {"access_token" : access_token}


if __name__ == "__main__":
    app.run(debug=True)