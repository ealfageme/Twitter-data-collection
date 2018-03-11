from py2neo.ogm import Property, GraphObject


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

# Consumer key, consumer_secret,access_token, access_token_secret7
NUMBER_KEYS = 2
MY_KEYS = [
    # @5DataCollection
    '5Xyt2JIpgCWsSboL4jqITlZCb',
    'QdgAqnCTeChFurGOyPcGowJAZw5m6eQ14gyZpeaRFw3mQWpoEF',
    '1924437534-ZnmL5AadDja6bFBkTCfczZLIfOvVbl6iil1ieqw',
    'tw0PzDpTsSIbKZuGOxPqxNdCIOsxblUWfB1hCiSN8DAEi',
    # @4DataCollection
    'ZMWV6z2cQq1BtROWNfkv8qHnB',
    'kQ3MtV6Fq3kRATCEZJ4jNuzkcJuOiITnSVUlMMX5isWdWZZK8E',
    '967359967723442176-smrg5oQ1rUFWBzgugSYarl1AYj91PFt',
    'bi2KVaKyJYbsdW4a506BBQk3xE3uDaLlecva63S9OuNm7'
]

ind = 0


def get_next_credentials():
    global ind
    index = ind
    credentials = (MY_KEYS[4 * index + 0],
                   MY_KEYS[4 * index + 1],
                   MY_KEYS[4 * index + 2],
                   MY_KEYS[4 * index + 3]
                   )
    if len(MY_KEYS) % 4 < (NUMBER_KEYS - 1):
        ind += 1
    else:
        ind = 0
    return credentials

