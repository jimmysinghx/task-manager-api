from tests.factories import UserFactory
from app.extensions import db
def test_register_empty_request(client):
    response = client.post("/register" , json={})
    assert response.status_code == 400

def test_register_no_email(client, user_factory):
    user = user_factory.build()
    response = client.post("/register", json={
        "username":user.username ,
        "email":" ",
        "password":"Password123"
    } )

    assert response.status_code == 400
    assert response.json == {"message" : "email can not be blank"}

def test_register_no_username(client , user_factory):
    user = user_factory.build()
    response = client.post("/register" , json={
        "username":"",
        "email": user.email,
        "password":"Password123"
    })
    
    assert response.status_code == 400 
    assert response.json == {"message" : "username can not be blank"}

def test_register_no_password(client , user_factory):
    user = user_factory.build()
    response = client.post("/register" , json={
        "username":user.username, 
        "email":user.email,
        "password":""
    })
    
    assert response.status_code == 400
    assert response.json == {"message" : "passwrod can not be blank"}

def test_register_duplicate_username(client , user_factory):
    user1=user_factory.create()
    user2=user_factory.build()
    response = client.post("/register" , json={
        "username" :  user1.username ,
        "email" : user2.email ,
        "password" : "Passwrord123"
    })

    assert response.status_code == 409
    assert response.json == {"message" : "username already taken"}

def test_register_duplicate_email(client, user_factory):
    user1 = user_factory.create()
    user2  =user_factory.build()
    response = client.post("/register", json={
        "username":user2.username ,
        "email":user1.email ,
        "password": "Password123"
    })

    assert response.status_code == 409 
    assert response.json == {"message" : "email id already exist"}

def test_register_user(client , user_factory):
    user = user_factory.build()
    response = client.post("/register" , json={
        "username"  : user.username,
        "email" : user.email,
        "password" : "Password123"
    })
    
    assert response.status_code == 201
    assert response.json == {"message" : "User has been created"}

def test_login_empty_request(client):
    response = client.post("/login" , json = {})
    assert response.status_code == 400
    assert response.json == {"message" : "Field can not be empty"}

def test_login_missing_username(client , user_factory):
    user = user_factory.build()
    response = client.post("/login" , json={
            "username" : "",
            "password" : "password123"
    })

    assert response.status_code == 400
    assert response.json == {"message" : "username can not be blank"}

def test_login_missing_password(client , user_factory):
    user = user_factory.build()
    response = client.post("/login", json = {
        "username" : user.username ,
        "password" : ""
    })

    assert response.status_code == 400
    assert response.json == {"message" : "password can not be blank"}

def test_login_fails_when_user_not_found(client , user_factory):
    user  = user_factory.create()
    user2 = user_factory.build()
    response = client.post("/login" , json = {
        "username" : user2.username ,
        "password" : "password123" 
    })

    assert response.status_code == 401
    assert response.json == {"message" : "Credentials not correct"}

def test_login_fails_when_password_is_incorrect(client , user_factory):
    user = user_factory.build()
    response = client.post("/login" , json ={
        "username" : user.username ,
        "password" : "password1"
    })

    assert response.status_code == 401
    assert response.json == {"message" : "Credentials not correct"}

def test_login_successful(client , user_factory):
    user = user_factory.create()
    response = client.post("/login" , json = {
        "username" : user.username ,
        "password" : "password123"
    })

    assert response.status_code == 200
    assert response.json == {"user_logged_in_as" : response.json["user_logged_in_as"] , "mail_id" : response.json["mail_id"] , "token" : response.json["token"]}

def test_protected_user_not_found(client , user_factory):
    user1 = user_factory.create()
    response1 = client.post("/login" , json={
        "username" : user1.username ,
        "password" : "password123"
    })
    access_token  = response1.json["token"]
    assert response1.status_code == 200
    db.session.delete(user1)
    db.session.commit()
    response2 = client.get("/protected" , headers = {"Authorization" : f"Bearer {access_token}"})
    
    assert response2.status_code == 404
    assert response2.json == {"message" : "User not found"}

def test_protected_successful(client , user_factory):
    user = user_factory.create()
    response1  = client.post("/login" , json ={
        "username" : user.username ,
        "password" : "password123"
    })
    access_token = response1.json["token"]
    assert response1.status_code  == 200

    response2 = client.get("/protected" , headers = {"Authorization" : f"Bearer {access_token}"})

    assert response2.status_code == 200 
    assert response2.json == {"username" : response2.json["username"], "email" : response2.json["email"]}