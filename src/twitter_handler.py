""" This handler searches twitter and saves tweets to DynamoDb.
The credentials to call Twitter API are read from EC2 Systems manager."""

import os
import boto3
import awstwitter
import twitter

TWEETS_TABLE = os.environ['TWEETS_TABLE_NAME']
QUERIES_TABLE = os.environ['QUERIES_TABLE_NAME']
CREDENTIALS_NAMESPACE = 'twitter.searchstore'

def get_queries():
    "Read queries table from DynamoDb"
    client = boto3.client('dynamodb')
    response = client.scan(TableName=QUERIES_TABLE)
    return response['Items']

def store_tweets(query, results):
    "Store tweets in DDB"
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TWEETS_TABLE)
    with table.batch_writer() as batch:
        for tweet in results:
            batch.put_item(
                Item={
                    'QueryId': query['QueryId']['S'],
                    'TweetId': tweet.id,
                    'ScreenName': tweet.user.screen_name,
                    'UserId': tweet.user.id,
                    'Coordinates': tweet.coordinates,
                    'Text': tweet.text
                }
            )

def update_last_tweet(query, latest_tweet_id):
    "Update last tweet id to be used for next time"
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(QUERIES_TABLE)
    table.update_item(
        Key={
            'QueryId': query['QueryId']['S']
        },
        UpdateExpression='SET LastTweetId = :val1',
        ExpressionAttributeValues={
            ':val1': latest_tweet_id
        }
    )

def process_query(api, query):
    """Query Twitter and store results
       Returns: Total new tweets found for this query."""
    last_tweet_id = None if 'LastTweetId' not in query else int(query['LastTweetId']['N'])
    results = api.GetSearch(result_type="recent", term=query['Term']['S'],
                           count=25, lang="en", since_id=last_tweet_id)
    new_tweets = []
    if results:
        latest_tweet_id = results[0].id
        for tweet in results:
            if last_tweet_id is not None and tweet.id <= last_tweet_id:
                break
            new_tweets.append(tweet)
        store_tweets(query, new_tweets)
        update_last_tweet(query, latest_tweet_id)
    return len(new_tweets)

def process_all():
    "Process all queries for search and store"
    creds = awstwitter.retrieve_credentials(CREDENTIALS_NAMESPACE)
    api = twitter.Api(creds['consumer_key'], creds['consumer_secret'],
                      creds['access_token'], creds['access_token_secret'])
    query_to_count = {}
    for query in get_queries():
        query_to_count[query['QueryId']['S']] = process_query(api, query)
    return query_to_count

def search_and_store(event, context):
    return process_all()

if __name__ == "__main__":
    RESULTS = process_all()
    if not RESULTS:
        print("No queries found. Please add queries to DynamoDB Table")
    else:
        print(RESULTS)
