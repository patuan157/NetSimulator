import sys
import os
from datetime import datetime

from bots.autoreg.reg_common import RegCommon
from bots.autoreg.reg_google import RegGoogle
from bots.autoreg.reg_facebook import RegFacebook

from bots.netsurf.news.surf_cnn import *
from bots.netsurf.news.surf_bbc import *
from bots.netsurf.social_media.surf_facebook import *


# Set Up Chrome or Firefox Browser
def set_up_webdriver(type_browser):
    from selenium import webdriver
    if type_browser.lower() == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        browser = webdriver.Chrome(chrome_options=options)
        # Bring New opened browser in front
        current_window = browser.current_window_handle
        browser.switch_to_window(current_window)

    else:
        profile = webdriver.FirefoxProfile()
        browser = webdriver.Firefox(firefox_profile=profile, log_path=os.devnull)

    return browser


# Set Up Window or Mac OS
def set_up_webdriver_os_dependent(browser):
    if platform.system() == "Darwin":                   # Mac OS Specific Browser position set-up
        window_size = mouse.size()
        browser.set_window_position(0, 0)
        browser.set_window_size(window_size[0], window_size[1])

    browser.set_page_load_timeout(60)
    time.sleep(2)
    return browser


# Start new Log File depend on the task
def start_log_file(task, type_browser, target):
    current_working_dir = os.getcwd()
    start_time = datetime.now().strftime('%Y%m%d%H%M%S')

    # Create a Logging File
    if "reg" in task.lower():
        logging.basicConfig(filename=(current_working_dir + "/logs/" + start_time + "-Registration" + target + ".log"),
                            level=logging.INFO)
        logging.info(" ******* " + datetime.now().strftime('%m/%d/%Y %I:%M:%S %p') + " : Program Start ********")
        logging.info(" Browser : " + type_browser.upper())
    elif "surf" in task.lower():
        logging.basicConfig(filename=(current_working_dir + "/logs/" + start_time + "-Surfing" + target + ".log"),
                            level=logging.INFO)
        logging.info(" ******* " + datetime.now().strftime('%m/%d/%Y %I:%M:%S %p') + " : Program Start ********")
        logging.info(" Browser : " + type_browser.upper())

    # logging.info(" Operation : Register Account")


# End Log File
def end_log_file():
    logging.info(" ******** " + datetime.now().strftime('%m/%d/%Y %I:%M:%S %p') + " : Program End *********")


# Entry of the Application
def main():
    # Pass enough arguments to run
    if len(sys.argv) != 4 and len(sys.argv) != 7:
        print("Make sure you have 4 arguments or 7 argument on Command.")
        exit(0)
    else:
        # Take passing argument for some needed variable
        browser_type = sys.argv[1]
        operation = sys.argv[2]
        pages = sys.argv[3]

        if 'chrome' not in browser_type.lower() and 'firefox' not in browser_type.lower():
            print("Please use Chrome or Firefox browser")
            exit(0)
        else:
            # Valid arugment => Set up Browser
            driver = set_up_webdriver(browser_type)

            driver = set_up_webdriver_os_dependent(driver)

            # Registration Task
            if "reg" in operation.lower():
                # Bots for Register Account
                if "google" in pages.lower():           # Google Reg Bot
                    start_log_file("reg", browser_type, "Google")
                    reg = RegGoogle(browser=driver)
                elif "facebook" in pages.lower():       # Facebook Reg Bot
                    start_log_file("reg", browser_type, "Facebook")
                    reg = RegFacebook(browser=driver)
                else:                                   # Other Reg Bot
                    start_log_file("reg", browser_type, "")
                    reg = RegCommon(browser=driver, url=pages)
                reg.start()

                end_log_file()
            # Net Surfing Task
            elif "surf" in operation.lower():
                # Bots for Net Surfing. Addition Arguments
                category = None if sys.argv[4] == "None" else sys.argv[4]
                keyword = None if sys.argv[5] == "None" else sys.argv[5]
                sharing = bool(sys.argv[6] == "Yes")
                # Bot to go CNN
                if "CNN" in pages:
                    start_log_file("surf", browser_type, "CNN")
                    bots = SurfCnn(browser=driver, category=category, keyword=keyword, allow_share_article=sharing)
                    bots.start_session()
                    # print("Surf CNN in Category " + str(category) + " focus on " + keyword)
                # Bot to go BBC
                elif "BBC" in pages:
                    start_log_file("surf", browser_type, "BBC")
                    bots = SurfBbc(browser=driver, category=category, keyword=keyword, allow_share_article=sharing)
                    bots.start_session()
                    # print("Surf BBC in Category " + str(category) + " focus on " + keyword)
                # Bot to go Facebook
                elif "Facebook" in pages:
                    start_log_file("surf", browser_type, "Facebook")
                    bots = SurfFacebook(browser=driver, keyword=sys.argv[5])
                    bots.start_session()
                    # print("Surf Facebook with Like and Share article")
                # Finish Log File
                end_log_file()
            else:                   # Break the program without correct Arguments
                print("Please pass Registration Or NetSurfing as Operation")
                driver.quit()
                exit(0)


if __name__ == "__main__":
    main()
