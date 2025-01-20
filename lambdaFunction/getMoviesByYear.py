import boto3
import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('Movies')
    
    path_parameters = event.get('pathParameters', {})
    year = path_parameters.get('year')
    
    if not year:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Year parameter is missing'})
        }
    
    try:
        # Convert year to integer
        year = int(year)
        
        response = table.scan(
            FilterExpression="releaseYear = :year",
            ExpressionAttributeValues={":year": year}
        )
        movies = response.get('Items', [])
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(movies, cls=DecimalEncoder)
        }
    
    except ValueError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Year parameter must be an integer'})
        }
