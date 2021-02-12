import csv
import requests
from bs4 import BeautifulSoup, NavigableString

# in this array we will save the data once is extracted
# to be included in the CSV file
all_books_data = []


# this method will extract the total number of pages from index.html
def extract_number_of_pages() -> int:
    index_url = "http://books.toscrape.com/index.html"
    home = requests.get(index_url)
    # Check if the page do not exist or has an error
    if home.status_code != 200:
        return 0

    home_soup = BeautifulSoup(home.content, 'html.parser')

    current = home_soup.find('li', class_='current').get_text().split()

    # remove from the array are not a number
    for c in current:
        if not c.isdigit():
            current.remove(c)

    # return the latest number in the array:
    # e.g.: in (1 of 50) will return 51 to get get range of 0 to 50
    if len(current) > 0:
        return int(current[len(current) - 1]) + 1
    else:
        return 0


# extract the required information into an all_books_data array:
for x in range(extract_number_of_pages()):
    url = "http://books.toscrape.com/catalogue/category/books_1/page-" + str(x) + ".html"
    page = requests.get(url)

    # Check if the page do not exist or has an error
    if page.status_code != 200:
        continue

    soup = BeautifulSoup(page.content, 'html.parser')

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

        url_book = book.find(class_="image_container").find('a')['href'].replace("../../", '')
        base_url = "http://books.toscrape.com/"
        product_page_url = base_url + "catalogue/" + url_book
        # print("product_page_url: " + product_page_url)
        product_page_request = requests.get(product_page_url)
        current_book_soup = BeautifulSoup(product_page_request.content, 'html.parser')

        # Check if the title do not exist or has an error
        if page.status_code != 200:
            continue

        try:
            product_description = current_book_soup.find('p', class_=False).get_text()
        except:
            product_description = ""

        title = current_book_soup.find(class_="col-sm-6 product_main").find('h1').get_text()

        image_url = base_url + current_book_soup.find('img')['src'].replace("../../", '')

        tables = current_book_soup.find('table', class_="table table-striped")

        for table in tables:
            # skip NavigableString rows
            if isinstance(table, NavigableString):
                continue

            th = str(table.find('th').get_text())
            td = str(table.find('td').get_text())
            if th == "UPC":
                universal_product_code = td

            if th == "Price (incl. tax)":
                price_including_tax = td

            if th == "Price (excl. tax)":
                price_excluding_tax = td

            if th == "Availability":
                def extract_stock(numbers: str) -> str:
                    stock = numbers.split()
                    for number in stock:
                        num = number.replace("(", "")
                        if num.isdigit():
                            return str(num)


                number_available = extract_stock(td)

            if th == "Product Type":
                category = td

            if th == "Number of reviews":
                review_rating = td

        all_books_data.append([
            product_page_url,
            universal_product_code,
            title,
            price_including_tax,
            price_excluding_tax,
            number_available,
            product_description,
            category,
            review_rating,
            image_url,
        ])
        print("Book: " + title + ", has been added")

# create CSV file:
scraped_file = "book_scraped.csv"

headers = [
    "product_page_url",
    "universal_product_code",
    "title",
    "price_including_tax",
    "price_excluding_tax",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url",
]
with open(scraped_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(headers)
    for row in all_books_data:
        writer.writerow(row)
