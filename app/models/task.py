from app.extensions import db 
from datetime import datetime

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer , primary_key= True)
    title = db.Column(db.String(255) , nullable=False)
    operation = db.Column(db.String(255) )
    completed = db.Column(db.Boolean , default = False)
    created_at = db.Column(db.DateTime )