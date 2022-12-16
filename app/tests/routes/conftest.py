import pytest
from run import create_app
import database
from config import TestConfig


@pytest.fixture(scope='session')
def test_client():
    pytest.sample_users = [
        {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@gmail.com',
            'birth_date': '2010-12-15 00:00:00'
        },
        {
            'first_name': 'Mike',
            'last_name': 'Baker',
            'email': 'mike.james@gmail.com',
            'birth_date': '2000-08-09 00:00:00'
        }
    ]

    flask_app = create_app(TestConfig)

    with flask_app.test_client() as client:
        with flask_app.app_context():
            database.remove_all_data()
            yield client


@pytest.fixture(scope='function', autouse=True)
def run_after_tests():
    yield
    database.remove_all_data()
