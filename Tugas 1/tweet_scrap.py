import tweepy

key = open("twitter_api_key.txt","r")
consumer_key=key.readline().rstrip()
consumer_secret=key.readline().rstrip()
access_token=key.readline().rstrip()
access_token_secret=key.readline().rstrip()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

file = open("raw_tweet.txt","w")

keywords = "Jokowi"

for tweet in tweepy.Cursor(api.search, q=keywords, rpp=100, result_type="recent", include_entities=True, lang="id").items(100):
    print(tweet.created_at)
    print(tweet.text)
    file.write("\n")
    file.write(str(tweet.created_at))
    file.write("\n")
    file.write(str(tweet.text))
    file.write("\n")

file.close()
