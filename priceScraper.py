from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from sys import argv


# Use this when debugging in IDE
search_matter = input("Please enter the product you would like to search for -> ") + " "
search_matter += input("Now specify the type of the product.\n"
                       " For example 'notebook, smartphone, tablet, speaker' ect -> ")

delay = 10

PATH = "/Users/edgarvildt/Developer/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("https://www.euronics.ee/en")


def toggle_search_bar_and_search(search_string : str):
    WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CLASS_NAME, "search")))
    driver.find_element(By.CLASS_NAME, "search").click()

    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "autocomplete__input")))
    input = driver.find_element(By.CLASS_NAME, "autocomplete__input")
    input.send_keys(search_matter)
    time.sleep(0.5)
    input.send_keys(Keys.RETURN)

def filter_goods_by_brand():
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "responsive-filter-button")))
    driver.find_element(By.CLASS_NAME, "responsive-filter-button").click()
    WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "sort-menu__button ")))
    data_filters = driver.find_elements(By.CLASS_NAME, "sort-menu__button ")
    data_filters[0].click()


    # Get sort menu
    WebDriverWait(driver, delay).\
        until(EC.presence_of_element_located((By.XPATH, '//*[@id="category-filter-panel"]/div/section/ul/li[1]/ul')))
    sort_menu = driver.find_element(By.XPATH, '//*[@id="category-filter-panel"]/div/section/ul/li[1]/ul')

    # Get sort menu submenu
    WebDriverWait(sort_menu, delay).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sort-menu__item')))
    results = sort_menu.find_elements(By.CLASS_NAME, 'sort-menu__item')
    assert len(results) > 0
    # Get category names for the user choice
    text_results = []
    for i in range(len(results)):
        if results[i].text == "":
            continue
        text_results.append(results[i].text.split('\n')[0])

    print('Choose the brand using the given categories \n')
    for el2 in text_results:
       print(str(text_results.index(el2) + 1) + " -> " + el2)
    chosen_brand = text_results[int(input("And the number is -> ")) - 1]
    print("You have chose ", chosen_brand)
    print("\n\n")
    # Click the button with a chosen brand
    for i in range(len(text_results)):
        if text_results[i] == chosen_brand:
            results[i].click()

def gather_price_info():

    # Updating page until all products are displayed
    update = True
    while update:
        try:
            WebDriverWait(driver, 3). \
                until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div/div[2]/button')))
            driver.find_element(By.XPATH,
                                '/html/body/div[7]/div/div[2]/button').click()
            time.sleep(0.5)
            print("New products revealed")
        except Exception:
            print("No more products to reveal\n\n")
            update = False

    WebDriverWait(driver, delay).\
        until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div/div[2]/section[3]')))
    product_list = driver.find_element(By.XPATH, '/html/body/div[7]/div/div[2]/section[3]')

    articles = []

    # Get articles separated from each other
    j = 1
    while True:
        try:
            articles.append(product_list.find_element(By.XPATH,
                                                      "/html/body/div[7]/div/div[2]/section[3]/article[" + str(j) + "]"))
            j += 1
        except Exception:
            break

    # Check if articles found
    try:
        assert len(articles) > 0
    except AssertionError:
        driver.quit()
        print("No elements in articles list")


    prices = []
    for el in articles:
        print(el.text)
        try:
            if "DISCOUNT" in el.text:
                price_of_element = el.text.split('\n')[5]
            elif "€" in el.text.split('\n')[3]:
                price_of_element = el.text.split('\n')[3]
            elif "€" in el.text.split('\n')[4]:
                price_of_element = el.text.split('\n')[4]
            prices.append(price_of_element)
        except IndexError:
            print("One was without the price ;(")

    return prices

def avg_price(numbers):
    count = 0
    total = 0
    for number in numbers:
        total += number
        count += 1
    return round((total / count), 2)

def analyze_product_prices(prices):
    float_price_list = []
    for price in prices:
        try:
            float_price_list.append(float(price[:-3].replace(" ", ".")))
        except ValueError:
            float_price_list.append(float(price[:-3]))
    minimal_price = min(float_price_list)
    maximal_price = max(float_price_list)
    average_price = avg_price(float_price_list)
    print("-------")
    print("Minimal price")
    print(minimal_price)
    print("-------")
    print("Maximum price")
    print(maximal_price)
    print("-------")
    print("Average price")
    print(average_price)

def main():
    try:
        toggle_search_bar_and_search(search_matter)
        print("Search successful\n------------")
        filter_goods_by_brand()
        print("filtering successful\n------------")
        prices = gather_price_info()
        print("price info gathered successful")
        analyze_product_prices(prices)
        print("\n\n\n")
    finally:
        driver.quit()

if __name__ == '__main__':
    main()


