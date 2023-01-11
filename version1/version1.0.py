import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


class GoogleMapsScraper:

    def create_driver(self):
        """
        Create the driver and maximize the window
        :return: driver
        """
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome("..\\chromedriver.exe", options=options)  # FIXME locate chromedriver
        driver.maximize_window()
        return driver

    def navigate_to_url(self, driver, url):
        """
        Open the URL  and it will wait 5 seconds till the whole page gets loaded
        :param driver:
        :param url: url of a business in google maps
        """
        driver.get(url)
        time.sleep(5)

    def scroll_side_panel_to_load_all_reviews(self, driver):
        """
        Scroll the side panel to load all the revies
        :param driver: driver will find the side panel and then scroll into it
        :return: None
        """
        driver.find_element(By.XPATH,
                            '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]/span[1]/span').click()
        last_height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(5)

        while True:
            google_maps_side_panel = driver.find_element(By.XPATH,
                                                         '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
            driver.execute_script(f'arguments[0].scrollBy(0, arguments[0].scrollHeight);', google_maps_side_panel)
            time.sleep(2)
            google_maps_side_panel = driver.find_element(By.XPATH,
                                                         '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
            new_height = driver.execute_script("return arguments[0].scrollHeight", google_maps_side_panel)
            if new_height == last_height:
                break
            last_height = new_height

    def click_see_more_buttons(self, driver):
        """
        Click to all  "More" buttons to get all HTML
        """
        buttons_in_review_widget = driver.find_elements(By.CLASS_NAME, "w8nwRe")
        for button in buttons_in_review_widget:
            if button.text == "More":
                button.click()
                time.sleep(2)

    def soup(self, driver):
        """
        Parse all HTML and returns it

        """
        return BeautifulSoup(driver.page_source, "lxml")

    def all_review_widgets(self, soup):
        """
        Get a list of HTML code for each review widget
        """
        return soup.find_all("div", class_="jftiEf fontBodyMedium")

    def create_df_and_populate_from_extracted_data(self, all_reviews):
        """
        # Populate data frame with the data extracted from all reviews
        and save it to csv file
        :param all_reviews: list of all review widgets
        """

        df = pd.DataFrame(columns=['Reviewer Name', 'Review Content',
                                   'Full Review Link', 'Rating', 'Review Time Information',
                                   "Owner Reply", 'Reply Text From Owner'])

        for review in all_reviews:
            reviewer_name = review.find("div", class_="d4r55").find("span").text
            review_content = review.find("span", class_="wiI7pd").text
            full_review_link = review.find("a")['href']
            rating = int((review.find_all("div", class_="DU9Pgb")[0].find("span").text)[0])
            review_time_information = review.find("div", class_="DU9Pgb").find("span", {"jstcache": "1539"}).text
            owner_reply = True if review.find("span", class_="nM6d2c") is not None else False
            if owner_reply:
                reply_text_from_owner = review.find("div", class_="wiI7pd").text
            else:
                reply_text_from_owner = ''

            row_of_data = [reviewer_name, review_content,
                           full_review_link, rating, review_time_information, owner_reply, reply_text_from_owner]

            length_of_data_frame = len(df)
            df.loc[length_of_data_frame] = row_of_data

        df.to_csv("..\\version1.0.csv")  # FIXME  save to your own location


if __name__ == "__main__":
    scraper = GoogleMapsScraper()
    url = "https://www.google.com/maps/place/Aspria+Berlin+Ku%E2%80%99damm/@52.5003887,13.2941771,17z/data=!4m20!1m11!3m10!1s0x47a850c4b634ef93:0x2faf0f02eacd864e!2sAspria+Berlin+Ku%E2%80%99damm!5m2!4m1!1i2!8m2!3d52.5003887!4d13.2941771!9m1!1b1!3m7!1s0x47a850c4b634ef93:0x2faf0f02eacd864e!5m2!4m1!1i2!8m2!3d52.5003887!4d13.2941771"  # TODO change to the url you want
    driver = scraper.create_driver()
    scraper.navigate_to_url(driver=driver, url=url)
    scraper.scroll_side_panel_to_load_all_reviews(driver=driver)
    soup = scraper.soup(driver=driver)
    all_reviews = scraper.all_review_widgets(soup=soup)
    scraper.click_see_more_buttons(driver=driver)
    dataframe = scraper.create_df_and_populate_from_extracted_data(all_reviews=all_reviews)
