from tests.factories import UserFactory
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
