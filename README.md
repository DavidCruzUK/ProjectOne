# Project One
This project scrap the url `http://books.toscrape.com/` exctacting data from each book into a CSV file.

### Dependencies included in the requeriments.txt: 
* beautifulsoup4 == 4.9.3
* certifi == 2020.12.5
* chardet == 4.0.0
* idna == 2.10
* requests == 2.25.1
* soupsieve == 2.2
* urllib3 == 1.26.3


## Steps for setup and run this app:
* Unzip the file in a path of your choice: (e.g.: `/Users/davidcruz/`)
* Access to that folder: `cd /Users/davidcruz/ProjectOne-master`
* Create Virtual Enviroment: `python3 -m venv venv/`
* Run your VENV: `source venv/bin/activate`
* Install required dependencies: `pip install -r requirements.txt`
* Run the script: `python main.py`

## After run the scrypt:
After run `main.py` scrypt you will see different logs:
* This log it tells you the current page: `Currently retrieving page 1 of 50`
* The following logs shows when the book has been added to the Array:
```
Book: A Light in the Attic, has been added
Book: Tipping the Velvet, has been added
Book: Soumission, has been added
... more books ....
```
* `...DONE...` Will be displayed when the scrypt finish
* Once all books has been correctly retrieved the csv file can be found in the root of the project:
```
// For our example:
e.g.: /Users/davidcruz/ProjectOne-master/book_scraped.csv
```



#### Python path Project assesment:
David Cruz anaya
