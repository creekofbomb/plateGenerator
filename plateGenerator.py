from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import itertools
import string
import csv
from datetime import datetime


class DMVLicensePlateBot:
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.csv_filename = self.init_csv_file()
    
    def init_csv_file(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f'available_plates_{timestamp}.csv'
        self.csv_filename = filename
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Available plates in Virginia"])
        return filename

    def write_to_csv(self, plate):
        with open(self.csv_filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([plate])

    def navigate_to_license_plate_search(self):
        self.browser.get('https://www.dmv.virginia.gov/vehicles/license-plates/search')

    def select_license_plate_category(self):
        search = self.browser.find_element(By.CSS_SELECTOR, '#block-plate-category > div > div > select')
        search.click()
        college = self.browser.find_element(By.CSS_SELECTOR, '#block-plate-category > div > div > select > option:nth-child(3)')
        college.click()

    def search_for_plate(self, keyword):
        gmu = self.browser.find_element(By.CSS_SELECTOR, '#edit-keyword')
        gmu.send_keys(keyword)
        gmu.send_keys(Keys.ENTER)
        sleep(3)

    def click_on_plate_link(self):
        link = self.browser.find_element(By.XPATH, '//*[@id="content-main"]/div/div/div[3]/div[1]/a')
        self.browser.execute_script("arguments[0].scrollIntoView();", link)
        sleep(1)
        link.click()

    def navigate_to_buy_plate_page(self):
        buy = self.browser.find_element(By.CSS_SELECTOR, '#content-main > div.c-plate-header > div > div.c-plate-header__content > a:nth-child(2)')
        buy.click()
        sleep(1)

    def switch_to_plate_frame(self):
        self.browser.switch_to.frame(self.browser.find_element(By.CSS_SELECTOR, "html > frameset > frameset > frameset > frame:nth-child(4)"))

    def enter_plate_details(self,combo):
        box_selectors = [
            f"body > table > tbody > tr > td > table:nth-child(2) > tbody > tr:nth-child(19) > td:nth-child(2) > table > tbody > tr > td:nth-child({i}) > input[type=text]"
            for i in range(1, 7)
        ]
        
        for selector, char in zip(box_selectors, combo):
            box = self.browser.find_element(By.CSS_SELECTOR, selector)
            box.send_keys(char)

        submit = self.browser.find_element(By.CSS_SELECTOR, "body > table > tbody > tr > td > table:nth-child(2) > tbody > tr:nth-child(19) > td:nth-child(2) > table > tbody > tr > td:nth-child(7) > input[type=button]:nth-child(2)")
        submit.click()

        message = self.browser.find_element(By.CSS_SELECTOR, "body > table > tbody > tr > td > table:nth-child(2) > tbody > tr:nth-child(1) > td:nth-child(1) > font")
        if message.text == 'Congratulations. The message you requested is available.':
            available_plate = ''.join(combo)      
            print(f'Plate {available_plate} is available')
            self.write_to_csv(available_plate)
            clear = self.browser.find_element(By.CSS_SELECTOR, "body > table > tbody > tr > td > table:nth-child(2) > tbody > tr:nth-child(20) > td:nth-child(2) > table > tbody > tr > td:nth-child(7) > input[type=button]:nth-child(1)")
            clear.click()
        else:
            clear = self.browser.find_element(By.CSS_SELECTOR, "body > table > tbody > tr > td > table:nth-child(2) > tbody > tr:nth-child(20) > td:nth-child(2) > table > tbody > tr > td:nth-child(7) > input[type=button]:nth-child(1)")
            clear.click()

    def generate_and_test_plates(self):
        possible_characters = string.ascii_lowercase + string.digits + '- &'
        password_length = 6
        combinations = itertools.product(possible_characters, repeat=password_length)

        for combo in combinations:
            self.enter_plate_details(combo)
            
    def close_browser(self):
        self.browser.quit()

# Create an instance of the DMVLicensePlateBot class
if __name__ == "__main__":
    # Create an instance of the DMVLicensePlateBot class
    bot = DMVLicensePlateBot()
    bot.navigate_to_license_plate_search()
    bot.select_license_plate_category()
    bot.search_for_plate('George Mason University')
    bot.click_on_plate_link()
    bot.navigate_to_buy_plate_page()
    bot.switch_to_plate_frame()
    bot.generate_and_test_plates()


