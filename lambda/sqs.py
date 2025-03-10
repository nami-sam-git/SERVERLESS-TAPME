import json
import boto3
from botocore.exceptions import ClientError

# Inisialisasi klien DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('BukuTamuTable')

def lambda_handler(event, context):
    try:
        # Loop melalui setiap pesan dalam event (SQS bisa mengirim batch pesan)
        for record in event['Records']:
            # Parse pesan dari SQS
            message = json.loads(record['body'])
            id = message['id']
            nama = message['nama']
            pesan = message['pesan']
            
            # Simpan data ke DynamoDB
            table.put_item(Item={
                'id': id,
                'nama': nama,
                'pesan': pesan
            })
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Data tamu berhasil diproses!'})
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }
