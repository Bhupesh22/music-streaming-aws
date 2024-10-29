from flask import Flask, request, render_template, jsonify
import boto3
import json
import os
from werkzeug.utils import secure_filename
import time
from boto3.dynamodb.conditions import Key

app = Flask(__name__)

# AWS credentials (Replace with your actual credentials)
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_REGION = ''  # Set your desired AWS region
# AWS clients with explicit credentials


s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

kinesis_client = boto3.client(
    'kinesis',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

sqs_client = boto3.client(
    'sqs',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# Define S3 bucket name
S3_BUCKET_NAME = ''
table = dynamodb.Table('')

# Your SQS Queue URL
QUEUE_URL = ''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_music():
    music_file = request.files['music_file']
    playlist_id = request.form['playlist_id']

    # Ensure a valid file is uploaded
    if music_file and music_file.filename.endswith('.mp3'):
        # Save the file temporarily
        filename = secure_filename(music_file.filename)
        music_file.save(filename)

        # Upload the file to S3
        s3_client.upload_file(filename, S3_BUCKET_NAME, filename)

        # Construct the S3 URL
        s3_url = f'https://{S3_BUCKET_NAME}.s3.amazonaws.com/{filename}'

        unique_id = int(time.time() * 1000)  # Current time in milliseconds

        # Store music details in DynamoDB
        table.put_item(
            Item={
                'playlist_id': playlist_id,  # This is now the only key needed
                'music_url': s3_url
            }
        )

        # Send music data to Kinesis
        response = kinesis_client.put_record(
            StreamName='my-music-stream-007',
            Data=json.dumps({'music_url': s3_url, 'playlist_id': playlist_id}),
            PartitionKey='partitionkey'
        )

        # Notify SQS about the new music
        sqs_client.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps({'music_url': s3_url, 'playlist_id': playlist_id})
        )

        # Remove the temporary file
        os.remove(filename)

        return 'Music uploaded successfully!'
    else:
        return 'Invalid file type. Please upload an MP3 file.', 400
    
@app.route('/playlists', methods=['GET'])
def get_playlists():
    response = table.scan()
    playlists = {item['playlist_id'] for item in response.get('Items', [])} 
    print(playlists)
    return {'playlists': list(playlists)}

@app.route('/playlist/<playlist_id>', methods=['GET'])
def get_music_by_playlist(playlist_id):
    response = table.query(
        KeyConditionExpression=Key('playlist_id').eq(playlist_id)
    )
    music_list = [{'music_url': item['music_url']} for item in response.get('Items', [])]

    return {'music': music_list}

@app.route('/listen', methods=['GET'])
def listen_music():
    response = sqs_client.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=20
    )

    messages = response.get('Messages', [])
    music_list = []

    for message in messages:
        body = json.loads(message['Body'])
        music_list.append(body['music_url'])

    return {'music_urls': music_list}

if __name__ == '__main__':
    app.run(debug=True)