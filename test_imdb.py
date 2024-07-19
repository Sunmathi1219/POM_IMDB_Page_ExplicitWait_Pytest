""""
test_imdb.py

Using Page Object Model(POM),explicit wait,expected conditions and pytest kindly do the following task mentioned below
1.) go to the https://www.imdb.com/search/name/
2.)fill the data given in the input boxes,select boxes and drop down menu on the web page and do a search
3.)do bot use sleep() method fot the task.
"""



from TestData.Imdb_Data import ImdbPage
from TestLocators.Imdb_Locators import Locators
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
#for explicit wait only
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pytest


class Test_Imdb:

    @pytest.fixture
    #Booting function for running all the pytest
    def booting_function(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        yield
        self.driver.close()

    #To get title
    def test_get_title(self, booting_function):
        try:
            self.driver.get(ImdbPage().url)
            assert self.driver.title == ImdbPage().title
            print("Success:IMDB Page title is verified")
        except WebDriverException as e:
            print(e)

    #To verify url
    def test_verify_url(self, booting_function):
        try:
            self.driver.get(ImdbPage().url)
            assert self.driver.current_url == ImdbPage().url
            print("Success: IMDB Page URL is verified")
        except WebDriverException as e:
            print(e)

    #To search the page
    def test_name_search(self, booting_function):
        try:
            self.driver.get(ImdbPage().url)
            #To scroll this page for skip the ad using javascript scrollBy
            self.driver.execute_script('window.scrollBy(0,500)')

            #enter datas in textboxes

            #To click the expand button
            expand_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, Locators().expand_button_locator)))
            expand_button.click()

            #name of the actor
            name = self.wait.until(EC.presence_of_element_located((By.NAME, Locators().name_locator)))
            name.send_keys(ImdbPage().name)

            #birthdate
            start_birthdate = self.wait.until(
                EC.presence_of_element_located((By.NAME, Locators().start_birthdate_locator)))
            start_birthdate.send_keys(ImdbPage().start_birthdate)
            end_birthdate = self.wait.until(EC.presence_of_element_located((By.NAME, Locators().end_birthdate_locator)))
            end_birthdate.send_keys(ImdbPage().end_birthdate)

            self.driver.execute_script('window.scrollBy(0,500)')

            #gender
            gender = self.wait.until(EC.element_to_be_clickable((By.XPATH, Locators().gender_locator)))
            #Gender.click()

            #if click is not working then use javascript click
            self.driver.execute_script("arguments[0].click();", gender)

            #results
            result_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, Locators().result_button_locator)))
            result_button.click()

            assert self.driver.current_url == ImdbPage().current_url
            print("Success :The relevant detail is searched with implicit wait and details {a},{b},{c}".format(a=ImdbPage().name,b=ImdbPage().start_birthdate,c=ImdbPage().end_birthdate))

        except NoSuchElementException as e:
            print(e)
