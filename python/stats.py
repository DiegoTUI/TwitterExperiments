import sys
import re
import json

# globals
languages = {}
nationalities = {}
places = {}

def lines(fp):
    print str(len(fp.readlines()))

def getWords(line):
    # get the json representation of the line
    try:
        tweetJson = json.loads(line)
    except:
        # line was not a json, return None
        return None
    # check if "text" is in the tweet
    if "text" in tweetJson:
        # isolate words
        words = re.findall(r"[\w']+", tweetJson["text"])
        # return lower case version of words
        return map(lambda line:line.lower(), words)
    # return None by default
    return None

def getScore(words):
    if words is None: return None
    score = 0
    for word in words:
        if word.encode('utf-8') in scores:
            score+=scores[word]
    return score

def process(tweet):
    language = tweet["lang"]
    userLocation = tweet["user"]["location"].encode("utf-8")
    place = tweet["place"]["country_code"]
    userName = tweet["user"]["screen_name"]
    if userName == "carmic":
        print "CHRIS!! - {0}".format(tweet["text"]) 
    if language in languages:
        languages[language] += 1
    else:
        languages[language] = 1
    if userLocation in nationalities:
        nationalities[userLocation] += 1
    else:
        nationalities[userLocation] = 1
    if place in places:
        places[place] += 1
    else:
        places[place] = 1

def main():
    total = 0;
    tweet_file = open(sys.argv[1])
    # iterate the tweets
    for line in tweet_file:
        try:
            tweetJson = json.loads(line)
        except:
            continue
        try:
            process(tweetJson)
            total += 1
        except:
            continue
        #print "{0} - {1}".format(tweetJson["place"]["full_name"].encode("utf-8"), tweetJson["lang"])
    # print the stuff
    print "**** TOTAL ****"
    print total
    print "**** LANGUAGES ****"
    sortedLanguages = sorted(languages, key=languages.get, reverse=True)
    for language in sortedLanguages:i
        print "{0} - {1}".format(language, languages[language])
    print "**** PLACES ****"
    sortedPlaces = sorted(places, key=places.get, reverse=True)
    for place in sortedPlaces:
        print "{0} - {1}".format(place, places[place])
    return
    sortedNationalities = sorted(nationalities, key=nationalities.get, reverse=True)
    print "**** Nationalities ****"
    for nationality in sortedNationalities:
        print "{0} - {1}".format(nationality, nationalities[nationality])

if __name__ == '__main__':
    main()