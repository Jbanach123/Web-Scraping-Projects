from bs4 import BeautifulSoup
import requests
import lxml
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

practice_url = "https://appbrewery.github.io/instant_pot/"
live_url = "https://www.amazon.com/LordBiulder-Building-Architecture-Collection-Compatible/dp/B0CVXBRZXY/ref=sr_1_11_sspa?crid=RHO9WKMTSO70&dib=eyJ2IjoiMSJ9.cGedirdslhcbTZGGYLsHUlLcW72aN5RgkU2eGAeEVC6W0xUbnkKIcxyByxKBLBafi6w754XtjTjR0eavfqBfF1bQYZOkbNkD1NLa59SC6CNWthiEET5D9mW5Q-Ui7O1n7qhga8aDv5QCzcW7r0EaP-h8lqi8KnvrhwP6QU2FfpUgoScJaHXy29Q9g3X1wdgUJe_T7tJ6gOxcbaVKesjt31fjyVWgi4UI-dIuBNl47zVgAkauGd-GjpIS60Ljg2p245rg09Y7RDDaoUUtwcdV_ZaNBNfVF7PFdsbrB4hPy7w.QzCF5YLzLOS6AhWF39lAU-4rHN4wexda9ppolcg212Y&dib_tag=se&keywords=lego&qid=1728310958&sprefix=lego%2Caps%2C279&sr=8-11-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9tdGY&psc=1"

target_price = 30 # Set higher if you want to check if it works

# Scraping website to get the price
response = requests.get(live_url, headers={"Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
                                               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"})
text = response.text
soup = BeautifulSoup(text, "lxml")
currency = soup.find(name="span", class_="a-price-symbol").getText()
decimal = soup.find(name="span", class_="a-price-whole")
fraction = soup.find(name="span", class_="a-price-fraction")

price = decimal.getText() + fraction.getText()
price_as_float = float(price)

# Scraping Website for name
scrap_name = soup.find(name="span", id="productTitle")
name = scrap_name.getText()

# Sending email if price is lower than our target
if price_as_float < target_price:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=os.environ["MY_ADDRESS"], password=os.environ["PASSWORD"])
        connection.sendmail(
            from_addr=os.environ["MY_ADDRESS"],
            to_addrs=os.environ["MY_ADDRESS"],
            msg=f"Subject:Hot offer\n\n{name} is now {currency}{price}.\n {live_url}".encode("utf-8")
        )
print(soup.prettify())
