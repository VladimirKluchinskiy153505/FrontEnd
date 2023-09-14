import pytest

# Create your tests here.
def test_example():
    assert 1+1==2

@pytest.fixture
def user(db):
    from django.contrib.auth.models import User
    user = User.objects.create(username='testuser')
    return user

def test_user_creation(user):
    assert user.username == 'testuser'
