import urllib2 as urllib

class HTTPResponseErrorProcessor(urllib.HTTPErrorProcessor):
    "Checks the response for errors before returning it"

    def http_response(self, request, response):
        if (response.getcode() == 200):
            return response;
        raise HTTPError()
    def https_response(self, request, response):
        if (response.getcode() == 200):
            return response;
        raise HTTPSError()

class HTTPError(Exception):
    pass

class HTTPSError(Exception):
    pass

def internet_on():
    "Checks if there is a connection to the Internet"
    try:
        response = urllib.urlopen("http://www.google.com",timeout=5)
        return True
    except urllib.URLError as err: pass
    return False