import pytest
import requests
from bs4 import BeautifulSoup

#Test sprawdzający czy strony internetowa zwraca kod 200
@pytest.mark.integrationTest
def test_homepage_status_code():
    response = requests.get('http://127.0.0.1:5000')
    assert response.status_code == 200

#Test sprawdzający czy strona główna nagłówek
@pytest.mark.integrationTest
def test_homepage_has_products():
    response = requests.get('http://127.0.0.1:5000')
    assert b'Produkty pobrane ze strony skapiec.pl' in response.content

#Test sprawdzający czy strona wyświetla szczegóły produktu (nazwa, cena, zdjęcie)
@pytest.mark.integrationTest
def test_homepage_displayed_details():
    response = requests.get('http://127.0.0.1:5000')

    soup = BeautifulSoup(response.text, 'html.parser')
    product_containers = soup.find_all('div', class_='square')
    assert len(product_containers) > 0

    for product_container in product_containers:
        assert product_container.find('img') is not None
        assert product_container.find('a') is not None
        assert product_container.find('p') is not None

