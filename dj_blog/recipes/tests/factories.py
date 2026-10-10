import factory
from factory.django import DjangoModelFactory
from faker import Faker

from accounts.models import CustomUser

fake = Faker()

class UserFactory(DjangoModelFactory):

    class Meta:
        model = CustomUser
    
    username = factory.Sequence(
        lambda n: f"user{n}"
    )

    email = factory.LazyFunction(fake.email)

    password = factory.PostGenerationMethodCall(
        "set_password",
        "testpass123"
    )