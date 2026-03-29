from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
load_dotenv()

from app import create_app

app=create_app()

jwt = JWTManager(app)

@jwt.unauthorized_loader
def missing_token_callback(reason):
    return {"message" : "Token missing" } , 401

@jwt.invalid_token_loader
def invalid_token_callback(reason):
    return {"message" : "Invalid Token" } , 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header , jwt_payload):
    return {"message" : "Token expired"} , 401

CORS(app, origins=["https://task-manager-api-rest-server.vercel.app"])






if __name__ == "__main__":
    app.run(debug=True)
