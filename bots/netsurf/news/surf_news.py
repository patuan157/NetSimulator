import abc


class SurfNews(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def start_session(self):
        """
        Start The New Surfing Session
        """

    @abc.abstractclassmethod
    def choose_next_action(self):
        """
        Consider Next Action : Go Back or Move to another Page
        """

    @abc.abstractclassmethod
    def choose_next_link(self):
        """
        Move to another Page by choose a new link
        """

    @abc.abstractclassmethod
    def get_list_link(self):
        """
        Return list link (<a href=>) on page
        """

    @abc.abstractclassmethod
    def go_back(self):
        """
        Go Back 1 Page
        """

    @abc.abstractclassmethod
    def mouse_visualize(self, element):
        """
        Scroll Mouse to the choosen element as Visualization
        """
