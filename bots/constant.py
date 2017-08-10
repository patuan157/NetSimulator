"""
Some Constants as Global Variable
Use across the Application
"""


class Constant(object):
    """
    Set Constants Variables
    """
    TESTURL = ["https://accounts.google.com/SignUp?hl=en-GB"
        , "http://facebook.com", "https://twitter.com/signup"
        , "https://www.instagram.com/accounts/emailsignup/?signupFirst=true"
        , "https://talent.stackoverflow.com/users/register"
        , "https://www.hackerrank.com/signup?utm_source=homepage&utm_medium=top_right&utm_content=green_signup&h_r=community_home&h_v=sign_up&h_l=header_right"
        , "https://store.steampowered.com/join/"]

    # Specific Registration URL (Social Media)
    GOOGLE_URL = "https://accounts.google.com/SignUp?hl=en-GB"
    FACEBOOK_URL = "http://facebook.com"
    TWITTER_URL = "https://twitter.com/signup"
    INSTAGRAM_URL = "https://www.instagram.com/accounts/emailsignup/?signupFirst=true"

    # Limit for a Surfing Session
    MIN_PAGES_PER_SESSION = 3
    MAX_PAGES_PER_SESSION = 5

    # Information To Login Facebook
    FACEBOOK_LOGIN_EMAIL = "clearlove.157@gmail.com"
    FACEBOOK_LOGIN_PASS = "Patuan1996"
    # Limit Like and Share an article?
    FACEBOOK_LIKED_ARTICLE_LIMIT = 7
    FACEBOOK_SHARED_ARTICLE_LIMIT = 4
    # Friend Keyword
    SEARCH_FRIEND_KEYWORD = "Anh Tuan Phan"

    # Some General Page Scroll Sequence
    PAGE_SCROLL_SEQUENCE = [["D", "D", "U", "D", "D", "D", "U"], ["D", "D", "D", "U", "U", "D", "D", "U"],
                            ["D", "U", "D", "D", "U", "D", "D"], ["D", "U", "D", "D", "D", "U", "D", "U"],
                            ["D", "D", "U", "D", "U", "D", "D"], ["D", "D", "U", "D", "D", "D", "U", "D"]]

    # CNN Sub_Page url
    CNN_URL = "http://edition.cnn.com/"
    CNN_OPINION_URL = "http://edition.cnn.com/opinions"
    CNN_SPORT_URL = "http://edition.cnn.com/sport"
    CNN_TRAVEL_URL = "http://edition.cnn.com/travel"
    CNN_STYLE_URL = "http://edition.cnn.com/style"
    CNN_MONEY_URL = "http://money.cnn.com/"
    CNN_HEALTH_URL = "http://edition.cnn.com/health"
    CNN_ENTERTAINMENT_URL = "http://edition.cnn.com/entertainment"
    CNN_TECHNOLOGY_URL = "http://money.cnn.com/technology/"

    # BBC Sub_Page url
    BBC_URL = "http://www.bbc.com/"
    BBC_NEWS_URL = "http://www.bbc.com/news"
    BBC_SPORT_URL = "http://www.bbc.com/sport"
    BBC_WEATHER_URL = "http://www.bbc.com/weather/"
    BBC_EARTH_URL = "http://www.bbc.com/earth/world"
    BBC_TRAVEL_URL = "http://www.bbc.com/travel/"

