# Web-Scraping-and-Selenium-Projects

## Key Libraries Used
- selenium – For browser automation and web interaction.
- requests – For making HTTP requests to websites and APIs.
- BeautifulSoup (bs4) – For parsing HTML and extracting data.
- spotipy – For interacting with the Spotify Web API.
- lxml – As the parser for BeautifulSoup.
- smtplib – For sending email notifications.
- dotenv – For loading environment variables from a .env file.

## Project Descriptions

### Auto Data Entry Project📋
Scrapes rental listing data (links, prices, addresses) from a Zillow clone website using BeautifulSoup, then automates data entry into a Google Form with Selenium.

### Auto Cookie Clicker🍪
Automates the classic Cookie Clicker game using Selenium. The bot continuously clicks the cookie and periodically evaluates available upgrades, purchasing the most expensive one it can afford.

### Spotify Time Machine🎶
Scrapes the Billboard Hot 100 chart for a given date using BeautifulSoup, searches for the corresponding tracks on Spotify using Spotipy, and creates a private Spotify playlist with the results.

### Amazon Price Tracker🛒
Scrapes product details (name and price) from a live Amazon product page using BeautifulSoup. If the price drops below a specified target, an email alert is sent via SMTP.
