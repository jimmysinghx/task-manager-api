from app.extensions import db 
from datetime import datetime , timezone

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer , primary_key= True)
    title = db.Column(db.String(255) , nullable=False)
    description = db.Column(db.String(255) )
    completed = db.Column(db.Boolean , default = False)
    created_at = db.Column(db.DateTime , default=lambda: datetime.now(timezone.utc) )
    user_id = db.Column(db.Integer , db.ForeignKey('users.id'))