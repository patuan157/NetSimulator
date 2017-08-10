from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *

import pyautogui as mouse
import random
import time
import logging
import platform

from bots.constant import Constant
from bots.script import Script


class SurfFacebook(object):
    def __init__(self, browser, keyword=None):
        self.browser = browser
        self.url = Constant.FACEBOOK_URL
        self.keyword = keyword if keyword is not None else None

        self.toolbarHeight = 0
        self.number_of_articles = 0             # Number of Article (update everytime we scroll down more)
        self.liked_article = 0                  # Limit Number of Like article
        self.shared_article = 0                 # Limit Number of Share article
        mouse.FAILSAFE = False

    def start_session(self):
        # Set up Toolbar height for browser
        self.calculate_browser_toolbar()

        logging.info(" Session Keywords : " + str(self.keyword))
        logging.info(" Go to " + self.url)
        # Start Session By Log in Facebook
        try:
            self.browser.get(self.url)
        except TimeoutException:
            self.browser.execute_script(Script.STOP_LOADING_SCRIPT)
            logging.info(" Unable To Fully Load Page")
        time.sleep(1)
        self.log_in()

        # Move to New Feed to Like and Share Article
        self.go_to_new_feed()
        for i in range(2):
            self.scroll_through_page()          # Scroll More than 1 time ?
            self.like_and_share_article()       # New Article appears
            time.sleep(5)

        # Randomly Add Friend. Change SEARCH_FRIEND_KEYWORD to change name you want to search
        self.add_friend()
        logging.info(" Find Friend with Keyword : " + Constant.SEARCH_FRIEND_KEYWORD)

        # Finish Session
        logging.info(" Finish Session. Liked "
                     + str(self.liked_article)
                     + " articles and Share "
                     + str(self.shared_article)
                     + " articles")
        self.browser.quit()

    def calculate_browser_toolbar(self):
        if platform.system() == "Darwin":               # Mac OS toolbar
            # MacOS Toolbar for Firefox
            if self.browser.capabilities["browserName"] == 'firefox':
                self.toolbarHeight = self.browser.execute_script(Script.GET_MAC_FIREFOX_TOOLBAR_HEIGHT_SCRIPT)
            # Mac OS Toolbar for Chrome
            else:
                self.toolbarHeight = self.browser.execute_script(Script.GET_MAC_TOOLBAR_HEIGHT_SCRIPT)
        # Window Toolbar in general
        elif platform.system() == "Windows":            # Window toolbar on browser
            self.toolbarHeight = self.browser.execute_script(Script.GET_WINDOW_TOOLBAR_HEIGHT_SCRIPT)

    def log_in(self):
        try:
            time.sleep(0.5)
            email = self.browser.find_element(By.ID, "email")
            self.mouse_visualize(email)
            email.send_keys(Constant.FACEBOOK_LOGIN_EMAIL)

            password = self.browser.find_element(By.ID, "pass")
            self.mouse_visualize(password)
            password.send_keys(Constant.FACEBOOK_LOGIN_PASS)

            log_in_button = self.browser.find_element(By.ID, "loginbutton")
            self.mouse_visualize(log_in_button)
            log_in_button.click()
            logging.info(" Logged in with User " + Constant.FACEBOOK_LOGIN_EMAIL)
        except NoSuchElementException:
            print(" Can't Find Field To Login")

    def go_to_new_feed(self):
        """
        Avoid Going anywhere else other than New Feed
        Go Back To Home New Feed
        """
        try:
            time.sleep(0.5)
            home_button = self.browser.find_element(By.XPATH, "//*[text() = 'Home']")
            self.mouse_visualize(home_button)
            home_button.click()
            logging.info(" Move To New Feed ")
        except NoSuchElementException:
            print(" Can't Find Home Button")

    def scroll_through_page(self):
        """
        # First Time Scroll through Facebook
        # print("Scrolling Through Page")
        scroll_sequence = random.choice(Constant.PAGE_SCROLL_SEQUENCE)
        for action in scroll_sequence:
            if action == "D":
                time.sleep(2)
                ActionChains(self.browser).send_keys(Keys.PAGE_DOWN).perform()
            elif action == "U":
                time.sleep(2)
                ActionChains(self.browser).send_keys(Keys.PAGE_UP).perform()
        """
        # Keep Scroll Down Facebook for more article appear
        logging.info(" Scroll Down ")
        for i in range(6):
            time.sleep(2)
            ActionChains(self.browser).send_keys(Keys.PAGE_DOWN).perform()

    def like_and_share_article(self):
        """
        Like and Share some article
        """
        list_article = self.get_list_article()
        number_of_new_articles = len(list_article) - self.number_of_articles
        logging.info(" " + str(number_of_new_articles) + " new articles appear")
        if self.keyword is None:
            # No keyword specify which article to target.
            # Randomly choose half of them?
            choose_article = random.sample(list_article[self.number_of_articles: len(list_article)],
                                           number_of_new_articles//2 + 1)
            logging.info(" Randomly Like and Share some articles ")
        else:
            # Have Keyword. Choose Article accordingly (consider all of them)
            choose_article = list_article[self.number_of_articles: len(list_article)]
            logging.info(" Like and Share articles according to Keyword")

        for article in choose_article:
            self.like_article(article)
            self.share_article(article)

    def get_list_article(self):
        """
        Return List article from New Feed
        """
        time.sleep(1)
        list_article = self.browser.execute_script(Script.GET_FACEBOOK_LIST_ARTICLES)
        return list_article

    def like_article(self, article):
        if self.keyword is None:
            try:
                like_button = self.browser.execute_script(Script.GET_LIKE_BUTTON, article)
                if like_button.is_displayed():
                    if random.random() < 0.4:       # Chance to randomly like an article?
                        # Scroll Article to middle of screen
                        self.browser.execute_script(Script.SCROLL_ELEMENT_INTO_MIDDLE_SCRIPT, like_button)
                        self.mouse_visualize(like_button)
                        mouse.click()
                        self.liked_article += 1
                        time.sleep(1)
            except WebDriverException:
                pass
        else:
            if self.is_keyword_appear(article):
                try:
                    like_button = self.browser.execute_script(Script.GET_LIKE_BUTTON, article)
                    if like_button.is_displayed():
                        self.browser.execute_script(Script.SCROLL_ELEMENT_INTO_MIDDLE_SCRIPT, like_button)
                        self.mouse_visualize(like_button)
                        mouse.click()
                        self.liked_article += 1
                        time.sleep(1)
                except WebDriverException:
                    pass

    def share_article(self, article):
        if self.keyword is None:
            try:
                share_button = self.browser.execute_script(Script.GET_SHARE_BUTTON, article)
                if share_button.is_displayed():
                    if random.random() < 0.25:      # Chance to randomly share an article
                        self.browser.execute_script(Script.SCROLL_ELEMENT_INTO_MIDDLE_SCRIPT, share_button)
                        self.mouse_visualize(share_button)
                        mouse.click()
                        mouse.typewrite("Now")          # Share Now Option
                        time.sleep(1)
                        mouse.press("enter")            # Confirm Sharing
                        time.sleep(5)                   # Some Delay to confirm sharing
                        self.shared_article += 1
            except WebDriverException:
                pass
        else:
            if self.is_keyword_appear(article):
                share_button = self.browser.execute_script(Script.GET_SHARE_BUTTON, article)
                try:
                    if share_button.is_displayed():
                        self.browser.execute_script(Script.SCROLL_ELEMENT_INTO_MIDDLE_SCRIPT, share_button)
                        self.mouse_visualize(share_button)
                        mouse.click()
                        mouse.typewrite("Now")
                        time.sleep(1)
                        mouse.press("enter")
                        time.sleep(5)
                        self.shared_article += 1
                except WebDriverException:
                    pass

    def is_keyword_appear(self, article):
        try:
            article_author = self.browser.execute_script(Script.GET_AUTHOR_OF_ARTICLE, article)
            article_content = self.browser.execute_script(Script.GET_ARTICLE_CONTENT, article)
        except WebDriverException:
            return False

        length_keyword = len(self.keyword)
        keyword_str = self.keyword[1:length_keyword-1]
        list_keyword = keyword_str.split(",")
        for keyword in list_keyword:
            keyword = keyword.replace("-", " ")
            if keyword.lower() in article_author.lower() or keyword.lower() in article_content.lower():
                return True

        return False

    def add_friend(self):
        self.browser.execute_script("document.body.scrollTop = 0")  # Scroll Back to Top for visible searh bar
        time.sleep(2)
        try:
            search_box = self.browser.execute_script("return document.querySelector('input._1frb')")
            self.mouse_visualize(search_box)
            mouse.click()
            time.sleep(1)
            search_box.send_keys(Constant.SEARCH_FRIEND_KEYWORD)
            mouse.press('enter')

            time.sleep(10)          # Loading To Friend Search with List of friends
            friend_box = self.browser.execute_script("return document.getElementsByClassName('_5w7z _5w81')[0]")
            extend_buttons = self.browser.execute_script("return arguments[0].getElementsByClassName('_5w9f')",
                                                         friend_box)
            # Extend List Friend for more options?
            for button in extend_buttons:
                if button.is_displayed():
                    self.mouse_visualize(button)
                    time.sleep(1)
                    button.click()
                    break
            # Move mouse a bit to avoid Hover some friend
            mouse.moveRel(100, 0)
            # Add Friend Button visualize
            time.sleep(2)
            add_friend_buttons = self.browser.execute_script(
                "return arguments[0].getElementsByClassName('FriendButton')", friend_box)
            for button in add_friend_buttons:
                if button.is_displayed():
                    self.mouse_visualize(button)        # Hover The Button
                    time.sleep(1)

            time.sleep(3)
        except WebDriverException:
            print("Error Here")
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
