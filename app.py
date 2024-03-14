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
def add_product_to_database(name, price, link):
    sql = "INSERT INTO products (name, price, link) VALUES (%s, %s, %s)"
    val = (name, price, link)
    cursor.execute(sql, val)
    db.commit()

#Funkcja do czyszczenia danych
def clear_previous_data():
    sql = "TRUNCATE TABLE products"
    cursor.execute(sql)
    db.commit()


@app.route('/')
def hello_world():
    # Pobranie danych z bazy danych
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run()
