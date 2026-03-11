import factory
from app.models.user import User 
from faker import Faker

fake = Faker()

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User 
        sqlalchemy_session = None
    
    username = factory.LazyFunction(lambda  : fake.user_name())
    email  = factory.LazyFunction(lambda : fake.email())
    password_hash = factory.LazyFunction(lambda : fake.sha256())