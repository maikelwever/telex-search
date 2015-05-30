import plugintypes
import tgl
from telegrambot.utils.decorators import group_only
import requests
import json

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
        '''Returns the link and the description of the first result from a google search
        '''
        #query = raw_input ( 'Query: ' )
        query=matches.group(1)
        # print "going to google %s" % query
        query = urllib.urlencode ( { 'q' : query } )
        params = {
            'q': query,
        }
        response = requests.get('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&', params = params).text
        jresults = json.loads ( response )
        results = jresults [ 'responseData' ] [ 'results' ]
        returnval=""
        for result in results:
            title = result['title']
            url = result['url']   # was URL in the original and that threw a name error exception
            #print ( title + '; ' + url )
            title=title.translate({ord(k):None for k in u'<b>'})
            title=title.translate({ord(k):None for k in u'</b>'})
            returnval += title + ' ; ' + url + '\n'

        return returnval
