import json
import boto3

#DynamoDB Client from the AWS Library
dynamodb = boto3.client('dynamodb')
#62 position's Alphabet for base62 encoding
alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def lambda_handler(event, context):
    #Check if POST Body has the URL
    if(event['url'] == ""):
        return {
            'statusCode': 422,
            'body': 'Number of parameters expected (1) URL of type String'
        }
    #Hash the url to create a numeric value, then encode it in base62
    hashedURL = encode(hash(event['url']))
    try:
        #Put item on DynamoDB as a key pair consisting on [Hash: Complete URL]
        dynamodb.put_item(TableName="links",Item={'id':{'S':hashedURL},'url':{'S':event['url']}})
    except Exception as error:
        return {
            'statusCode' : 500,
            'body' : error
        }
    #Return finished URL using a template url for this challenge    
    return {
        'statusCode': 200,
        'body': 'shorty.com/'+hashedURL
    }

# Encoder for base62
# Input: Any numeric value
# Output: A base62 encoded string
def encode(num):
    if num == 0 :
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        num,rem = divmod(num,base)
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)
