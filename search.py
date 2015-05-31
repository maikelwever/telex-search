from telegrambot import plugin
import requests
import json

class SearchPlugin(plugin.TelegramPlugin):
    """
    Search engines
    """

    patterns = {
        "^/google (.*)":"google",
    }

    usage = [
        "/google <query>: google search",
    ]

    def __init__(self):
        super().__init__()


    @group_only
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
