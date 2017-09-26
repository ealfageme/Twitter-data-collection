import tweepy
import json
from py2neo import Graph
from py2neo.ogm import Property, GraphObject, RelatedTo


# Twitter keys
consumer_key = '5Xyt2JIpgCWsSboL4jqITlZCb'
consumer_secret = 'QdgAqnCTeChFurGOyPcGowJAZw5m6eQ14gyZpeaRFw3mQWpoEF'
access_token = '1924437534-ZnmL5AadDja6bFBkTCfczZLIfOvVbl6iil1ieqw'
access_token_secret = 'tw0PzDpTsSIbKZuGOxPqxNdCIOsxblUWfB1hCiSN8DAEi'

# graph instance
graph = Graph(password='password')
tx = graph.begin()

# Class node
class Tweet(GraphObject):
    __primarykey__ = "nick"
    text = Property()
    nick = Property()
    # associate_with = RelatedTo(Hastag)
    # written_by = RelatedTo(Author)


class Author(GraphObject):
    __primarykey__ = "nick"
    nick = Property()

class Hastag(GraphObject):
    __primarykey__ = "name"
    name = Property()




# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        tweetObject = Tweet()
        tweetObject.nick = decoded['user']['screen_name']
        tweetObject.text = decoded['text'].encode('ascii', 'ignore')

        graph.create(tweetObject)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        print ''
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':


    result = raw_input("Do you want delete the last search? (Y/N)? :")

    if (result == "Y") or (result == "y"):
        graph.delete_all()
        print 'The last search has been deleted'
    else:
        print 'The last searches are in database'

    # Main
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)


    name = raw_input("Hastag to search:")
    hastag = "#" + name
    print "Showing all new tweets for ", hastag

    # Create de node with the hastag
    has = Hastag()
    has.name = hastag
    graph.create(has)

    stream = tweepy.Stream(auth, l)
    stream.filter(track=[hastag])