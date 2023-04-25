# -*- coding: utf-8 -*-
import os
from typing import Any
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ex_cond
from selenium.common.exceptions import TimeoutException as TE
from selenium.common.exceptions import NoSuchElementException as NSEE
from bs4 import BeautifulSoup
from background import start_schedule

UserAgent = "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"
citilink_url = "https://www.citilink.ru/catalog/smartfony/"
directory = os.getcwd()
env_path = directory + "\chromedriver"
chromedriver_path = env_path + "\chromedriver.exe"
os.environ['PATH'] += env_path  # Добавляет chromedriver в PATH
js_scroll = "arguments[0].scrollIntoView();"

def count_files(path: str):
    return len([file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))])

class CitilinkParser:
    def __init__(self, chromedriver_path: str, url: str):
        self.driver = None
        self.service = Service(chromedriver_path)
        self.options = webdriver.ChromeOptions()
        # self.options.headless = True
        self.options.add_experimental_option("excludeSwitches", ['enable-automation'])
        self.options.add_argument(f'--user-agent={UserAgent}')

        self.citilink_url = url

    def move_to(self, method: Any, string: str):
        self.driver.execute_script(js_scroll, self.driver.find_element(method, string))

    def click_on(self, method: Any, string: str):
        self.driver.find_element(method, string).click()

    def wait(self, method: Any, time: int, string: str):
        try:
            WebDriverWait(self.driver, time).until(ex_cond.presence_of_element_located((method, string)))
        except TE:
            print(f"TimeoutException - {string}")

    def save_page(self, filename: str):
        with open(filename, 'w+', encoding="utf-8") as f:
            f.write(self.driver.page_source)

    def web_parser(self):
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.get(url=self.citilink_url)
        try:
            self.wait(By.XPATH, 10, "//span[contains(@class,'e1j9birj0 e106ikdt0')]")
            self.click_on(By.XPATH, "//span[text()='Фильтры']")
            self.move_to(By.XPATH, "//button[text()='5% и больше']")
            self.click_on(By.XPATH, "//button[text()='5% и больше']")
            self.click_on(By.XPATH, "//button[contains(@class,'e1ynvv0q0 eblt8r0')]")
            for i in range(2, 100):
                try:
                    self.save_page(f"pages/page{i-1}.html")
                    print(f"Saved page {i-1};")
                    sleep(1)
                    self.wait(By.XPATH, 5, "//div[@data-meta-name='PaginationElement__go-forward']")
                    self.move_to(By.XPATH, "//div[@data-meta-name='PaginationElement__go-forward']")
                    self.move_to(By.XPATH, "//div[@data-meta-name='PaginationElement__go-forward']")
                    self.click_on(By.XPATH, "//div[@data-meta-name='PaginationElement__go-forward']")
                except NSEE:
                    print("End of page saving.")
                    break

        except Exception as ex:
            print(ex)
        finally:
            self.driver.close()
            self.driver.quit()

    def html_parser(self, pages_num: int):
        data = []
        for i in range(1, pages_num + 1):
            with open(f"pages/page{i}.html", "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file.read(), "lxml")
            products = soup.find_all("div", {'data-meta-name': 'SnippetProductHorizontalLayout'})
            for product in products:
                head = product.find("a", class_='app-catalog-9gnskf e1259i3g0')
                if head is None:
                    continue
                prices = product.find("div", class_="app-catalog-zybnbl ep7361f0").find_all("span")
                img_link = product.find("div", class_="app-catalog-lxji0k e153n9o30").find('img')['src']
                title = head["title"]
                link = f"https://www.citilink.ru{head['href']}"
                full_price = int(prices[0].text.replace(" ", ""))
                discount_price = int(prices[1].text[:-1].replace(" ", ""))
                discount = int((1 - discount_price / full_price) * 100)
                data.append({"title": title,
                             "link": link,
                             "img_link": img_link,
                             "full_price": full_price,
                             "discount_price": discount_price,
                             "discount": discount})
        # print(data)
        print(f"{len(data)} positions were processed.")



if __name__ == "__main__":
    parser = CitilinkParser(chromedriver_path=chromedriver_path, url=citilink_url)
    parser.web_parser()
    pages_num = count_files("pages")
    parser.html_parser(pages_num)