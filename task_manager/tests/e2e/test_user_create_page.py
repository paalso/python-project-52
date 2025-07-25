import random
from urllib.parse import urljoin

import pytest


@pytest.mark.playwright
def test_register_and_check_user(page, base_url):
    page.goto(urljoin(base_url, "/users/create/"))

    username = f"e2etestuser_{random.randint(1, 100_000)}"
    page.fill('input[name="first_name"]', 'E2E')
    page.fill('input[name="last_name"]', 'User')
    page.fill('input[name="username"]', username)
    page.fill('input[name="password1"]', 'strongpass123')
    page.fill('input[name="password2"]', 'strongpass123')

    page.click('text="Зарегистрировать"')

    assert page.url.endswith('/login/')

    page.goto(urljoin(base_url, '/users/'))
    content = page.content()

    assert username in content
    assert 'E2E User' in content
