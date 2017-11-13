""" This handler searches twitter and saves tweets to DynamoDb.
The credentials to call Twitter API are read from EC2 Systems manager."""

import boto3
import awstwitter
import twitter
import pprint

SEARCH_QUERIES = [
    {
        'term': 'Amazon'
    }
]

def process_query(api, query):
    "Query Twitter and store results"
    since_id = None
    search = api.GetSearch(result_type="recent", term=query['term'],
                           count=100, since_id=since_id)
    for tweet in search:
        print '@%s tweeted: %s\n' % (tweet.user.screen_name, tweet.text)


def process_all():
    "Process all queries for search and store"
    creds = awstwitter.retrieve_credentials('twitter.searchstore')
    api = twitter.Api(creds['consumer_key'], creds['consumer_secret'],
                      creds['access_token'], creds['access_token_secret'])
    for query in SEARCH_QUERIES:
        process_query(api, query)

def search_and_store(event, context):
    process_all()
    return {
        'message' : "Hello"
    }

if __name__ == "__main__":
    process_all()
