import os
import json
import twitter
import credentials

USERS = ['@twitter', '@twitterapi', '@support']

LANGUAGES = ['en']

#Columbus, Cleveland, Buffalo, Pittsburg
#NW
Cleveland = "41.49, 81.69"
#SW
Columbus = "39.9, 82.9"
#NE
Buffalo = "42.8, 78.8"
#SE
Pittsburgh ="40.4, 80.0"
#Columbus, Pittsburg, Bffalo, Cleveland

api = twitter.Api(credentials.consumer_key, credentials.consumer_secret, credentials.access_token_key, credentials.access_token_secret)

def main():
    with open('output1.txt', 'a') as f:
        for line in api.GetStreamFilter(locations=["-81.8791, 41.333","-81.4698, 41.5685"]):
            #data = json.dumps(line)
            if 'text' in line:
                f.write(json.dumps(line["text"]))
                f.write('\n')
            #f.write("User: {user}, Tweet: '{tweet}'".format(user=tweets.user.screen_name, tweet=tweets.text))


if __name__ == '__main__':
    main()

