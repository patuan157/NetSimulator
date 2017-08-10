from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException, \
    StaleElementReferenceException, NoSuchElementException

import pyautogui as mouse
import time
import random
import platform
import logging
import numpy as np

from bots.netsurf.news.surf_news import SurfNews
from bots.constant import Constant
from bots.script import Script


class SurfBbc(SurfNews):
    def __init__(self, browser, category=None, allow_share_article=None, keyword=None):
        self.browser = browser
        self.url = Constant.BBC_URL
        self.category = category if category is not None else None
        self.allow_share_article = allow_share_article if allow_share_article is not None else False
        self.keyword = keyword if keyword is not None else None

        self.domain = "bbc.com"                # Start Url Domain
        self.toolbarHeight = 0
        self.current_action = ""               # Either Go Back or Go Forward
        self.history_page = 0                  # You cant go back anywhere when start browser (Avoid Go Back when start)
        self.list_url_visited = []             # Avoid Going To same URL again
        self.number_of_pages_visited = 0       # Number of Page Visited
        mouse.FAILSAFE = False

    def start_session(self):
        # Random Number of Pages will be navigate
        number_of_page_will_visit = random.randint(Constant.MIN_PAGES_PER_SESSION, Constant.MAX_PAGES_PER_SESSION)
        # Set up Toolbar height for browser
        self.calculate_browser_toolbar()
        # Check if the session will start at any sub-pages
        self.check_session_sub_pages()
        logging.info(" Session Keywords : " + self.keyword)

        logging.info(" " + str(self.number_of_pages_visited + 1) + ". Navigating " + self.url)         # Log
        while self.number_of_pages_visited < number_of_page_will_visit:
            if self.current_action != "GoBack":
                try:
                    self.browser.get(self.url)
                except TimeoutException:
                    self.browser.execute_script(Script.STOP_LOADING_SCRIPT)
                    logging.info(" Unable To Fully Load Page")
            else:
                self.go_back()
            try:
                time.sleep(1)           # Delay
                self.number_of_pages_visited += 1
                self.scroll_through_page()
                self.share_article()
                self.choose_next_action()
            except WebDriverException:
                continue

        logging.info(" Finish Session. Visited " + str(self.number_of_pages_visited) + " pages")
        self.browser.quit()

    def calculate_browser_toolbar(self):
        if platform.system() == "Darwin":               # Mac OS toolbar on browser
            if self.browser.capabilities["browserName"] == 'firefox':
                self.toolbarHeight = self.browser.execute_script(Script.GET_MAC_FIREFOX_TOOLBAR_HEIGHT_SCRIPT)
            else:
                self.toolbarHeight = self.browser.execute_script(Script.GET_MAC_TOOLBAR_HEIGHT_SCRIPT)
        elif platform.system() == "Windows":            # Window toolbar on browser
            self.toolbarHeight = self.browser.execute_script(Script.GET_WINDOW_TOOLBAR_HEIGHT_SCRIPT)

    def check_session_sub_pages(self):
        if self.category == "News":
            self.url = Constant.BBC_NEWS_URL
        elif self.category == "Sport":
            self.url = Constant.BBC_SPORT_URL
        elif self.category == "Travel":
            self.url = Constant.BBC_TRAVEL_URL
        elif self.category == "Weather":
            self.url = Constant.BBC_WEATHER_URL
        elif self.category == "Earth":
            self.url = Constant.BBC_EARTH_URL

    def choose_next_action(self):
        """
        Either Go Back or Choose a Random Link to navigate Next
        If the history Page is the start_url then only go forward options
        """

        # Random Choice with Numpy. Set up Probability as "Back" = 0.2 and "Forward" = 0.8
        random_choice = np.random.choice(["Back", "Forward"], 1, p=[0.2, 0.8])

        if self.history_page == 0 or random_choice[0] == 'Forward':
            self.current_action = "GoForward"
            self.choose_next_link()
        else:
            self.current_action = "GoBack"

    def choose_next_link(self):
        """
        Manage to choose next Page to navigate in the session
        Make Random decision for any url in current page
        """

        list_urls = self.get_list_link()

        # While loop to choose link in same domain
        while 1:
            # System Secure Random Method
            secure_random = random.SystemRandom()
            # Random a links and update instance's url
            url_element = secure_random.choice(list_urls)
            self.url = url_element.get_attribute("href")

            if self.url in self.list_url_visited:
                continue

            if self.is_link_in_same_domain():
                break

        # Locate and Visualize through mouse

        self.browser.execute_script(Script.SCROLL_ELEMENT_INTO_MIDDLE_SCRIPT, url_element)
        self.mouse_visualize(url_element)
        time.sleep(0.5)

        # Increase Counter for History_Page
        self.history_page += 1
        # Append the url will visit next. Next link to be choose shouldn't be in this list
        self.list_url_visited.append(self.url)
        logging.info(" " + str(self.number_of_pages_visited + 1) + ". Next Decision : Go to " + self.url)

    def share_article(self):
        if self.allow_share_article:
            facebook_share = self.browser.execute_script(Script.GET_BBC_FACEBOOK_SHARE_BUTTON_SCRIPT)
            if len(facebook_share) != 0:
                self.browser.execute_script("document.body.scrollTop = 0")  # Scroll Back to Top for visible share
                time.sleep(1)
                window_before = self.browser.current_window_handle
                for button in facebook_share:
                    if button.is_displayed():
                        self.mouse_visualize(button)
                        button.click()
                        break
                # New Tab will pop-up ask to share article to Facebook
                time.sleep(5)
                window_after = self.browser.window_handles[1]
                # Change to Pop-up window and Login Facebook
                self.browser.switch_to_window(window_after)
                try:
                    time.sleep(1)
                    self.browser.find_element_by_id("email").send_keys(Constant.FACEBOOK_LOGIN_EMAIL)
                    time.sleep(1)
                    self.browser.find_element_by_id("pass").send_keys(Constant.FACEBOOK_LOGIN_PASS)
                    time.sleep(1)
                    ActionChains(self.browser).send_keys(Keys.ENTER).perform()
                    logging.info(" Login Facebook")
                except NoSuchElementException:
                    # print("Already Login")
                    pass
                time.sleep(5)
                # Find Post Button and Post
                post_button = self.browser.find_element_by_xpath("//span[text()='Post to Facebook']")
                post_button.click()
                time.sleep(5)
                # Let the Post process and switch back to Main Tab
                self.browser.switch_to_window(window_before)
                time.sleep(3)
                logging.info(" Complete Sharing This Article")
            else:
                logging.info(" This site can't be share to Facebook")

    def is_link_in_same_domain(self):
        if self.category == "News":
            return self.domain in self.url and "news" in self.url
        elif self.category == "Sport":
            return self.domain in self.url and "sport" in self.url
        elif self.category == "Travel":
            return self.domain in self.url and "travel" in self.url
        elif self.category == "Weather":
            return self.domain in self.url and "weather" in self.url
        elif self.category == "Earth":
            return self.domain in self.url and "earth" in self.url
        else:
            return self.domain in self.url

    def go_back(self):
        """
        Go back 1 Page
        """
        logging.info(" " + str(self.number_of_pages_visited + 1) + ". Next Decision : Go Back 1 Page")
        try:
            self.browser.back()
        except WebDriverException:
            print("Going Back")
        time.sleep(1)

        self.url = self.browser.current_url
        self.history_page -= 1

    def get_list_link(self):
        # List Visible URL on current Page
        list_links = self.browser.find_elements_by_tag_name("a")
        # Remove duplicates URL and choose visible link
        list_urls = []

        if self.keyword is not None:              # Consider Topic when return list link
            for link in list_links:
                try:
                    href_attribute = link.get_attribute("href")
                    text_content = link.text
                    if href_attribute is not None:
                        if link not in list_urls and link.is_displayed() \
                                and self.is_keyword_appear(href_attribute, text_content):
                            list_urls.append(link)
                except StaleElementReferenceException:
                    continue

        if len(list_urls) > 0:                  # While more than 1 link relate to topic, return it
            return list_urls

        for link in list_links:                 # Or we will return a general list link anyway
            if link not in list_urls and link.is_displayed():
                list_urls.append(link)

        return list_urls

    def is_keyword_appear(self, url, text_content):
        length_keyword = len(self.keyword)
        keyword_str = self.keyword[1:length_keyword-1]
        list_keyword = keyword_str.split(",")
        for keyword in list_keyword:
            if keyword.lower() in url:
                return True

        for keyword in list_keyword:
            keyword = keyword.replace("-", " ")
            if keyword.lower() in text_content.lower():
                return True

        return False

    def scroll_through_page(self):
        """
        # Back up way to scroll
        print("Scrolling Through Page")
        scroll_sequence = random.choice(Constant.PAGE_SCROLL_SEQUENCE)
        for action in scroll_sequence:
            time.sleep(2)
            if action == "D":
                mouse.press('pagedown')
            else:
                mouse.press('pageup')
        """
        logging.info(" Scrolling Through Page")
        scroll_sequence = random.choice(Constant.PAGE_SCROLL_SEQUENCE)
        for action in scroll_sequence:
            if action == "D":
                time.sleep(2)
                ActionChains(self.browser).send_keys(Keys.PAGE_DOWN).perform()
            elif action == "U":
                time.sleep(2)
                ActionChains(self.browser).send_keys(Keys.PAGE_UP).perform()

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
