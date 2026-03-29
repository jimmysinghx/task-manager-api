from flask import Blueprint , request , jsonify 
from app.extensions import db, migrate , jwt, bcrypt
from flask_jwt_extended import create_access_token , jwt_required , get_jwt_identity
from app.models.user import User
from sqlalchemy.exc import IntegrityError

auth  = Blueprint("auth" , __name__)

@auth.route("/register" , methods=["POST"])
def register():

    """
    Register a new user
    ---
    tags:
      - Auth
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            email:
              type: string
              description: User email
            username:
              type: string
              description: User username
            password:
              type: string
              description: User password
    responses:
      201:
        description: User has been created
      400:
        description: Field can not be blank
      409:
        description: Username or email already exists
    """
    
    data = request.get_json()
    if not data :
        return jsonify({"message" : "Field can not be blank"}) , 400
    email = data.get("email")
    username = data.get("username")
    password= data.get("password")

    if not email or not email.strip():
        return jsonify({"message" : "email can not be blank"}) , 400
    elif not username or not username.strip():
        return jsonify({"message" : "username can not be blank" }) , 400
    elif not password or not password.strip():
        return jsonify({"message" : "passwrod can not be blank"}) , 400
    
    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    
    existing_user_username = User.query.filter_by(username = username).first()
    existing_user_email = User.query.filter_by(email = email).first()
    if existing_user_username:
        return jsonify({"message" : "username already taken"}), 409
    elif existing_user_email:
        return jsonify({"message" : "email id already exist"}) , 409
    try:
        user = User(username = username , password_hash = password_hash , email = email)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message" : "User has been created"}) , 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message" : "User with given credentials already exist"}) , 409

@auth.route("/login" , methods=["POST"])
def login():

    """
    Login and get JWT token
    ---
    tags:
      - Auth
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            username:
              type: string
              description: User username
            password:
              type: string
              description: User password
    responses:
      200:
        description: Returns JWT token
      400:
        description: Field can not be blank
      401:
        description: Credentials not correct
    """

    data = request.get_json()
    if not data:
        return jsonify({"message" : "Field can not be empty"}) , 400
    
    username = data.get("username")
    password =  data.get("password")

    if not username or not username.strip():
        return jsonify({"message" : "username can not be blank"}) , 400
    elif not password or not password.strip():
        return jsonify({"message" : "password can not be blank"}) , 400
    
    user = User.query.filter_by(username=username).first()


    if not user or not bcrypt.check_password_hash(user.password_hash , password):
        return jsonify({"message" : "Credentials not correct"}) , 401
    access_token = create_access_token(identity=str(user.id))
    return jsonify({"user_logged_in_as" : user.username , "mail_id" : user.email , "token" : access_token}) , 200

@auth.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    """
    Get current logged in user details
    ---
    tags:
      - Auth
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
        description: Bearer <your_jwt_token>
    responses:
      200:
        description: Returns username and email
      401:
        description: Unauthorized
      404:
        description: User not found
    """
    current_user_id= get_jwt_identity()
    user = User.query.filter_by(id = current_user_id ).first()
    if not user:
        return jsonify({"message" : "User not found"}) , 404
    return jsonify({"username" : user.username, "email" : user.email}) , 200
