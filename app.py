from flask import Flask, render_template
from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
import mysql.connector

ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

# Konfiguracja połączenia z bazą danych MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="skapiec_data"
)

cursor = db.cursor()


# Funkcja do dodawania danych do bazy
def add_product_to_database(name, price, link, url_src):
    sql = "INSERT INTO products (name, price, link, img_url) VALUES (%s, %s, %s, %s)"
    val = (name, price, link, url_src)
    cursor.execute(sql, val)
    db.commit()


# Funkcja do czyszczenia danych
def clear_previous_data():
    sql = "TRUNCATE TABLE products"
    cursor.execute(sql)
    db.commit()

# Funkcja do pobierania danych z bazy danych
def get_products_from_database():
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()


@app.route('/')
def hello_world():
    url = "https://www.skapiec.pl/szukaj?query=rower&categoryId="
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    product_elements = soup.find_all("div", class_="product-box-narrow-container")

    clear_previous_data()

    for product_element in product_elements:
        link_element = product_element.find("a", class_="product-box-narrow-link")
        name = link_element.get('aria-label')
        link = link_element.get('href')

        price_element = product_element.find("span", class_="price")
        price = price_element.text.strip()

        div_img_element = product_element.find("div", class_="product-box-narrow__photo-box-image")
        img_element = div_img_element.find('img')
        img_url = img_element.get('src')

        # Dodawanie produktu do bazy danych MySQL
        add_product_to_database(name, price, link, img_url)

    # Pobranie danych z bazy danych
    products = get_products_from_database()

    return render_template('index.html', products=products)


if __name__ == '__main__':
    app.run()