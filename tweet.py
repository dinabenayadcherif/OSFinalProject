import os
import json
import twitter
import credentials

USERS = ['@twitter', '@twitterapi', '@support']

LANGUAGES = ['en']


api = twitter.Api(credentials.consumer_key, credentials.consumer_secret, credentials.access_token_key, credentials.access_token_secret)

def main():
    with open('output.txt', 'a') as f:
        for line in api.GetStreamFilter(track=['Trump']):
            f.write(json.dumps(line))
            f.write('\n')


if __name__ == '__main__':
    main()

