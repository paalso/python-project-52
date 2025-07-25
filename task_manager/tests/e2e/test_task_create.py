from urllib.parse import urljoin

import pytest

DATA = {
    'tasks': {
        'first': {
            'name': 'Task # 1',
            'description': 'Task # 1 description',
            'status': 'completed',
            'executor': 'Paul S',
        }
    }
}


@pytest.mark.playwright
def test_create_task(page, base_url):
    page.goto(urljoin(base_url, "/login/"))
    page.fill('input[name="username"]', 'plato')
    page.fill('input[name="password"]', 'qwe')
    page.click('text="Войти"')
    page.wait_for_load_state()

    assert 'Вы залогинены' in page.content()

    page.goto("/tasks/")
    page.click('text="Создать задачу"')
    page.wait_for_load_state()
    assert page.url == urljoin(base_url, "/tasks/create/")

    page.fill('text="Имя"', DATA["tasks"]["first"]["name"])
    page.fill('text="Описание"', DATA["tasks"]["first"]["description"])
    page.select_option(
        'text="Статус"', label=DATA["tasks"]["first"]["status"]
    )
    page.select_option(
        'text="Исполнитель"', label=DATA["tasks"]["first"]["executor"]
    )
    page.pause()
