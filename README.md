# DigiKala-Scraper
This is Scraper For Digikala with Selenium and Bs4 for Scrap and SqlArhemy for save data in database

# Installation
- clone the project
```
git clone https://github.com/Cmatrix1/DigiKala-Scraper
```

- FireFox Or Chrome Driver For Open Browser With Selenium Introduce the Web Driver Path in Line 82
- [Download Web Driver](https://github.com/mozilla/geckodriver/releases/tag/v0.31.0)
```python
driver = webdriver.Firefox(executable_path="C://geckodriver.exe")
```

- install requirements
```
pip install requirements.txt
```

- run the project
```
python DigiKala-Scraper.py
```

# Usage

- after run the project Enter Your Url Here
```bash
Enter The List Of Product Like This Link:
[https://www.digikala.com/search/category-notebook-netbook-ultrabook/]
Link: https://www.digikala.com/search/category-men-clothing/
```
- and Press Enter

# Configuration

- Enter Your DataBase Name in line 9 in File DataBase.py
```python
engine = create_engine('sqlite:///digikala.db', echo=True)
```
- Enter Your Table DataBase Name in line 15 in File DataBase.py
```python
__tablename__ = 'Digikala'
```

# Document
### Import the requirements librarys
- Slenium for Web Sraping and Open Browser
- time for wait for load the pages
- unidecode for Convert Persian numbers to English
- Bs4 for pulling data out of HTML
- Database is file in this directory


```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.keys import Keys
from unidecode import unidecode
from bs4 import BeautifulSoup
from os import system
from DataBase import Phones, session

system("clear")
```

- The function checks whether the element is on the page or not


```python
def check_element_exist(mode, inp):
    try:
        return driver.find_element(mode, inp)
    except:
        return False
```

- This is function for load the digikala pages 
- This function looks for pagination because pagination is loaded when the entire content is loaded


```python
def load_all_page(url):
    print("[x] Waiting For Load Page ", url) ## LOG
    driver.get(url)
    body = driver.find_element("tag name", "html")
    pagination = check_element_exist("xpath", "/html/body/div[1]/div[1]/div[3]/div[3]/div[1]/div/section[1]/div[2]/div[2]/div[2]")
    while not pagination:
        print("[x] Try to Loading Page", url) ## LOG
        body.send_keys(Keys.END)
        sleep(2)
        pagination = check_element_exist("xpath", "/html/body/div[1]/div[1]/div[3]/div[3]/div[1]/div/section[1]/div[2]/div[2]/div[2]")
    sleep(3)
    print(f"[+] Page {url} Loaded") ## LOG
```

- This function is used to shorten the Url of the product image


```python
def shorten_link(link):
    valid = link.split("/")[:3]
    return "/".join(valid)
```

- This function extracts the elements of all the products on the page


```python
def extract_products():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    source = soup.find("div", {"class": "d-flex flex-wrap"})
    return source.find_all("div", {"class": "border-b border-l"})
```

- This function is used to extract detailed product information and checks if the product price element is "ناموجود" (unavailable)and exits the program if it is not available


```python
def extract_product_information(products):
    objects = []
    for product in products:
        link = shorten_link(product.find("a")["href"])
        image = product.find("img")["data-src"]
        name = product.find("h2").text
        try:
            price = product.find(class_="d-flex ai-center jc-end gap-1 color-700 color-400 text-h5 grow-1").span.text
            objects.append(Phones(link=link, photo=image, name=name, price=unidecode(price)))
            system("clear")
        except:
            return False
    session.add_all(objects)
    session.commit()
    system("clear")

    print("[+] Add ", len(objects), "Objects in DataBase") ## LOG
```

- This function connects all program functions together
First, the user adds the first page to the input link and starts loading the page and products 


```python
def main(url):
    ## Example Url "https://www.digikala.com/search/category-notebook-netbook-ultrabook/"
    cant = open("cant.txt", "a")
    for i in range(1, 100):
        url_p = url+"?page="+str(i)
        try:
            load_all_page(url=url_p)
            products = extract_products()
            output = extract_product_information(products)
            if output == False:
                print("[+] Products Ended") ## LOG
                break
        except Exception as err:
            cant.write(url+"\n")
            print("[-] Error On Page ", url_p)
```

- And here we get input from the user and open the browser and load the url


```python
url = input("Enter The List Of Product Like This Link:\n[https://www.digikala.com/search/category-notebook-netbook-ultrabook/]\nLink: ")
system("clear")
print("[x] Waiting For Load Driver . . .") ## LOG
driver = webdriver.Firefox(executable_path="C://geckodriver.exe")
system("clear")
main(url)
```
