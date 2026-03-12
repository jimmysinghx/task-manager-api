import factory
from app.models.user import User 
from faker import Faker
from app.extensions import bcrypt

fake = Faker()

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User 
        sqlalchemy_session = None
    
    username = factory.LazyFunction(lambda  : fake.user_name())
    email  = factory.LazyFunction(lambda : fake.email())
    password_hash = factory.LazyFunction(lambda : bcrypt.generate_password_hash("password123").decode("utf-8"))