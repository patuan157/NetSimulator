from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

import time
import logging
import platform
import pyautogui as mouse

from bots.script import Script
from bots.profile import Profile


class RegCommon(object):
    def __init__(self, browser, url):
        self.browser = browser
        self.toolbarHeight = 0
        self.url = url
        mouse.FAILSAFE = False
        mouse.PAUSE = 0.5

    def start(self):
        logging.info(" Operation : Register Account")
        self.calculate_browser_toolbar()
        try:
            self.browser.get(self.url)
            logging.info(" Website URL : " + self.url)
        except TimeoutException:
            logging.error(" Unable To Fully Load Page")

        try:
            reg_form = self.locate_form_root()
            self.handle_text_input(reg_form)
            self.choose_birth_day(reg_form)
            self.choose_gender(reg_form)
            self.accept_agreement(reg_form)
            self.submit_form(reg_form)
            time.sleep(5)
            self.browser.quit()
        except NoSuchElementException:
            self.browser.quit()

    def calculate_browser_toolbar(self):
        if platform.system() == "Darwin":               # Mac OS toolbar on browser
            if self.browser.capabilities["browserName"] == 'firefox':
                self.toolbarHeight = self.browser.execute_script(Script.GET_MAC_FIREFOX_TOOLBAR_HEIGHT_SCRIPT)
            else:
                self.toolbarHeight = self.browser.execute_script(Script.GET_MAC_TOOLBAR_HEIGHT_SCRIPT)
        elif platform.system() == "Windows":            # Window toolbar on browser
            self.toolbarHeight = self.browser.execute_script(Script.GET_WINDOW_TOOLBAR_HEIGHT_SCRIPT)

    def locate_form_root(self):
        """
        Assumption : Only 1 Registration Form in a page
        Across multiple form, If Form-Id focus on Keywords as "reg", "account-create", "signup", choose them
        If Not, Then the only form in the page SHOULD be the registration form without a clearly context
        """

        try:
            forms = self.browser.find_elements_by_tag_name("form")

            # Only 1 reg form in a page
            for form in forms:
                form_id = form.get_attribute("id").lower()

                id_focus = ("reg" in form_id) or ("signup" in form_id) or \
                           ("account" in form_id and "create" in form_id) or \
                           ("account" in form_id and "creation" in form_id)

                if id_focus:
                    return form

            if len(forms) == 1:
                return forms[0]

        except NoSuchElementException:
            logging.error(" Can't find Registration Form")

    def handle_text_input(self, form):
        """
        Collect all the Text Input Field to evaluate their context and fill them
        """
        text_inputs = form.find_elements_by_tag_name("input")
        # ["text", "password", "tel", "email"] is type for text input
        for text_field in text_inputs:
            if text_field.get_attribute("type") in ["text", "password", "tel", "email"]:
                input_type = text_field.get_attribute("type")
                input_name = text_field.get_attribute("name")
                try:
                    logging.info(" Enter "
                                 + input_type
                                 + " field : "
                                 + input_name
                                 + " - "
                                 + self.fill_text_input(text_field))
                except WebDriverException:
                    logging.error(input_type
                                  + " : "
                                  + input_name
                                  + " - UNKNOWN FIELD")

    def fill_text_input(self, text_field):
        """
        Fill The Text Field depends on the context of that input
        """
        input_name = text_field.get_attribute("name").lower()

        if "name" in input_name:
            if "first" in input_name:                               # First Name Field
                result = Profile.FIRST_NAME
            elif "last" in input_name or "sur" in input_name:       # Last Name or Sur Name Field
                result = Profile.LAST_NAME
            elif "user" in input_name or "account" in input_name:   # User Name or Account Name Field
                result = Profile.USERNAME
            elif "full" in input_name:                              # Full Name Field
                result = Profile.FULL_NAME
            else:                                                   # Only Name required
                result = Profile.FULL_NAME

        elif "mail" in input_name:
            result = Profile.EMAIL                                  # Email Field

        elif "passwd" in input_name or "password" in input_name:
            result = Profile.PASSWORD                               # Password and Re-enter Password Field

        elif "birth" in input_name:                                 # Birthday Input as Text Field
            if "month" in input_name:
                result = Profile.BIRTH_MONTH_S
            elif "year" in input_name:
                result = Profile.BIRTH_YEAR
            else:
                result = Profile.BIRTHDAY

        elif "sex" in input_name or "gender" in input_name:
            result = Profile.GENDER                                 # Gender Input as Text Field

        elif "phone" in input_name:                                 # Phone Number Field
            result = Profile.PHONE

        elif "captcha" in input_name:                               # Captcha, which can't be handle
            return "UNABLE TO FILL CAPTCHA"
        else:
            return "UNKNOWN FIELD"

        self.mouse_visualize(text_field)
        text_field.clear()
        text_field.send_keys(result)
        return result                                               # For Log

    def choose_birth_day(self, form):
        """
        Birth Day can be ask by
        Either Standard Text Input (cover in other Method)
        Or A Dropdown Menu (this Method)
        """
        try:
            select_menu = form.find_elements_by_tag_name("select")
            for menu in select_menu:
                menu_id = menu.get_attribute("id").lower()
                if "day" in menu_id:                                    # BirthDay
                    result = Profile.BIRTHDAY
                    self.mouse_visualize(menu)
                    menu.send_keys(result)
                    logging.info(" Choose drop-down menu - BirthDay - " + result)           # Write Logs
                elif "month" in menu_id:                                # BirthMonth
                    result = Profile.BIRTH_MONTH_S
                    self.mouse_visualize(menu)
                    menu.send_keys(result)
                    logging.info(" Choose drop-down menu - BirthMonth - " + result)         # Write Logs
                elif "year" in menu_id:                                 # BirthYear
                    result = Profile.BIRTH_YEAR
                    self.mouse_visualize(menu)
                    menu.send_keys(result)
                    logging.info(" Choose drop-down menu - BirthYear - " + result)          # Write Logs
                else:                                                   # Other Dropdown Menus might not be relevant
                    continue
        except WebDriverException:
            pass

    def choose_gender(self, form):
        """
        A Registration Form has 3 way to ask for Gender(Sex)
        Either Group Radion Button or Dropdown Menu (in this Method)
        Or A Standard Text Input (cover in other Method)
        """

        # Radio Buttons to choose Gender
        radio_buttons = form.find_elements_by_xpath("//input[@type='radio']")
        # The Context That Group Radio Button focus
        radio_buttons_name = []

        for button in radio_buttons:
            button_name = button.get_attribute("name").lower()
            if button_name != "" and button_name not in radio_buttons_name:
                radio_buttons_name.append(button_name)

        for name in radio_buttons_name:
            if "sex" in name or "gender" in name:
                sex = form.find_element_by_xpath("//*[text()='" + Profile.GENDER + "']")
                self.mouse_visualize(sex)
                ActionChains(self.browser).move_to_element(sex).click().perform()
                logging.info(" Choose Options : Gender - " + Profile.GENDER)

        # Drop-down Menu to Choose a Gender
        select_menus = form.find_elements_by_tag_name("select")

        for menu in select_menus:
            menu_id = menu.get_attribute("id").lower()
            if "sex" in menu_id or "gender" in menu_id:
                self.mouse_visualize(menu)
                menu.send_keys(Profile.GENDER)
                logging.info(" Choose drop-down menu - Gender - " + Profile.GENDER)

    def accept_agreement(self, form):
        """
        Accept Page Agreement to register an account
        Usually go on an Checkbox button
        """
        try:
            agree_btn = form.find_element_by_xpath("//input[@type='checkbox']")
            if "agree" in agree_btn.get_attribute("id").lower():
                self.mouse_visualize(agree_btn)
                agree_btn.click()
        except NoSuchElementException:
            pass

    def submit_form(self, form):
        """
        Find Button to submit Form : "Create An Account" , "Sign Up"
        In general form, it will be either a button or input with type='submit'
        More specific : We need to evaluate the text the button shows or its value to judge "Submit" button
        """
        try:
            list_btn1 = form.find_elements_by_xpath("//*[@type='submit']")
            list_btn2 = form.find_elements_by_tag_name("button")
            list_btn3 = form.find_elements_by_tag_name("input")
            list_btn = list_btn1 + list_btn2 + list_btn3
            for btn in list_btn:
                if btn.is_displayed():
                    log_in = "log in" in btn.get_attribute("value").lower() or "log in" in btn.text.lower()
                    condition = (btn.get_attribute("type") == 'submit' and not log_in) or \
                                ("sign up" in btn.get_attribute("value").lower()) or \
                                ("sign up" in btn.text.lower()) or \
                                ("create" in btn.get_attribute("value").lower() and "account" in btn.get_attribute(
                                    "value").lower()) or \
                                ("create" in btn.text.lower() and "account" in btn.text.lower())
                    if condition:
                        # print(btn.get_attribute("type") + " - " + btn.get_attribute("value") + " - " + btn.text)
                        self.mouse_visualize(btn)
                        break

        except NoSuchElementException:
            logging.error(" Special Submit Button")
            pass

    def mouse_visualize(self, element):
        """
        Move Mouse to Web Element
        """
        location = element.location_once_scrolled_into_view
        size = element.size

        # Screen Size Might Be Depend on Browser (and OS)
        if self.browser.capabilities['browserName'] == "chrome":
            on_screen_width = location["x"] + size["width"]/2
            on_screen_height = location["y"] + size["height"]/2 + self.toolbarHeight
        elif self.browser.capabilities["browserName"] == "firefox":
            on_screen_width = location["x"] + size["width"] / 2
            on_screen_height = location["y"] + size["height"]/2 +self.toolbarHeight
        else:
            return

        time.sleep(0.2)

        mouse.moveTo(on_screen_width, on_screen_height, duration=0.3)
