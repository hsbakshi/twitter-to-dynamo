"This script allows managing queries to search and store in DynamoDb"

import os
import argparse
import pprint
import uuid
import boto3

try:
    input = raw_input
except NameError:
    pass

QUERIES_TABLE = os.environ['QUERIES_TABLE_NAME']

def process():
    "Process arguments to manage queries"
    parser = argparse.ArgumentParser(description='Manage queries.')
    parser.add_argument('mode', choices=['add', 'list'],
                        help='Choose mode')
    args = parser.parse_args()
    mode = args.mode
    if mode == 'add':
        add_query()
    elif mode == 'list':
        list_queries()

def add_query():
    "Add query to be processed."
    term = input('Please enter query term: ')
    query_id = uuid.uuid4().hex
    query = {
        'QueryId': query_id,
        'Term': term
    }
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(QUERIES_TABLE)
    table.put_item(
        Item=query,
        ConditionExpression="attribute_not_exists(QueryId)"
    )
    print("Query has been added. QueryId: %s" % query_id)

def list_queries():
    "List queries to processed."
    client = boto3.client('dynamodb')
    response = client.scan(TableName=QUERIES_TABLE)
    for query in response['Items']:
        pprint.pprint(query)
    if not response['Items']:
        print("No queries found.")

if __name__ == "__main__":
    process()
