from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.keys import Keys
from unidecode import unidecode
from bs4 import BeautifulSoup
from os import system
from DataBase import Phones, session


print("[x] Waiting For Load Driver . . .") ## LOG
driver = webdriver.Firefox(executable_path="C://geckodriver.exe")
system("clear")

def check_element_exist(mode, inp):
    try:
        return driver.find_element(mode, inp)
    except:
        return False


def validate_pagination(pagination):
    try:
        num = pagination.text.split()[-1]
        return unidecode(num)
    except Exception as err:
        return 100


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
    return validate_pagination(pagination)


def validate_link(link):
    valid = link.split("/")[:3]
    return "/".join(valid)


def extract_products():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    source = soup.find("div", {"class": "d-flex flex-wrap"})
    return source.find_all("div", {"class": "border-b border-l"})


def extract_product_information(products):
    objects = []
    for product in products:
        link = validate_link(product.find("a")["href"])
        image = product.find("img")["data-src"]
        name = product.find("h2").text
        # try:
        price = product.find(class_="d-flex ai-center jc-end gap-1 color-700 color-400 text-h5 grow-1").span.text
        objects.append(Phones(link=link, photo=image, name=name, price=unidecode(price)))
        # except:
        #     return False
    session.add_all(objects)
    session.commit()
    print("[+] Add ", len(objects), "Objects in DataBase")


def main(url):
    ## Example Url "https://www.digikala.com/search/category-notebook-netbook-ultrabook/"
    core_url = url
    count = load_all_page(core_url)
    pages = [i for i in range(1, int(count))]
    cant = open("cant.txt", "a")

    for page in pages:
        url = core_url+"?page="+str(page)
        # try:
        load_all_page(url=url)
        products = extract_products()
        output = extract_product_information(products)
        if output == False:
            print("[+] Products Ended") ## LOG
            break
        # except Exception as err:
        #     cant.write(url+"\n")
        #     print("[-] Error On Page ", url)


url = input("Enter The List Of Product Like This Link:\n[https://www.digikala.com/search/category-notebook-netbook-ultrabook/]\nLink: ")
main(url)