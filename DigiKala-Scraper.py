from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from DataBase import Products, session
from unidecode import unidecode
from bs4 import BeautifulSoup
from time import sleep
from os import system

system("clear")

def check_element_exist(mode, inp):
    try:
        return driver.find_element(mode, inp)
    except:
        return False


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


def shorten_link(link):
    valid = link.split("/")[:3]
    return "/".join(valid)


def extract_products():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    source = soup.find("div", {"class": "d-flex flex-wrap"})
    return source.find_all("div", {"class": "border-b border-l"})


def extract_product_information(products):
    objects = []
    for product in products:
        link = shorten_link(product.find("a")["href"])
        image = product.find("img")["data-src"]
        name = product.find("h2").text
        try:
            price = product.find(class_="d-flex ai-center jc-end gap-1 color-700 color-400 text-h5 grow-1").span.text
            objects.append(Products(link=link, photo=image, name=name, price=unidecode(price)))
            system("clear")
        except:
            return False
    session.add_all(objects)
    session.commit()
    system("clear")
    print("[+] Add ", len(objects), "Objects in DataBase") ## LOG


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


url = input("Enter The List Of Product Like This Link:\n[https://www.digikala.com/search/category-notebook-netbook-ultrabook/]\nLink: ")
system("clear")
print("[x] Waiting For Load Driver . . .") ## LOG
driver = webdriver.Firefox(executable_path="C://geckodriver.exe")
system("clear")
main(url)