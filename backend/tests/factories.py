import factory
from app.models.user import User 
from app.models.task import Task
from faker import Faker
from app.extensions import bcrypt
from datetime import datetime , timezone

fake = Faker()

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User 
        sqlalchemy_session = None
    
    username = factory.LazyFunction(lambda  : fake.user_name())
    email  = factory.LazyFunction(lambda : fake.email())
    password_hash = factory.LazyFunction(lambda : bcrypt.generate_password_hash("password123").decode("utf-8"))

class TaskFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta :
        model = Task
        sqlalchemy_session = None

    title = factory.LazyFunction(lambda : fake.sentence(nb_words=4))
    description = factory.LazyFunction(lambda : fake.sentence(nb_words=10))
    completed = factory.LazyFunction(lambda : fake.boolean())
    created_at = factory.LazyFunction(lambda : datetime.now(timezone.utc))
    user = factory.SubFactory(UserFactory)
    user_id = factory.LazyAttribute(lambda obj : obj.user.id)
