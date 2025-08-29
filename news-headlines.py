from selenium.webdriver.common.by import By
from navigate import Navigate



website = "https://www.skysports.com/"

with Navigate(teardown=True, headless=True) as bot:
    bot.get(website)
    bot.click_cookies()
    bot.find_news()