from telex import plugin
import requests
import json
from bs4 import BeautifulSoup
import duckduckgo as ddg

class SearchPlugin(plugin.TelexPlugin):
    """
    Search engines
    """

    patterns = {
        "^!google (.*)":"google",
        "^!duck (.*)": "duck",
        "^!ddg (.*)": "ddgia",
    }

    usage = [
        "!google <query>: google search",
        "!duck <query>: duckduckgo top result",
        "!duck 5 <query>: DDG top 5 results (upto 20)",
        "!ddg <query>: DDG instant answer",
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
        n = query.split()[0]
        try:
            n = min(20, int(n))  # will be later used to limit the results
            query = ''.join(query.split()[1:])
            if query == "":
                return "No, you go ask your math teacher."
        except ValueError:
            n = 1

        params = {
            'q': query,
        }
        response = requests.post('https://duckduckgo.com/html/', params = params).text
        soup = BeautifulSoup(response)
        links = soup.findAll('div', {"class": "links_main links_deep"})
        reply = "DuckDuckGo results for %s\n" % query
        for link in links[:n]:
            title = link.a.text.replace("<b>","").replace("</b>","")
            url = link.a['href']
            snippet = link.div.text.replace("<b>","").replace("</b>","")
            reply += "%s ~ %s\n" % (title, url)
            if n == 1:
                reply += snippet
        return reply

    def ddgia(self, msg, matches):
        '''Returns DDG instant answer'''
        query = matches.group(1)
        reply = ddg.get_zci(query)
        return reply
