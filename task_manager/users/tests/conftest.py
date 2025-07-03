import pytest
from django.core.management import call_command


@pytest.fixture
def load_users(db):
    call_command('loaddata', 'users')
