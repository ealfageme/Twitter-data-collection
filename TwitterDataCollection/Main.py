import tweepy
import sys
import signal
import time
import json
from py2neo import Graph, Node, Relationship
from py2neo.ogm import Property, GraphObject

# Twitter keys
consumer_key = '5Xyt2JIpgCWsSboL4jqITlZCb'
consumer_secret = 'QdgAqnCTeChFurGOyPcGowJAZw5m6eQ14gyZpeaRFw3mQWpoEF'
access_token = '1924437534-ZnmL5AadDja6bFBkTCfczZLIfOvVbl6iil1ieqw'
access_token_secret = 'tw0PzDpTsSIbKZuGOxPqxNdCIOsxblUWfB1hCiSN8DAEi'

# graph instance
graph = Graph(password='password')
tx = graph.begin()
api = ""
# Mode debug don't necessary to introduce the hastag and print the search
debug = False
list_user = []
timeLimit = 1  # In minutes
timeout = time.time() + timeLimit * 60  # 1 minute


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

            print str(len(list_user)) + ":\t" + str(round((time.time() - self.time_start), 2)) + " seconds"\
                  + ":\t\t" + accountobject.username

            return True
        else:
            # Stop the search
            print "TIMEOUT: "+ str(round((time.time() - self.time_start), 2)) + \
                  " The search has been finished"
            return False

    def on_error(self, status):
        print status


def be_follow():
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


def create_relationship(user1, user2):
    print str(user1.username) + " following to " + str(user2.username)
    print "creating relationship..."
    existing_user1 = graph.find_one('Account', property_key='username', property_value=user1.username)
    existing_user2 = graph.find_one('Account', property_key='username', property_value=user2.username)
    existing_u1_knows_u2 = Relationship(existing_user1, 'Follow to', existing_user2)
    graph.create(existing_u1_knows_u2)


def signal_handler(signal, frame):
    print("You pressed Ctrl+C")
    print("Stop th application")
    sys.exit(0)


def start_app():
    global api
    try:
        l = StdOutListener()
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
    except Exception:
        print "Error: Authentication failed"

    if not debug:

        name = raw_input("Hastag to search:")
        toSearch = "#" + name
        print "Showing all new tweets for ", toSearch
    else:

        toSearch = "#FelizSabado"

    print "Initializing stream:"
    stream = tweepy.Stream(auth, l)
    stream.filter(track=[toSearch])

if __name__ == '__main__':

    print "The last graph has been deleted"
    graph.delete_all()
    print "Press Ctrl + C to cancel the application"
    signal.signal(signal.SIGINT, signal_handler)
    print "START the application"
    start_app()
    print "Checking friendship..."
    be_follow()

    print "END"






