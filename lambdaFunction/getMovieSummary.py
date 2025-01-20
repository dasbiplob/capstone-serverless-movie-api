import boto3
import json
from decimal import Decimal

# Custom serializer for Decimal objects
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('Movies')  # Replace 'Movies' with your table name

    # Extract 'title' and optionally 'releaseYear' from event
    path_params = event.get('pathParameters', {})
    query_params = event.get('queryStringParameters', {})
    title = path_params.get('title')
    release_year = query_params.get('releaseYear') if query_params else None

    try:
        # Validate inputs
        if not title:
            raise ValueError("Missing required path parameter: 'title'")
        if release_year is None:
            raise ValueError("Missing required query parameter: 'releaseYear'")

        # Convert releaseYear to integer
        release_year = int(release_year)

        # Construct the key
        key = {"title": title, "releaseYear": release_year}

        # Fetch item from DynamoDB
        response = table.get_item(Key=key)

        # Check if item exists
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"message": "Movie not found"})
            }

        # Add generated summary (optional)
        movie = response['Item']
        movie['generatedSummary'] = f"{movie['title']} is a {movie.get('genre', 'movie')} released in {movie['releaseYear']}."

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(movie, cls=DecimalEncoder)
        }

    except ValueError as ve:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"message": str(ve)})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"message": str(e)})
        }
