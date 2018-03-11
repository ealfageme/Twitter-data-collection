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


index = 0
# Consumer key, consumer_secret,access_token, access_token_secret7
MY_KEYS = [
    # @5DataCollection
    [
        '5Xyt2JIpgCWsSboL4jqITlZCb',
        'QdgAqnCTeChFurGOyPcGowJAZw5m6eQ14gyZpeaRFw3mQWpoEF',
        '1924437534-ZnmL5AadDja6bFBkTCfczZLIfOvVbl6iil1ieqw',
        'tw0PzDpTsSIbKZuGOxPqxNdCIOsxblUWfB1hCiSN8DAEi'
    ],
    # @4DataCollection
    [
        'ZMWV6z2cQq1BtROWNfkv8qHnB',
        'kQ3MtV6Fq3kRATCEZJ4jNuzkcJuOiITnSVUlMMX5isWdWZZK8E',
        '967359967723442176-smrg5oQ1rUFWBzgugSYarl1AYj91PFt',
        'bi2KVaKyJYbsdW4a506BBQk3xE3uDaLlecva63S9OuNm7'
    ],
    # @3DataCollection
    [
        'qHuStmPL8V2uOufSfMJxnpc7m',
        '0e4xzKdFzDDBC96MBLrWbRHQOggQrSOM5ajaommRmz35G1ajbu',
        '972770478904479744-9ereYzqEJDisw39KYHO6MzU3a55tlB9',
        'kv3P3EnjtZdLIEW0qFRdf7MNV22YfZWH8ccTbWS7NHJro'
    ],
    [
        'HX4DhaSMnQ4mdvmpt0In4ioLe',
        'XkAApKqDMvy4rl7Vnw8CtuUsFzimyJsJjgInFMYpT4HKKAHQC7',
        '972800145187360768-LmYlc8LC6akgAkjNUY6lG8oOhby26br',
        'Ow6DY1UVrlZDPTGte2EhC5sIJJBjunkM6c7Ssl4FwmjGn'
    ]
]


def get_next_credentials():
    global index
    credentials = MY_KEYS[index]
    if index == (len(MY_KEYS) - 1):
        index = 0
    else:
        index += 1
    return credentials

