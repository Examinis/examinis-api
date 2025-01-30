import factory

from examinis.models.difficulty import Difficulty
from examinis.models.role import Role
from examinis.models.subject import Subject
from examinis.models.user import User
from examinis.models.user_status import UserStatus


class RoleFactory(factory.Factory):
    class Meta:
        model = Role

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Sequence(lambda n: f'role{n}')


class UserStatusFactory(factory.Factory):
    class Meta:
        model = UserStatus

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker('word')


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n + 1)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(
        lambda obj: f'{obj.first_name.lower()}@test.com'
    )
    password = factory.Faker('password')

    status = factory.SubFactory(UserStatusFactory)
    role = factory.SubFactory(RoleFactory)

    status_id = factory.SelfAttribute('status.id')
    role_id = factory.SelfAttribute('role.id')


class SubjectFactory(factory.Factory):
    class Meta:
        model = Subject

    id = factory.Sequence(lambda n: n + 1)
    name = 'Geography'


class DifficultyFactory(factory.Factory):
    class Meta:
        model = Difficulty

    id = factory.Sequence(lambda n: n + 1)
    name = 'Easy'
