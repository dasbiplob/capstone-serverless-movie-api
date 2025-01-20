import boto3

def upload_movies_to_dynamodb():
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')  # Use your region
    table = dynamodb.Table('Movies')
    
    movies = [
        {
            "title": "Inception",
            "releaseYear": 2010,
            "genre": "Science Fiction, Action",
            "coverUrl": "https://serverless-movie-bucket.s3.eu-north-1.amazonaws.com/inception.jpg"
        },
        {
            "title": "The Dark Knight",
            "releaseYear": 2008,
            "genre": "Action, Crime, Drama",
            "coverUrl": "https://serverless-movie-bucket.s3.eu-north-1.amazonaws.com/darkkighnt.jpg"
        }
    ]

    for movie in movies:
        table.put_item(Item=movie)
        print(f"Uploaded: {movie['title']}")

if __name__ == "__main__":
    upload_movies_to_dynamodb()
