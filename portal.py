import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

url = "https://books.toscrape.com/"
response = requests.get(url)

if response.status_code != 200:
    print("Не удалось подключиться к сайту")
    exit()

soup = BeautifulSoup(response.text, "html.parser")
books = soup.find_all("article", class_="product_pod")

titles = []
prices = []
image_links = []

for book in books:
    h3_tag = book.find("h3")
    if not h3_tag:
        continue
    a_tag = h3_tag.find("a")
    if not a_tag or not a_tag.get("title"):
        continue
    title = a_tag["title"]
    titles.append(title)
    price_tag = book.find("p", class_="price_color")
    if price_tag:
        prices.append(price_tag.text)
    else:
        prices.append("")
    img_div = book.find("div", class_="image_container")
    if img_div:
        img_tag = img_div.find("img")
        if img_tag and img_tag.get("src"):
            img_full = "https://books.toscrape.com/" + img_tag["src"]
            image_links.append(img_full)
        else:
            image_links.append("")
    else:
        image_links.append("")
df = pd.DataFrame({
    "Название": titles,
    "Цена": prices,
    "Ссылка на картинку": image_links
})
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
filepath = os.path.join(desktop, "books.xlsx")
df.to_excel(filepath, index=False)
print(f"Готово! Данные сохранены в {filepath}")