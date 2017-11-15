# Serverless Twitter to DynamoDb

This serverless stack searches Twitter and stores the Tweets in Dynamo.

If you want to see what people are saying about a topic on Twitter and
store tweets, then you can use this stack to enable the automation.

## AWS technologies used

* AWS EC2 Systems Manager - Twitter Credentials storage
* KMS - Encryption of credentials
* AWS Cloudformation - Stack management
* AWS Lambda - Call Twitter and write to DynamoDB
* AWS DynamoDB - Store tweets and queries
* AWS Cloudwatch - Invoke Lambda periodically

# Setup required to use this stack

## Prerequisite: S3 Bucket

Create an S3 bucket to host the code for lambda. Your Lambda code will
be packaged and uploaded to this bucket.

You can export the bucket name so that the Makefile will use it.
```
  $ export S3_BUCKET=my-s3-bucket-name
```

## Prerequisite: Twitter API credentials

You will need to register an app with Twitter to get API credentials.

Start here: https://apps.twitter.com/app/new

This website has a good walk-through: https://www.slickremix.com/docs/how-to-get-api-keys-and-tokens-for-twitter/

After creating the app, you will get the following credetials:
* Consumer Key
* Consumer Secret
* Access Token
* Access Token Secret

We use AWS EC2 Systems manager to store our Twitter credentials.

We will use the 'awstwitter' python module to securely store the credentials
in EC2 Systems manager in an encrypted format.
```
   $ pip install awstwitter
   $ awstwitter store
   ...
```

The awstwitter package will ask for a namespace.
Use "twitter.searchstore" as the namespace.
Then enter the API credentials that you obtained from Twitter.

## Setting up the Cloudformation stack

### One step build and release

To do everything including build, package and stack deployment in one command, run:
```
    $ make release
```

If you do not like using environment variables, then run
```
    $ S3_BUCKET=<bucket name> make release
```

### With local testing

Create bundle:
```
   $ make bundle
```

Create deployable package:
```
   $ make package
```

Deploy the stack
```
   $ make deploy
```

To test the scripts locally, you can use virtualenv to create and activate
a virtual environment. Then install dependencies and run the handler:
```
    $ pip install -r requirements.txt
    $ QUERIES_TABLE_NAME=<query table name> \
     TWEETS_TABLE_NAME=<tweets table name> \
     python src/twitter_handler.py
```

To locally invoke the lambda, first install "aws-sam-local".
See: https://github.com/awslabs/aws-sam-local for installation instructions.
Then install dependencies and invoke:
```
    $ pip install -r requirements.txt
    $ echo {} | QUERIES_TABLE_NAME=<query table name> \
     TWEETS_TABLE_NAME=<tweets table name> \
     sam local invoke "TwitterSearchAndStoreHandler"
```

## Adding queries to search and store in Twitter

Now that the stack is setup, you should have two DynamoDB tables.
One will store the query details that we will use to search Twitter.
The other will store the actual tweets that we find.

Initially, there will be no queries setup. To add a query to crawled, run:
```
    $ python src/manage_queries.py add
```
This command will ask you for a query term. Enter the term.
Once added, the Lambda function will periodically search Twitter
and store Tweets in DynamoDB.





