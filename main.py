import requests
from bs4 import BeautifulSoup, NavigableString

for x in range(1, 51):
    url = "http://books.toscrape.com/catalogue/category/books_1/page-" + str(x) + ".html"
    page = requests.get(url)

    # Check if the page do not exist or has an error
    if page.status_code != 200:
        continue

    soup = BeautifulSoup(page.content, 'html.parser')

    # get a href: row.find(class_="image_container").find('a')['href'] == book url
    # get img src: row.find(class_="image_container").find('img')['src'] == book image

    product_page_url = ""  # done
    universal_product_code = ""  # done
    title = ""  # done
    price_including_tax = ""  # done
    price_excluding_tax = ""  # done
    number_available = ""  # done
    product_description = ""  # done
    category = ""  # done
    review_rating = ""  # done
    image_url = ""

    list_of_books = soup.find_all(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

    for book in list_of_books:
        # product_page_url = book.find(class_="image_container").find('a').get('href')
        # print("product_page_url: " + product_page_url)

        url_book = book.find(class_="image_container").find('a')['href'].replace("../../", '')
        base_url = "http://books.toscrape.com/"
        product_page_url = base_url + "catalogue/" + url_book
        print("product_page_url: " + product_page_url)
        product_page_request = requests.get(product_page_url)
        current_book_soup = BeautifulSoup(product_page_request.content, 'html.parser')

        # Check if the title do not exist or has an error
        if page.status_code != 200:
            continue

        product_description = current_book_soup.find('p', class_=False).get_text()
        print("product_description:" + product_description)

        tables = current_book_soup.find('table', class_="table table-striped")

        for table in tables:
            # skip NavigableString rows
            if isinstance(table, NavigableString):
                continue

            th = str(table.find('th').get_text())
            td = str(table.find('td').get_text())
            if th == "UPC":
                universal_product_code = td
                print("universal_product_code: " + universal_product_code)

            if th == "Price (incl. tax)":
                price_including_tax = td
                print("price_including_tax: " + price_including_tax)

            if th == "Price (excl. tax)":
                price_excluding_tax = td
                print("price_excluding_tax: " + price_excluding_tax)

            if th == "Availability":
                def extract_stock(numbers: str) -> str:
                    stock = numbers.split()
                    for number in stock:
                        num = number.replace("(", "")
                        if num.isdigit():
                            return str(num)


                number_available = extract_stock(td)
                print("number_available: " + number_available)

            if th == "Product Type":
                category = td
                print("category: " + category)

            if th == "Number of reviews":
                review_rating = td
                print("review_rating: " + review_rating)

        title = current_book_soup.find(class_="col-sm-6 product_main").find('h1').get_text()
        print("title: " + title)

        image_url = base_url + current_book_soup.find('img')['src'].replace("../../", '')
        print("image_url: " + image_url)
