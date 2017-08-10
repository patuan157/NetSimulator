"""
Short Javascript the browser will use across the application
"""


class Script(object):
    """
    Script Object
    """
    # Scroll any element to the middle of the ViewPort
    SCROLL_ELEMENT_INTO_MIDDLE_SCRIPT = "var viewPortHeight = Math.max(document.documentElement.clientHeight, " \
                                        + "window.innerHeight || 0);" \
                                        + "var elementTop = arguments[0].getBoundingClientRect().top;" \
                                        + "window.scrollBy(0, elementTop-(viewPortHeight/2));"

    # Window Toolbar Height
    GET_WINDOW_TOOLBAR_HEIGHT_SCRIPT = "return window.outerHeight - window.innerHeight"

    # MAC Toolbar Height Chrome
    GET_MAC_TOOLBAR_HEIGHT_SCRIPT = "return window.outerHeight - window.innerHeight + window.screenTop"

    # MAC Toolbar Height Firefox
    GET_MAC_FIREFOX_TOOLBAR_HEIGHT_SCRIPT = "return window.outerHeight - window.innerHeight + window.screenY"

    # Stop Browser Loading After Timeout occurs
    STOP_LOADING_SCRIPT = "window.stop();"

    # CNN Facebook Share Button
    GET_CNN_FACEBOOK_SHARE_BUTTON_SCRIPT = "return document.getElementsByClassName('gig-button-container-facebook');"

    # CNN Money site Facebook Share Button
    GET_CNN_MONEY_FACEBOOK_SHARE_BUTTON_SCRIPT = "return document.getElementsByClassName('js-share-fb')"

    # BBC Facebook Share Button
    GET_BBC_FACEBOOK_SHARE_BUTTON_SCRIPT = "return document.getElementsByClassName" \
                                           "('twite__channel-out twite__channel--facebook " \
                                           "twite__channel-click-extracted--facebook');"

    # FACEBOOK Javascript stuff
    GET_FACEBOOK_LIST_ARTICLES = "return document.getElementsByClassName('fbUserContent _5pcr')"

    GET_AUTHOR_OF_ARTICLE = "return arguments[0].getElementsByClassName('_5pbw _5vra')[0].textContent"

    GET_ARTICLE_CONTENT = "return arguments[0].getElementsByClassName('_5pbx userContent')[0].textContent"

    GET_LIKE_BUTTON = "return arguments[0].getElementsByClassName('_1mto')[0]"

    GET_COMMENT_BUTTON = "return arguments[0].getElementsByClassName('_1mto')[1]"

    GET_SHARE_BUTTON = "return arguments[0].getElementsByClassName('_1mto')[2]"


