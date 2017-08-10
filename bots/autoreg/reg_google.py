import time
import logging

from bots.constant import Constant
from bots.profile import Profile
from bots.autoreg.reg_common import RegCommon as Registration
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class RegGoogle(Registration):
    def __init__(self, browser):
        Registration.__init__(self, browser, Constant.GOOGLE_URL)

    def start(self):
        """
        Start the auto registration for Google
        No Need to check for agreement here
        An addition step when submit
        """
        Registration.calculate_browser_toolbar(self)
        logging.info(" Operation : Register Google Account")
        try:
            self.browser.get(self.url)
            logging.info(" Website URL : " + self.url)
        except TimeoutException:
            logging.error(" Unable To Fully Load Page")

        try:
            reg_form = self.browser.find_element_by_id("createaccount")
            self.handle_text_input(reg_form)
            self.choose_birth_day(reg_form)
            self.choose_gender(reg_form)
            self.submit_form(reg_form)
            time.sleep(5)
            logging.info(" Click Next Step")
            self.browser.quit()
        except NoSuchElementException:
            pass

    def choose_birth_day(self, form):
        """
        BirthDay and BirthYear will be handle as normal text input
        BirthMonth is special drop-down menu with "div" tag.
        """
        month = form.find_element_by_id("BirthMonth")
        self.mouse_visualize(month)
        ActionChains(self.browser).move_to_element(month).click()\
            .send_keys(Profile.BIRTH_MONTH_S)\
            .send_keys(Keys.ENTER)\
            .perform()
        logging.info(" Choose drop-down menu : BirthMonth - " + Profile.BIRTH_MONTH_S)

    def choose_gender(self, form):
        """
        Gender is special drop-down menu with "div" tag
        """
        gender = form.find_element_by_id("Gender")
        self.mouse_visualize(gender)
        ActionChains(self.browser).move_to_element(gender).click()\
            .send_keys(Profile.GENDER)\
            .send_keys(Keys.ENTER)\
            .perform()
        logging.info(" Choose drop-down menu : Gender - " + Profile.GENDER)

    def submit_form(self, form):
        """
        Locate Submit Button with Id Specific for Google form
        """
        submit_btn = form.find_element_by_id("submitbutton")
        self.mouse_visualize(submit_btn)

"""
if __name__ == "__main__":
    from selenium import webdriver
    driver = webdriver.Chrome()
    reg = GoogleReg(driver)
    reg.start()
"""