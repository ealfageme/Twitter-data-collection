import tweepy
import sys
import signal
import time
import json
from py2neo import Graph
from py2neo.ogm import Property, GraphObject

# Twitter keys
consumer_key = 'ZMWV6z2cQq1BtROWNfkv8qHnB'
consumer_secret = 'kQ3MtV6Fq3kRATCEZJ4jNuzkcJuOiITnSVUlMMX5isWdWZZK8E'
access_token = '967359967723442176-smrg5oQ1rUFWBzgugSYarl1AYj91PFt'
access_token_secret = 'bi2KVaKyJYbsdW4a506BBQk3xE3uDaLlecva63S9OuNm7'

# graph instance
graph = Graph(password='password')
tx = graph.begin()
# Mode debug don't necessary to introduce the hastag and print the search
debug = True
list_user = []
limit = 0
timeLimit = 1  # In minutes
# timeout = time.time() + timeLimit * 60 # 1 minute
timeout = time.time() + 5  # 5 seconds


class Account(GraphObject):
    __primarykey__ = "username"
    name = Property()
    username = Property()
    tweet = Property()
    description = Property()
    id_twitter = Property()
    url = Property()
    verified = Property()
    location = Property()
    profile_image_url = Property()
    followers = Property()


# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    time_start = time.time()

    def on_data(self, data):
        if time.time() < timeout:
            # Twitter returns data in JSON format - we need to decode it first
            decoded = json.loads(data)

            accountobject = Account()
            accountobject.username = decoded['user']['screen_name']
            accountobject.tweet = decoded['text'].encode('ascii', 'ignore')
            accountobject.name = decoded['user']['name']
            accountobject.description = decoded['user']['description']
            accountobject.location = decoded['user']['location']
            accountobject.id_twitter = decoded['user']['id']
            accountobject.profile_image_url = decoded['user']['profile_image_url']
            accountobject.verified = decoded['user']['verified']
            accountobject.url = decoded['user']['url']
            accountobject.followers = decoded['user']['followers_count']

            list_user.append(accountobject)
            graph.create(accountobject)

            if not debug:
                print "----------------------------------------------------"
                print "username   :" + accountobject.username
                print "tweet      :" + accountobject.tweet
                print "name       :" + accountobject.name
            else:
                print str(len(list_user)) + ":   " + str(round((time.time() - self.time_start), 2)) + " seconds"
            return True
        else:
            # Stop the search
            print "TIMEOUT: The search has been finished"
            return False

    def on_error(self, status):
        print status


def be_follow():
    print "Checking friendship..."
    copy_list = list_user[:]
    for user in list_user:
        for user2 in copy_list:
            if user.username is not user2.username:
                if check_following(user.username, user2.username):
                    create_relationship(user, user2)
    print "End of search of friendship"


def check_following(user, user2):
    # True if user following to user2
    relation = api.show_friendship(source_screen_name=user, target_screen_name=user2)

    return relation[0].following


def create_relationship(user, user2):
    print str(user.username) + " following to " + str(user2.username)
    # Create the relationship between the node user and the node user2


def signal_handler(signal, frame):
    print("You pressed Ctrl+C")
    print("Stop th application")
    sys.exit(0)


if __name__ == '__main__':

    print 'The last graph has been deleted'
    graph.delete_all()
    signal.signal(signal.SIGINT, signal_handler)
    # Main
    try:
        l = StdOutListener()
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
    except Exception:
        print "Error: Authentication failed"

    if not debug:
        limit = raw_input("The limit of search:")
        name = raw_input("Hastag to search:")
        toSearch = "#" + name
        print "Showing all new tweets for ", toSearch
    else:
        limit = 200
        toSearch = "#FelizSabado"

    print "Initializing stream:"
    stream = tweepy.Stream(auth, l)
    stream.filter(track=[toSearch])

    be_follow()

