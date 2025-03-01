from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

"""Web Scraping"""
header = {
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

# Zillow Clone
rental_page = "https://appbrewery.github.io/Zillow-Clone/"
response = requests.get(rental_page, headers=header)

text = response.text
soup = BeautifulSoup(text, "lxml")

# Making lists of links, prices and addresses
links = soup.find_all(name="a", class_="StyledPropertyCardDataArea-anchor")
links_list = [link.get('href') for link in links]
print(links_list)

prices = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")
prices_list = [price.getText().strip("+/mo").strip("+ 1db") for price in prices]
print(prices_list)

addresses = soup.find_all(name="address")
addresses_list = [address.getText().strip() for address in addresses]
print(addresses_list)

"""Automatic Filing"""
google_form = "YOUR FORMS LINK"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(google_form)

# Filing forms
for i in range(0, len(links_list), 1):
    enter_address = driver.find_element(by=By.XPATH,
                                        value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    enter_address.send_keys(addresses_list[i])

    enter_price = driver.find_element(by=By.XPATH,
                                      value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    enter_price.send_keys(prices_list[i])

    enter_link = driver.find_element(by=By.XPATH,
                                     value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    enter_link.send_keys(links_list[i])

    send = driver.find_element(by=By.XPATH,
                               value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    send.click()

    again = driver.find_element(by=By.XPATH,
                                value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    again.click()

driver.quit()

