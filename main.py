import requests
from bs4 import BeautifulSoup

for x in range(1, 51):
    url = "http://books.toscrape.com/catalogue/category/books_1/page-" + str(x) + ".html"
    page = requests.get(url)

    # Check if the page do not exist or has an error
    if page.status_code != 200:
        continue

    soup = BeautifulSoup(page.content, 'html.parser')

    # get a href: row.find(class_="image_container").find('a')['href'] == book url
    # get img src: row.find(class_="image_container").find('img')['src'] == book image

    product_page_url = ""
    universal_product_code = ""
    title = ""
    price_including_tax = ""
    price_excluding_tax = ""
    number_available = ""
    product_description = ""
    category = ""
    review_rating = ""
    image_url = ""

    list_of_books = soup.find_all(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

    for book in list_of_books:
        # product_page_url = book.find(class_="image_container").find('a').get('href')
        # print("product_page_url: " + product_page_url)

        url_book = book.find(class_="image_container").find('a')['href'].replace("../../", '')
        product_page_url = "http://books.toscrape.com/catalogue/" + url_book
        product_page_request = requests.get(product_page_url)
        current_book_soup = BeautifulSoup(product_page_request.content, 'html.parser')

        # Check if the title do not exist or has an error
        if page.status_code != 200:
            continue

        title = current_book_soup.find(class_="col-sm-6 product_main").find('h1').get_text()

        print("title: " + title)

        # image_url = book.find(class_="image_container").find('img')['src']
        # print("image_url: " + image_url)
