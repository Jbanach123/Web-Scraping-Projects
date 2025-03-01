from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

# Locate the cookie button to be clicked repeatedly.
cookie_button = driver.find_element(by=By.ID, value="cookie")

# Retrieve all store items and extract their IDs for upgrade options.
store_items = driver.find_elements(by=By.CSS_SELECTOR, value="#store div")
upgrade_ids = [item.get_attribute("id") for item in store_items]

# Set initial timeouts: check for upgrades every 5 seconds and run for 5 minutes.
check_interval_end = time.time() + 5
end_time = time.time() + 60 * 5  # 5 minutes

while True:
    cookie_button.click()

    # Every 5 seconds, evaluate available upgrades.
    if time.time() > check_interval_end:
        # Get all upgrade price elements.
        price_elements = driver.find_elements(By.CSS_SELECTOR, value="#store b")
        upgrade_prices = []

        # Parse each price element to extract the cost as an integer.
        for price in price_elements:
            text = price.text
            if text != "":
                cost = int(text.split("-")[1].replace(",", ""))
                upgrade_prices.append(cost)

        # Map each upgrade's price to its corresponding store item ID.
        upgrades = {}
        for i in range(len(upgrade_prices)):
            upgrades[upgrade_prices[i]] = upgrade_ids[i]

        # Retrieve the current cookie count from the page.
        cookies_text = driver.find_element(By.ID, value="money").text
        if "," in cookies_text:
            cookies_text = cookies_text.replace(",", "")
        cookies_available = int(cookies_text)

        # Identify which upgrades are affordable based on the current cookie count.
        purchasable_upgrades = {}
        for price, upgrade_id in upgrades.items():
            if cookies_available > price:
                purchasable_upgrades[price] = upgrade_id

        # If there are affordable upgrades, purchase the most expensive one.
        if purchasable_upgrades:
            max_affordable_price = max(purchasable_upgrades)
            upgrade_to_buy_id = purchasable_upgrades[max_affordable_price]
            driver.find_element(By.ID, value=upgrade_to_buy_id).click()

        # Reset the interval check to occur in the next 5 seconds.
        check_interval_end = time.time() + 5

    # After 5 minutes, stop the bot and display the cookies-per-second rate.
    if time.time() > end_time:
        cookies_per_second = driver.find_element(By.ID, value="cps").text
        print(cookies_per_second)
        break
