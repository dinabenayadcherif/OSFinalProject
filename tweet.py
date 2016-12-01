import os
import json
import twitter
import credentials

USERS = ['@twitter', '@twitterapi', '@support']

LANGUAGES = ['en']


api = twitter.Api(credentials.consumer_key, credentials.consumer_secret, credentials.access_token_key, credentials.access_token_secret)

def main():
    with open('output2.txt', 'a') as f:
        for line in api.GetStreamFilter(track=['Trump']):
            #data = json.dumps(line)
            if 'text' in line:
                f.write(json.dumps(line["text"]))
                f.write('\n')
            #f.write("User: {user}, Tweet: '{tweet}'".format(user=tweets.user.screen_name, tweet=tweets.text))


if __name__ == '__main__':
    main()

