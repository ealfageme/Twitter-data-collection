import tweepy
import json
import time

from py2neo import Graph, Relationship
from Account import get_next_credentials, Account

graph = Graph(password='password')
tx = graph.begin()
api = ""
list_user = []
timeLimit = 1  # In minutes
timeout = time.time() + timeLimit*60


class StdOutListener(tweepy.StreamListener):
    # time_start = time.time()

    def __init__(self, time):
        self.time_start = time
        self.time_out = self.time_start + timeLimit*10

    def on_data(self, data):

        if time.time() < self.time_out:
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

            print "[APP] " + str(len(list_user)) + ":\t" + str(round((time.time() - self.time_start), 2)) \
                                        + " seconds" + ":\t\t" + accountobject.username

            return True
        else:
            # Stop the search
            print "[APP] " + "TIMEOUT: " + str(round((time.time() - self.time_start), 2)) + \
                  " The search has been finished"
            return False

    def on_error(self, status):
        print status


def be_follow():
    print "[APP] " + "there are ", len(list_user), "users"
    copy_list = list_user[:]
    for user in list_user:
        for user2 in copy_list:
            if user.username is not user2.username:
                if check_following(user.username, user2.username):
                    create_relationship(user, user2)
    print "[APP] " + "End of search of friendship"


def check_following(user, user2):
    # True if user following to user2
    try:
        relation = api.show_friendship(source_screen_name=user, target_screen_name=user2)
    except tweepy.error.RateLimitError:
        change_credentials()
        relation = api.show_friendship(source_screen_name=user, target_screen_name=user2)
    return relation[0].following


def change_credentials():
    global api
    credentials = get_next_credentials()
    auth = tweepy.OAuthHandler(credentials[0], credentials[1])
    auth.set_access_token(credentials[2], credentials[3])
    api = tweepy.API(auth)


def create_relationship(user1, user2):
    print "[APP] " + str(user1.username) + " following to " + str(user2.username)
    print "[APP] " + "creating relationship...     ",
    existing_user1 = graph.find_one('Account', property_key='username', property_value=user1.username)
    existing_user2 = graph.find_one('Account', property_key='username', property_value=user2.username)
    existing_u1_knows_u2 = Relationship(existing_user1, 'Follow to', existing_user2)
    graph.create(existing_u1_knows_u2)
    print "[APP] " + "[DONE]"


def start_app(hastag, minutes):
    global api
    global timeLimit
    timeLimit = int(minutes)
    # timeLimit = int(time)
    time_start = time.time()
    l = StdOutListener(time_start)
    # try:
    credentials = get_next_credentials()
    auth = tweepy.OAuthHandler(credentials[0], credentials[1])
    auth.set_access_token(credentials[2], credentials[3])
    api = tweepy.API(auth)

    to_search = "#" + hastag
    print "[APP] " + "Showing all new tweets for ", to_search
    print "[APP] " + "Initializing stream:"
    stream = tweepy.Stream(auth, l)
    stream.filter(track=[to_search])


def get_all_node():
    return graph.data("Match(n:Account) return n.username")


def main(hastag, minutes):
    print "[APP] " + "The last graph has been deleted"
    graph.delete_all()
    print "[APP] " + "START the application"
    start_app(hastag, minutes)
    print "[APP] " + "Checking friendship..."
    be_follow()
    print "[APP] " + 'END'
