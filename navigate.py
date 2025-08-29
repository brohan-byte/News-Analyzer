
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
from datetime import datetime
import os
import sys


class Navigate(webdriver.Firefox):
    def __init__(self, teardown=False, headless=False):
        self.teardown = teardown

        opts = FirefoxOptions()
        if headless:
            opts.add_argument("--headless")
        
        opts.set_preference("dom.webdriver.enabled", False)
        opts.set_preference("useAutomationExtension", False)

        super().__init__(options=opts)
        self.implicitly_wait(2)   
        self.wait = WebDriverWait(self, 15)
        try:
            self.maximize_window()
        except Exception:
            pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            try:
                self.quit()
            except Exception:
                pass

    def click_cookies(self, timeout=12):
        w = WebDriverWait(self, timeout)

       
        try:
            w.until(EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[id^='sp_message_iframe'], iframe[title*='privacy'], iframe[src*='sp-']")
            ))
        except TimeoutException:
           
            return

        for by, sel in [
            (By.CSS_SELECTOR, "button[aria-label='Essential cookies only']"),
            (By.CSS_SELECTOR, "button[title='Essential cookies only']"),
            (By.XPATH, "//button[normalize-space()='Essential cookies only']"),
            (By.XPATH, "//button[contains(.,'Accept all') or contains(.,'Accept All')]"),
        ]:
            try:
                w.until(EC.element_to_be_clickable((by, sel))).click()
                break
            except TimeoutException:
                continue

        # always return to the main page
        self.switch_to.default_content()

    def find_news(self):
        elements = self.find_elements(By.XPATH, "//div[@class='sdc-site-tiles__group']/div[contains(@class,'sdc-site-tiles__item')]")
        titles = []
        links = []
        
        for element in elements:
            # skip the “live on sky” tiles
            if element.find_elements(By.XPATH, ".//a[contains(@class,'sdc-site-live-on-sky__link')]"):
                continue

            
            title_els = element.find_elements(By.XPATH, ".//span[contains(@class,'sdc-site-tile__headline-text')]")
            
            link_els  = element.find_elements(By.XPATH, ".//a[contains(@class,'sdc-site-tile__headline-link')] | .//h3//a")

            if not title_els or not link_els:
                continue

            news_title = (title_els[0].text or "").strip()
            page_link  = link_els[0].get_attribute("href")

            if news_title and page_link:
                titles.append(news_title)
                links.append(page_link)


        application_path = os.path.dirname(sys.executable)
        now = datetime.now()
        month_day_year = now.strftime("%m%d%Y")
        my_dict = {'title': titles, 'link': links}
        df_headlines = pd.DataFrame(my_dict)
        file_name = f'headlines--{month_day_year}.csv'
        final_path = os.path.join(application_path, file_name)
        df_headlines.to_csv(final_path)

        

        
