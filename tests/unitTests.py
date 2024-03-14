import pytest
from app import add_product_to_database,get_products_from_database, clear_previous_data

@pytest.fixture(scope="function")
def clean_database():
    clear_previous_data()
    yield

def test_add_product_to_database(clean_database):
    add_product_to_database("test product name",
                            "test product price", "test link", "test url")
    products = get_products_from_database()
    assert len(products) == 1
    assert products[0][1] == "test product name"
    assert products[0][2] == "test product price"
    assert products[0][3] == "test link"
    assert products[0][4] == "test url"

def test_clear_previous_data(clean_database):
    add_product_to_database("test product name",
                            "test product price", "test link", "test url")
    products_before_clear = get_products_from_database()
    assert len(products_before_clear) == 1
    print("PRZED", products_before_clear)
    products_after_clear = get_products_from_database()
    assert len(products_after_clear) == 0

