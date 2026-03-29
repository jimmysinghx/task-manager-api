from flask import Blueprint , request , jsonify
from flask_jwt_extended import get_jwt_identity , jwt_required
from app.models.task import Task
from app.extensions import db

tasks=Blueprint("tasks", __name__)

@tasks.route("/tasks", methods=['POST'])
@jwt_required()
def create_task():

    """
    Create a new task
    ---
    tags:
      - Tasks
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
        description: Bearer <your_jwt_token>
      - name: body
        in: body
        required: true
        schema:
          properties:
            title:
              type: string
              description: Title of the task
            description:
              type: string
              description: Description of the task (optional)
    responses:
      201:
        description: Task created successfully
      400:
        description: Title is required
      401:
        description: Unauthorized
      415:
        description: Content type must be application/json
    """
   
    if not request.is_json:
        return jsonify({"message" : "Content type must be aplication/json"}) , 415
    data = request.get_json()
    title =data.get("title")
    description = data.get("description")
    if not title or not title.strip():
        return jsonify({"message" : "Title is required"}) , 400
    current_user_id  = int(get_jwt_identity())
    task = Task(title = title , description = description , user_id=current_user_id )
    db.session.add(task)
    db.session.commit()
    return jsonify({"message" : "Task has been created successfully", "task_id" : task.id}),201

@tasks.route("/tasks" , methods=['GET'])
@jwt_required()
def viewTask():
    """
    Get all tasks for the logged in user
    ---
    tags:
      - Tasks
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
        description: Bearer <your_jwt_token>
      - name: page
        in: query
        type: integer
        description: Page number (default 1)
      - name: sort
        in: query
        type: string
        description: Sort by created_at - asc or desc (default desc)
      - name: completed
        in: query
        type: boolean
        description: Filter by completed status
    responses:
      200:
        description: List of tasks
      401:
        description: Unauthorized
    """
    current_user_id= int(get_jwt_identity())
    page = request.args.get("page" , 1 , type=int)
    sort = request.args.get("sort" , "desc")
    completed = request.args.get("completed")
  
    tasks = Task.query.filter_by(user_id = current_user_id)
    
    if completed is not None:
        completed = completed.lower()=="true"
        tasks = tasks.filter_by(completed=completed)
    if sort=="asc":
        tasks = tasks.order_by(Task.created_at.asc())
    if sort=="desc":
        tasks = tasks.order_by(Task.created_at.desc())
    if page:
        tasks= tasks.paginate(page=page , per_page=5 , error_out =False)
    if not tasks.items:
        return jsonify({"tasks" : [] , "total" : 0}) , 200
    
    task_list=[]
    for t in tasks.items:
        task_list.append({ "id" : t.id , "title": t.title , "description" :t.description , "completed" : t.completed, "created_at" : t.created_at.isoformat() })
    return jsonify({"tasks" : task_list , "total" : tasks.total , "pages" : tasks.pages , "current_page" : tasks.page}) , 200
    

@tasks.route("/tasks/<int:task_id>" , methods=['GET'])
@jwt_required()
def taskById(task_id):

    """
    Get a single task by ID
    ---
    tags:
      - Tasks
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
        description: Bearer <your_jwt_token>
      - name: task_id
        in: path
        required: true
        type: integer
        description: ID of the task
    responses:
      200:
        description: Task details
      401:
        description: Unauthorized
      404:
        description: Task not found
    """

    current_user_id = int(get_jwt_identity())
    task = Task.query.filter_by(user_id = current_user_id , id= int(task_id)).first()
    if task is None:
        return jsonify({"message" : "Task not found"}) , 404
    return jsonify({"id" : task.id , "title" : task.title , "description" : task.description , "completed" : task.completed , "created_at" : task.created_at.isoformat() }) , 200

@tasks.route("/tasks/<int:task_id>" , methods=['PATCH'] )
@jwt_required()
def update_task(task_id):

    """
    Update a task
    ---
    tags:
      - Tasks
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
        description: Bearer <your_jwt_token>
      - name: task_id
        in: path
        required: true
        type: integer
        description: ID of the task
      - name: body
        in: body
        required: true
        schema:
          properties:
            title:
              type: string
              description: Updated title (optional)
            description:
              type: string
              description: Updated description (optional)
            completed:
              type: boolean
              description: Updated completed status (optional)
    responses:
      200:
        description: Task has been updated
      400:
        description: Invalid data
      401:
        description: Unauthorized
      404:
        description: Task does not exist
      415:
        description: Content type must be application/json
    """

    if not request.is_json:
        return jsonify({"message" : "Content type must be aplication/json"}) , 415
    
    data=request.get_json() 

    if not data:
        return jsonify({"message" : "Data can not be blank"}) , 400

    current_user_id  = int(get_jwt_identity())
    task=Task.query.filter_by(id=task_id , user_id = current_user_id).first()

    if task is None:
        return jsonify({"message": "Task does not exist."}) , 404
    
    if "completed" in data :
        if not isinstance(data["completed"] , bool):
            return jsonify({"message" : "Boolean only acceptalbe on completed field"}) , 400 
        task.completed = data["completed"] 
    
    if "description" in data:
        task.description = data["description"]
        
    if "title" in data :
        if not data["title"] or not data["title"].strip():
            return jsonify({"message"  : "Title can not be blank"}) , 400
        task.title = data["title"]                                                                                                                                                                                                                                                                                                                                                          
    
    db.session.commit()
    return jsonify({"message" : "Task has been updated"}) , 200

@tasks.route("/tasks/<int:task_id>" , methods=["DELETE"])
@jwt_required()
def delete_task(task_id):

    """
    Delete a task
    ---
    tags:
      - Tasks
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
        description: Bearer <your_jwt_token>
      - name: task_id
        in: path
        required: true
        type: integer
        description: ID of the task
    responses:
      204:
        description: Task deleted successfully
      401:
        description: Unauthorized
      404:
        description: Task does not exist
    """

    current_user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id , user_id = current_user_id).first()
    if task is None:
        return jsonify({"message" : "Task does not exist"}) , 404
    db.session.delete(task)
    db.session.commit()
    return "",204




