import json
import boto3
import requests
import os

def lambda_handler(event, context):
    # TODO implement
    input = event['queryStringParameters']['q'].strip()
    url = os.getenv('ES_URL') + "posts/_search?q=" + input
    responseES = requests.get(url, auth=(os.getenv('ES_USER'), os.getenv('ES_PASS')))
    r = responseES.json()
    
    idList = []
    if 'hits' in r:
        count = 0
        for val in r['hits']['hits']:
            idList.append(val['_source']['id'])
            count += 1
            if count == 3:
                break
    
        client = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id=os.getenv('AWS_ACCESS'), aws_secret_access_key=os.getenv('AWS_SECRET'))
        answerList = []
        for id in idList:
            payload = {'id': {'S': id}}
            responseDB = client.get_item(TableName='posts', Key=payload)
            answerList.append(responseDB['Item'])
        
        return {
            'statusCode': 200,
            'body': json.dumps(answerList)
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps([])
        }
