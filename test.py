import tweepy
import random
import time


def clean_tweet(txt):
    new_word = []
    for word in txt.split():
        if word[0] != '#' and word[0] != '@' and 'http' not in word:
            new_word.append(word)

    return ' '.join(x for x in new_word)

def log(msg):
    nowstr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("{} ----> {}".format(nowstr, msg))


auth = tweepy.OAuthHandler('l63LoKEENH7GgwuhI8b3JNkgB', '1l1cCPcJSFhOVkHQcfmIpPzfZRewjFSMaKJrSxTwnX82TKbd8t')
auth.set_access_token("1062246567405633537-PyZ9I0hpkltbpGRqF8hXFTQXZGrYKN", "J7OnDYneIOcsNI9oEr1Nj8vAFYVKQBKD1pQN9aVj2eOcA")
api = tweepy.API(auth_handler=auth)


# my_tweets = api.user_timeline('@danlabilic', count=200)
# print(len(my_tweets))
#
# for tweet in my_tweets:
#     print(tweet.text)
#     input()

# status = api.get_status(1257746888255614977)
# print(status.text)

# message="Twitter API deneme"
# api.update_status(message)

istanbul_id = api.trends_closest(41.0082, 28.9784)[0]['parentid']

cnt = 0

while True:
    trends = api.trends_place(istanbul_id)[0]['trends']
    # print(len(trends))
    limit = 10
    min_length = 20

    for t in trends:
        if not t['tweet_volume']:

            t['tweet_volume'] = 0

    # print('==========================')
    trends = sorted(trends, key=lambda k: k['tweet_volume'] if k['tweet_volume'] else 0, reverse=True)
    trends_short = trends[:limit]

    hashtags = []

    for t in trends_short:
        hashtag = t['name']
        hashtags.append(hashtag)

    tweet_pool = []

    for tag in hashtags:
        # print('----------------------------------------')
        # print(tag)
        try:
            for tweet in tweepy.Cursor(api.search, q=tag, rpp=100, tweet_mode='extended').items(200):
                txt = tweet._json['full_text']
                if 'RT' not in txt:
                    txt = clean_tweet(txt)
                    if len(txt) > min_length:
                        tweet_pool.append(txt)
        except:
            time.sleep(20 * 60)
            # print('except')
            with open("exception.txt", "w") as exfr:
                exfr.write("OH NO")
            continue

        if len(tweet_pool) > 5:
            random_tweets = random.choices(tweet_pool, k=2)

            my_text = random_tweets[0]
            if len(my_text) + len(random_tweets[1]) < 200:
                my_text += '\n\n\n' + random_tweets[1]

            my_text += '\n' + tag

            # log(my_text)
            api.update_status(my_text)
            # print('waiting...')
            now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            with open(now_str + ".txt", "w") as fw:
                fw.write(my_text)
            time.sleep(3600)


