import time
import logging

from bots.constant import Constant
from bots.profile import Profile
from bots.autoreg.reg_common import RegCommon as Registration
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import Select


class RegFacebook(Registration):
    def __init__(self, browser):
        Registration.__init__(self, browser, Constant.FACEBOOK_URL)

    def start(self):
        """
        Start the auto registration for Facebook
        No Need to check for agreement here
        """
        Registration.calculate_browser_toolbar(self)
        logging.info(" Operation : Register Facebook Account")
        try:
            self.browser.get(self.url)
            logging.info(" Website URL : " + self.url)
        except TimeoutException:
            logging.error(" Unable To Fully Load Page")

        try:
            reg_form = self.browser.find_element_by_id("reg")
            self.handle_text_input(reg_form)
            self.choose_birth_day(reg_form)
            self.choose_gender(reg_form)
            self.submit_form(reg_form)
            time.sleep(5)
            self.browser.quit()
        except NoSuchElementException:
            pass

    def choose_birth_day(self, form):
        """
        All Field in Birth-day is a drop-down menu
        We locate by Id Specific for Facebook form
        """
        birth_day = form.find_element_by_id("day")
        self.mouse_visualize(birth_day)
        Select(birth_day).select_by_value(Profile.BIRTHDAY)
        # birth_day.send_keys(Profile.BIRTHDAY)
        """
        ActionChains(self.browser).move_to_element(birth_day).click() \
            .send_keys(Profile.BIRTHDAY) \
            .send_keys(Keys.ENTER) \
            .perform()
        """
        logging.info(" Choose drop-down menu : BirthDay : " + Profile.BIRTHDAY)

        birth_month = form.find_element_by_id("month")
        self.mouse_visualize(birth_month)
        Select(birth_month).select_by_value(Profile.BIRTH_MONTH_N)
        # birth_month.send_keys(Profile.BIRTH_MONTH_S)
        """
        ActionChains(self.browser).move_to_element(birth_month).click() \
            .send_keys(Profile.BIRTH_MONTH_S) \
            .send_keys(Keys.ENTER) \
            .perform()
        """
        logging.info(" Choose drop-down menu : BirthMonth : " + Profile.BIRTH_MONTH_S)

        birth_year = form.find_element_by_id("year")
        self.mouse_visualize(birth_year)
        Select(birth_year).select_by_value(Profile.BIRTH_YEAR)
        # birth_year.send_keys(Profile.BIRTH_YEAR)
        """
        ActionChains(self.browser).move_to_element(birth_year).click() \
            .send_keys(Profile.BIRTH_YEAR) \
            .send_keys(Keys.ENTER) \
            .perform()
        """
        logging.info(" Choose drop-down menu : BirthYear : " + Profile.BIRTH_YEAR)
