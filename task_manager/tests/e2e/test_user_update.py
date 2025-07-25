import random
import re
import pytest
from urllib.parse import urljoin

def rand_int():
    return random.randint(1, 1000)


@pytest.mark.playwright
def test_update_user(page, base_url):
    page.goto(urljoin(base_url, "/login/"))
    #Взял существующего в БД юзера
    page.fill('input[name="username"]', 'plato')
    page.fill('input[name="password"]', 'qwe')
    page.click('text="Войти"')
    page.wait_for_load_state()

    assert 'Вы залогинены' in page.content()

    page.goto(urljoin(base_url, "/users/"))

    assert page.query_selector('text="plato"') is not None
    row = page.query_selector('xpath=//tr[td[contains(text(), "plato")]]')
    row.query_selector('text="Изменить"').click()
    page.wait_for_load_state()
    assert re.search(r"/users/\d+/update/", page.url)
    page.fill('input[name="first_name"]', f"Plato{rand_int()}")
    page.fill('input[name="last_name"]', f"Platonicus{rand_int()}")
    # page.fill('input[name="username"]', "new_unique_username123")
    page.fill('input[name="password1"]', 'qwe')
    page.fill('input[name="password2"]', 'qwe')
    # page.pause()
    page.click('text="Изменить"')
    page.wait_for_load_state()
    assert page.url == urljoin(base_url, "/users/")
