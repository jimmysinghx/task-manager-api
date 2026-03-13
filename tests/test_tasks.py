from app.models.task import Task
def test_tasks_unsupported_media_type(client , user_factory):
    user = user_factory.create()
    response1 = client.post("/login" , json={
        "username" : user.username ,
        "password" : "password123"
    })

   
    assert response1.status_code == 200
    access_token = response1.json["token"]

    response2 = client.post("/tasks" , headers = {"Authorization" : f"Bearer {access_token}"} , data="")
    assert response2.status_code == 415
    assert response2.json == {"message" : "Content type must be aplication/json"}

def test_tasks_empty_title(client , user_factory , task_factory):
    user = user_factory.create()
    response1 = client.post("/login" , json={
        "username" : user.username ,
        "password" : "password123"
    })

    assert response1.status_code == 200
    access_token = response1.json["token"]
    task = task_factory.build()
    response2 = client.post("/tasks" , headers = {"Authorization" : f"Bearer {access_token}"} , json={
        "title" : "" ,
        "description" : task.description
    })
    assert response2.status_code == 400 
    assert response2.json == {"message" : "Title is required"}


def test_task_create_successfully(client , user_factory , task_factory):
    user = user_factory.create()
    response1 = client.post("/login" , json={
        "username" : user.username ,
        "password" : "password123"
    })

    assert response1.status_code == 200
    access_token = response1.json["token"]

    task = task_factory.build()
    response2 = client.post("/tasks" , headers ={"Authorization" :f"Bearer {access_token}"} ,json={
        "title" : task.title,
        "description" : task.description
    })
    assert response2.status_code == 201 
    assert response2.json == {"message" : "Task has been created successfully", "task_id" : response2.json["task_id"]}

def test_task_does_not_exist(client , user_factory , task_factory):
    user = user_factory.create()
    response1 = client.post("/login" , json={
        "username" : user.username ,
        "password" : "password123"
    })

    assert response1.status_code == 200
    access_token = response1.json["token"]
    
    response2 = client.get("/tasks" , headers = {"Authorization" : f"Bearer {access_token}"} )
    assert response2.status_code == 404
    assert response2.json == {"message" : "Task does not exist"}

def test_task_view_successfully(client , user_factory , task_factory) :
    user = user_factory.create() 
    task1 = task_factory.create(user=user)
    task2= task_factory.create(user=user)
    response1 = client.post("/login" , json={
        "username" : user.username ,
        "password" : "password123"
    })
    assert response1.status_code == 200
    access_token  = response1.json["token"]
    

    response2 = client.get("/tasks" , headers ={"Authorization" : f"Bearer {access_token}"})
    assert response2.status_code == 200
    assert response2.json == {"tasks" : response2.json["tasks"] , "total" : response2.json["total"] , "pages" : response2.json["pages"] , "current_page" : response2.json["current_page"]}


def test_task_by_id_not_found(client , user_factory , task_factory) :
    user = user_factory.create() 
    task1 = task_factory.create(user = user)
    task2 = task_factory.create(user = user)
    task3 = task_factory.create()
    response1 = client.post("/login" , json ={
        "username" : user.username ,
        "password" : "password123"
    })
    assert response1.status_code == 200
    access_token = response1.json["token"] 

    response2 = client.get(f"/tasks/{task3.id}" , headers = {"Authorization" : f"Bearer {access_token}"}) 
    assert response2.status_code == 404
    assert response2.json == {"message" : "Task not found"}

def test_task_by_id_successful(client , user_factory , task_factory):
    user = user_factory.create()
    task = task_factory.create(user = user)
    response1 = client.post("/login" , json = {
        "username" : user.username ,
        "password" : "password123"
    })
    assert response1.status_code == 200
    access_token = response1.json["token"]

    response2 = client.get(f"/tasks/{task.id}" , headers = {"Authorization": f"Bearer {access_token}"})
    assert response2.status_code == 200
    assert response2.json == ({"id" : response2.json["id"] , "title" : response2.json["title"] , "description" : response2.json["description"] , "completed" : response2.json["completed"] , "created_at" : response2.json["created_at"] })

def test_update_task_unsupported_media_type(client , user_factory , task_factory):
    task = task_factory.create()
    response1 = client.post("/login" , json= {
        "username" : task.user.username ,
        "password" : "password123"
    })
    assert response1.status_code == 200
    access_token = response1.json["token"]
    response2 = client.patch(f"/tasks/{task.id}" , headers = {"Authorization" : f"Bearer {access_token}"} , data={})
    assert response2.status_code == 415
    assert response2.json == {"message" : "Content type must be aplication/json"}

def test_update_task_empty_request(client , user_factory , task_factory) :
    task = task_factory.create()
    response1 = client.post("/login" , json ={
        "username" : task.user.username ,
        "password" : "password123"
    })
    assert response1.status_code == 200
    access_token = response1.json["token"] 
    response2  = client.patch(f"/tasks/{task.id}"  , headers = {"Authorization" : f"Bearer {access_token}"} , json ={})
    assert response2.status_code == 400
    assert response2.json == {"message" : "Data can not be blank"}

def test_update_task_not_found(client , user_factory , task_factory):
    user = user_factory.create()    
    task1 =  task_factory.create(user = user)
    task2 = task_factory.create()
    response1 = client.post("/login" , json ={
        "username" : user.username ,
        "password" : "password123"
    })
    assert response1.status_code == 200
    access_token = response1.json["token"]
    response2 =  client.patch(f"/tasks/{task2.id}" , headers = {"Authorization" : f"Bearer {access_token}"}, json ={
        "completed" : not(task2.completed)
    })
    assert response2.status_code == 404
    assert response2.json == {"message": "Task does not exist."}

def test_update_task_completed_data_type_check(client  , task_factory):
    task = task_factory.create()
    response1 = client.post("/login" , json ={
        "username" : task.user.username ,
        "password" : "password123"
    })
    assert response1.status_code == 200
    access_token = response1.json["token"] 
    response2 =  client.patch(f"/tasks/{task.id}" , headers = {"Authorization" : f"Bearer {access_token}"}, json ={
        "completed" : "yes"
    })
    assert response2.status_code == 400
    assert response2.json == {"message" : "Boolean only acceptalbe on completed field"}

def test_update_task_title_empty(client , task_factory):
    task = task_factory.create()
    response1 = client.post("/login" , json ={
        "username" : task.user.username ,
        "password" : "password123"
    })
    assert response1.status_code == 200
    access_token = response1.json["token"] 
    response2 =  client.patch(f"/tasks/{task.id}" , headers = {"Authorization" : f"Bearer {access_token}"}, json ={
        "title" : ""
    })
    assert response2.status_code == 400
    assert response2.json == {"message"  : "Title can not be blank"}

def test_task_updated_successfully(client ,  task_factory):
    task = task_factory.create()
    task2 = task_factory.build()
    response1 = client.post("/login" , json ={
        "username" : task.user.username ,
        "password" : "password123"
    })
    assert response1.status_code == 200
    access_token = response1.json["token"] 
    response2 =  client.patch(f"/tasks/{task.id}" , headers = {"Authorization" : f"Bearer {access_token}"}, json ={
        "title" : task2.title ,
        "description" : task2.description ,
        "completed" : task2.completed
    })

    assert response2.status_code == 200
    assert response2.json == {"message" : "Task has been updated"} 


def test_delete_task_not_found_returns_404(client ,  task_factory):
    task1 = task_factory.create()
    task2 = task_factory.create()
    response1 = client.post("/login" , json ={
        "username" : task1.user.username ,
        "password" : "password123"
    })
    assert response1.status_code == 200
    access_token = response1.json["token"] 
    response2 = client.delete(f"/tasks/{task2.id}" , headers = {"Authorization" : f"Bearer {access_token}"})
    assert response2.status_code == 404
    assert response2.json == {"message" : "Task does not exist"}

def test_delete_task_successful(client , task_factory):
    task = task_factory.create()
    response1 = client.post("/login" , json ={
        "username" : task.user.username ,
        "password" : "password123"
    })
    assert response1.status_code == 200
    access_token = response1.json["token"] 
    assert Task.query.get(task.id) is not None 
    response2 = client.delete(f"/tasks/{task.id}" , headers = {"Authorization" : f"Bearer {access_token}"})
    assert response2.status_code == 204
    assert response2.data == b""
    assert Task.query.get(task.id) is None
    