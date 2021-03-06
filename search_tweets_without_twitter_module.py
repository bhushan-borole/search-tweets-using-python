import requests
import json
import ast
from requests_oauthlib import OAuth1

import sys

#reference for non_nmp_map : https://stackoverflow.com/questions/32442608/ucs-2-codec-cant-encode-characters-in-position-1050-1050
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

url = 'https://api.twitter.com/1.1/search/tweets.json?q='

class Twitter_Client:
    def __init__(self):
        try:
            with open("twitter_credentials.json", "r") as file:
                creds = json.load(file)
            self.auth = OAuth1(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
        except Exception as e:
            print(e)

    def get_tweets(self, search):

        r = requests.get(url = url + search + '&count=200', auth = self.auth)

        data = r.json()
        #initalize max_id
        MAX_ID = 0

        COUNT = 0

        for tweets in data['statuses']:
            print('User: ' + tweets['user']['screen_name'])
            print('Created At: ' + tweets['created_at'])
            print('Text: ' + tweets['text'].translate(non_bmp_map))
            MAX_ID = tweets['id']                                          #fetch max_id of the last tweet of the first request
            print(''.join(['-']*15))
            COUNT += 1

        for i in range(0, 40):
            try:
                r1 = requests.get(url = url + search + '&count=200&max_id=' + str(MAX_ID), auth = self.auth) # pass max_id as the parameter to the request

                data1 = r1.json()

                for tweets in data1['statuses']:
                    print('User: ' + tweets['user']['screen_name'])
                    print('Created At: ' + tweets['created_at'])
                    print('Text: ' + tweets['text'].translate(non_bmp_map))
                    MAX_ID = tweets['id']                                 
                    print(''.join(['-']*15))
                    COUNT += 1

            except Exception as e:
                print(e)

        print(str(COUNT) + ' tweets fetched.')


def main():
    client = Twitter_Client()
    search = input("Enter Keyword: ")
    client.get_tweets(search)


if __name__ == '__main__':
    main()


'''
retrieve max_id of the last tweet of each request and pass it as a parameter to the next request.
'''





        
