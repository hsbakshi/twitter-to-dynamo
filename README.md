# Serverless Twitter to DynamoDb

This serverless stack searches Twitter and stores the Tweets in Dynamo.

If you want to see what people are saying about a topic on Twitter and
store tweets, then you can use this stack to enable the automation.

## AWS technologies used

AWS EC2 Systems Manager - Credentials storage
KMS - Encryption of credentials
AWS Cloudformation
AWS Lambda
AWS DynamoDB
AWS Cloudwatch

## Uploading credentials

We use AWS EC2 Systems manager to store our Twitter credentials.

There are multiple ways of storing credentials there.
Easiest way is to use the "awstwitter" package

## Setting up the Cloudformation stack

Create bundle:

   $ make bundle

Create deployable package:

   $ make package

Deploy the stack

   $ make deploy





