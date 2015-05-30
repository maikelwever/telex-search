import plugintypes
import tgl
from telegrambot.utils.decorators import group_only
import requests
from bs4 import BeautifulSoup


class SearchPlugin(plugintypes.TelegramPlugin):
    """
    Search engines
    """

    patterns = {
        "^/google (.*)":"google",
    }

    usage = [
        "/google: google search",
    ]

    def __init__(self):
        super().__init__()


    @group_only
    def google(self, msg, matches):
