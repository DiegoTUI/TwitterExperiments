# add path for tests
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
import oauth2 as oauth
import urllib2 as urllib
from config.twitter import TwitterConfig
from util.http import HTTPResponseErrorProcessor

class LocationStream(object):
    "A class to start a Twitter Location Stream and dump it to an output."
    "Returns the twitter stream in text format"
    "It uses the Twitter API POST statuses/filter request - https://dev.twitter.com/docs/api/1.1/post/statuses/filter."
    "It requires a locations parameter to work."
    "Raises HTTPSError in the Twitter feed returns anything but 200"

    locations = None
    opener = None
    request = None

    def __init__(self, locations):
        "Inits the LocationStream with a location and an output."
        "The location should be a comma separated string defining a bounding box."
        "If the output is none, then stdout is used"
        "Otherwise, a file is created"

        self.locations = locations
        self._initOpenerDirector()

    def _initOpenerDirector(self):
        "Inits the opener director"
        # build the oauth tokens
        oauth_token = oauth.Token(key=TwitterConfig.access_token_key, secret=TwitterConfig.access_token_secret)
        oauth_consumer = oauth.Consumer(key=TwitterConfig.api_key, secret=TwitterConfig.api_secret)
        signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
        # create handler
        http_handler  = urllib.HTTPHandler(debuglevel = 0)
        https_handler = urllib.HTTPSHandler(debuglevel = 0)
        error_handler = HTTPResponseErrorProcessor()
        # create request
        self.request = oauth.Request.from_consumer_and_token(oauth_consumer,
                                                     token = oauth_token,
                                                     http_method = "POST",
                                                     http_url = TwitterConfig.url, 
                                                     parameters = [])
        self.request["locations"] = self.locations
        self.request.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)
        # create opener
        self.opener = urllib.OpenerDirector()
        self.opener.add_handler(http_handler)
        self.opener.add_handler(https_handler)
        self.opener.add_handler(error_handler)

    def start(self):
        "starts fetching data from twitter into de desired output"
        # launch request
        response = self.opener.open(TwitterConfig.url, self.request.to_postdata())
        # return response
        return response

    def stop(self):
        "stops fetching data from the twitter stream"
        self.opener.close()

###############################################
################ UNIT TESTS ###################
###############################################

class LocationStreamTests(unittest.TestCase):
    "LocationStream Unit Tests"

    from util.http import internet_on

    def test_wrong_url(self):
        restoreTwitterUrl = TwitterConfig.url
        TwitterConfig.url = "https://unexisting.web.url"
        try:
            LocationStream("randomLocations").start()
            self.fail("wrong url should raise an exception")
        except urllib.URLError:
            pass
        except Exception as exception:
            self.fail("wrong url raised the wrong exception: {0}".format(type(exception).__name__))
        # restore config url
        TwitterConfig.url = restoreTwitterUrl

    @unittest.skipIf(not(internet_on()), "irrelevant test if you are offline")
    def test_invalid_locations(self):
        from util.http import HTTPSError
        try:
            LocationStream("invalidLocations").start()
            self.fail("wrong locations should raise an exception")
        except HTTPSError:
            pass
        except Exception as exception:
            self.fail("wrong locations raised the wrong exception: {0}".format(type(exception).__name__))

    @unittest.skipIf(not(internet_on()), "irrelevant test if you are offline")
    def test_valid_query(self):
        import json
        from threading import Timer
        location_stream = LocationStream("-180,-90,180,90")
        response = location_stream.start()
        count = 0
        for tweet in response:
            self.assertGreater(len(tweet), 0, "valid request returned empty tweet")
            try:
                json.loads(tweet)
            except Exception as exception:
                self.fail("Tweet is not a valid JSON. Exception raised: {0}. Tweet: {1}".format(type(exception).__name__, tweet))
            count += 1
            if count > 5:
                break
        location_stream.stop()

if __name__ == '__main__':
    unittest.main()
