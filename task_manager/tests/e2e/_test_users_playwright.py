import re
from urllib.parse import urljoin

import pytest
from django.contrib.auth import get_user_model
import uuid


@pytest.fixture
def register_user(page, base_url):
    def _register(first_name="E2E", last_name="User"):
        username = f"user_{uuid.uuid4().hex[:8]}"
        page.goto(urljoin(base_url, "/users/create/"))

        page.fill('input[name="first_name"]', first_name)
        page.fill('input[name="last_name"]', last_name)
        page.fill('input[name="username"]', username)
        page.fill('input[name="password1"]', "strongpass123")
        page.fill('input[name="password2"]', "strongpass123")
        page.click('text="Зарегистрировать"')
        return username, f"{first_name} {last_name}"
    return _register

DATA = {
    "users": {
        "existing": {
            "first_name": "Иван",
            "last_name": "Иванов",
            "username": "ivanov",
            "password": "testpass123"
        },
        "new": {
            "first_name": "Пётр",
            "last_name": "Петров",
            "username": "petrov",
            "password": "newpass123"
        }
    }
}


@pytest.fixture(scope="function", autouse=True)
def create_test_user(db):
    User = get_user_model()
    if not User.objects.filter(
            username=DATA["users"]["existing"]["username"]).exists():
        User.objects.create_user(
            username=DATA["users"]["existing"]["username"],
            password=DATA["users"]["existing"]["password"],
            first_name=DATA["users"]["existing"]["first_name"],
            last_name=DATA["users"]["existing"]["last_name"],
        )


def login(page, base_url):
    page.goto(urljoin(base_url, "/login/"))
    page.fill('input[name="username"]', DATA["users"]["existing"]["username"])
    page.fill('input[name="password"]', DATA["users"]["existing"]["password"])
    page.click('text="Войти"')
    page.wait_for_load_state()


def test_update_user(page, base_url):
    login(page, base_url)

    page.click('text="Пользователи"')

    full_name = (f"{DATA['users']['existing']['first_name']} "
                 f"{DATA['users']['existing']['last_name']}")
    row_selector = f"css=tr:has-text('{full_name}')"
    row = page.query_selector(row_selector)
    assert row is not None,\
        "❌ Строка с пользователем не найдена. Проверь рендеринг таблицы."

    # Клик по ссылке "Изменить"
    edit_link = row.query_selector('text="Изменить"')
    assert edit_link is not None, "❌ Не найдена кнопка 'Изменить'"
    edit_link.click()
    page.wait_for_load_state()

    # Проверка формы
    assert re.search(r"/users/\d+/update/", page.url)
    assert page.get_attribute(
        "#id_first_name", "value") == DATA["users"]["existing"]["first_name"]
    assert page.get_attribute(
        "#id_last_name", "value") == DATA["users"]["existing"]["last_name"]
    assert page.get_attribute(
        "#id_username", "value") == DATA["users"]["existing"]["username"]
    assert page.get_attribute("#id_password1", "value") is None
    assert page.get_attribute("#id_password2", "value") is None

    # Обновим данные
    page.fill('input#id_first_name', DATA["users"]["new"]["first_name"])
    page.fill('input#id_last_name', DATA["users"]["new"]["last_name"])
    page.fill('input#id_username', DATA["users"]["new"]["username"])
    page.fill('input#id_password1', DATA["users"]["new"]["password"])
    page.fill('input#id_password2', DATA["users"]["new"]["password"])
    page.click('text="Изменить"')

    page.wait_for_url(urljoin(base_url, "/users/"))
    assert page.url == urljoin(base_url, "/users/")
