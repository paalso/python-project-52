from urllib.parse import urljoin


def test_homepage_loads(page, base_url):
    page.goto(urljoin(base_url, "/"))

    assert 'Привет от Хекслета!' in page.content()
    assert page.title() == 'Менеджер задач'
