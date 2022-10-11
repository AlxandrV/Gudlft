from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import time
import server


class TestFunctional:

    BASE_PATH = 'http://127.0.0.1:5000'
    DRIVER_PATH = 'tests/functional/chromedriver.exe'

    def test_complete_booking_scenario(self):
        competitions = server.loadCompetitions()
        clubs = server.loadClubs()
        competition = [competition for competition in competitions if competition['name'] == 'Test competitions'][0]
        places_before = competition['numberOfPlaces']
        club = [club for club in clubs if club['email'] == 'admin@test.com'][0]
        points_before = club['points']
        places = 3
        points_per_places = 3

        # Driver
        self.browser = webdriver.Chrome(service=Service(self.DRIVER_PATH))
        self.browser.get(self.BASE_PATH)

        # Scenario
        time.sleep(2)
        self.browser.find_element(By.XPATH, "//input[@type='email']").send_keys(club['email'])
        time.sleep(1)
        self.browser.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        self.browser.find_element(By.XPATH, f"//ul/li[contains(text(), \"{competition['name']}\")]/a").click()
        time.sleep(1)
        self.browser.find_element(By.XPATH, "//input[@type='number']").send_keys(places)
        time.sleep(1)
        self.browser.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)

        # Assert
        points_after = int(points_before) - places * points_per_places
        places_after = int(places_before) - places
        assert f"Points available: {points_after}" in self.browser.find_element(By.TAG_NAME, 'body').text
        assert f"Number of Places: {places_after}" in self.browser.find_element(By.XPATH, f"//ul/li[contains(text(), \"{competition['name']}\")]").text

        self.browser.find_element(By.XPATH, "//a[@href='/logout']").click()
        assert self.browser.find_element(By.XPATH, '//h1[text()="Welcome to the GUDLFT Registration Portal!"]')

        # Board view
        time.sleep(2)
        self.browser.find_element(By.XPATH, "//a[@href='/board']").click()
        assert self.browser.find_element(By.XPATH, f"//tr/td[text()='{club['name']}']//following-sibling::td[text()='{points_after}']")
        time.sleep(2)

        self.browser.close()