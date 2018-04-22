import tweepy
import json
import time

from py2neo import Graph, Relationship
from Account import get_next_credentials, Account, initial_credentials


class StdOutListener(tweepy.StreamListener):
    # time_start = time.time()

    def __init__(self, graph, list_user, timelimit):
        self.graph = graph
        self.list_user = list_user
        self.timeLimit = timelimit
        self.time_start = time.time()
        self.time_out = self.time_start + self.timeLimit * 10

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
            accountobject.created_at = decoded['created_at']

            self.list_user.append(accountobject)
            self.graph.create(accountobject)

            print "[APP] " + str(len(self.list_user)) + ":\t" + str(round((time.time() - self.time_start), 2)) \
                  + " seconds" + ":\t\t" + accountobject.username

            return True
        else:
            # Stop the search
            print "[APP] " + "TIMEOUT: " + str(round((time.time() - self.time_start), 2)) + \
                  " The search has been finished"
            return False

    def on_error(self, status):
        print status


class neo4j():
    def __init__(self):
        self.graph = Graph(password='password')
        self.tx = self.graph.begin()
        self.api = ""
        self.list_user = []
        self.timeLimit = 1  # In minutes
        self.timeout = time.time() + self.timeLimit * 60

    def be_follow(self):
        print "[APP] " + "there are ", len(self.list_user), "users"
        copy_list = self.list_user[:]
        len1 = len(self.list_user)
        for user in self.list_user:
            for user2 in copy_list:
                if user.username is not user2.username:
                    a = self.list_user.index(user)

                    b = copy_list.index(user2)
                    print "{0:.2f}".format((self.list_user.index(user) *
                        len1 + copy_list.index(user2)) / float(len1 * len1) * 100), " %"

                    # print a * b / len(self.list_user) * 100
                    # print user.username, " to ", user2.username
                    try:
                        if self.check_following(user.username, user2.username):
                            self.create_relationship(user, user2)
                    except tweepy.RateLimitError:
                        self.change_credentials()
        print "100.00 %"
        print "[APP] " + "End of search of friendship"

    def check_following(self, user, user2):
        # True if user following to user2
        try:
            relation = self.api.show_friendship(source_screen_name=user, target_screen_name=user2)
        except tweepy.RateLimitError:
            self.change_credentials()
            relation = self.api.show_friendship(source_screen_name=user, target_screen_name=user2)
        return relation[0].following

    def change_credentials(self):
        credentials = get_next_credentials()
        auth = tweepy.OAuthHandler(credentials[0], credentials[1])
        auth.set_access_token(credentials[2], credentials[3])
        self.api = tweepy.API(auth)

    def create_relationship(self, user1, user2):
        print "[APP] " + str(user1.username) + " following to " + str(user2.username)
        print "[APP] " + "creating relationship...     ",
        existing_user1 = self.graph.find_one('Account', property_key='username', property_value=user1.username)
        existing_user2 = self.graph.find_one('Account', property_key='username', property_value=user2.username)
        existing_u1_knows_u2 = Relationship(existing_user1, 'Follow to', existing_user2)
        self.graph.create(existing_u1_knows_u2)
        print "[APP] " + "[DONE]"

    def start_app(self, hastag, minutes):

        self.timeLimit = int(minutes)
        # timeLimit = int(time)
        time_start = time.time()
        l = StdOutListener(self.graph, self.list_user, self.timeLimit)
        # try:
        credentials = initial_credentials()
        auth = tweepy.OAuthHandler(credentials[0], credentials[1])
        auth.set_access_token(credentials[2], credentials[3])
        try:
            self.api = tweepy.API(auth)
        except tweepy.error.RateLimitError:
            self.change_credentials()
            self.api = tweepy.API(auth)

        to_search = "#" + hastag
        print "[APP] " + "Showing all new tweets for ", to_search
        print "[APP] " + "Initializing stream:"
        stream = tweepy.Stream(auth, l)
        stream.filter(track=[hastag])

    def get_all_node(self):
        return self.graph.data("Match(n:Account) return n")

    def main(self, hastag, minutes):
        print "[APP] " + "The last graph has been deleted"
        self.graph.delete_all()
        print "[APP] " + "START the application"
        self.start_app(hastag, minutes)
        print "[APP] " + "Checking friendship..."
        self.be_follow()
        print "[APP] END"
