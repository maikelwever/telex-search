from telegrambot import plugin
import requests
import json
from bs4 import BeautifulSoup

class SearchPlugin(plugin.TelegramPlugin):
    """
    Search engines
    """

    patterns = {
        "^/google (.*)":"google",
        "^/duck (.*)": "duck",
    }

    usage = [
        "/google <query>: google search",
        "/duck <query>: duckduckgo",
    ]

    def __init__(self):
        super().__init__()


    def google(self, msg, matches):
        '''Returns the link and the description of the first result from a google search
        '''
        query = matches.group(1)
        params = {
            'q': query,
        }
        response = requests.get('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&', params = params).text
        jresults = json.loads(response)
        results = jresults['responseData']['results']
        returnval=""
        for result in results:
            title = result['title']
            url = result['url']
            title=title.translate({ord(k):None for k in u'<b>'})
            title=title.translate({ord(k):None for k in u'</b>'})
            returnval += title + ' ; ' + url + '\n'
        return returnval

    def duck(self, msg, matches):
        '''Returns results of a DDG search'''
        query = matches.group(1)
        params = {
            'q': query,
        }
        response = requests.post('https://duckduckgo.com/html/', params = params).text
        soup = BeautifulSoup(response)
        links = soup.findAll('div', {"class": "links_main links_deep"})
        reply = "DuckDuckGo results for %s\n" % query
        for link in links[:7]:
            title = link.a.text.replace("<b>","").replace("</b>","")
            url = link.a['href']
            # snippet = link.div.text.replace("<b>","").replace("</b>","")
            reply += "%s ~ %s\n" % (title, url)
        return reply
