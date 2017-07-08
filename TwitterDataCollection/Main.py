import tweepy
import json

consumer_key = '5Xyt2JIpgCWsSboL4jqITlZCb'
consumer_secret = 'QdgAqnCTeChFurGOyPcGowJAZw5m6eQ14gyZpeaRFw3mQWpoEF'
access_token = '1924437534-ZnmL5AadDja6bFBkTCfczZLIfOvVbl6iil1ieqw'
access_token_secret = 'tw0PzDpTsSIbKZuGOxPqxNdCIOsxblUWfB1hCiSN8DAEi'

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        print ''
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)


    name = raw_input("Hastag to search:")
    hastag = "#" + name
    print "Showing all new tweets for ",hastag

    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth, l)
    stream.filter(track=[hastag])