import json
import boto3
from botocore.exceptions import ClientError
import time

# Inisialisasi klien DynamoDB dan SQS
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('BukuTamuTable')
sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/694368835432/BukuTamuQueue'  # Ganti dengan URL SQS Anda

def lambda_handler(event, context):
    try:
        http_method = event['httpMethod']
        
        # Handle OPTIONS request (Preflight CORS)
        if http_method == 'OPTIONS':
            return {
                "isBase64Encoded": False,
                "statusCode": 200,
                "statusDescription": "200 OK",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                "body": ""
            }
        
        # Route ke handler sesuai HTTP method
        if http_method == 'GET':
            return handle_get(event, context)
        elif http_method == 'POST':
            return handle_post(event, context)
        elif http_method == 'PUT':
            return handle_put(event, context)
        elif http_method == 'DELETE':
            return handle_delete(event, context)
        else:
            return {
                "isBase64Encoded": False,
                "statusCode": 405,
                "statusDescription": "405 Method Not Allowed",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"message": "Method not allowed"})
            }
    
    except Exception as e:
        return {
            "isBase64Encoded": False,
            "statusCode": 500,
            "statusDescription": "500 Internal Server Error",
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": str(e)})
        }

# -------------------------------
# Fungsi untuk menangani GET
# -------------------------------
def handle_get(event, context):
    try:
        response = table.scan()
        
        if not response['Items']:
            initial_data = [
                {'id': '1', 'nama': 'Agus', 'pesan': 'Samawa ya gaes'},
                {'id': '2', 'nama': 'Bambang', 'pesan': 'Sugeng ndalu'},
                {'id': '3', 'nama': 'Cheryl', 'pesan': 'GWS yah'},
                {'id': '4', 'nama': 'Darsimin', 'pesan': 'Semoga langgeng'},
                {'id': '5', 'nama': 'Eriana', 'pesan': 'Selamat menempuh hidup baru, salam dari Bapak'}
            ]
            for item in initial_data:
                table.put_item(Item=item)
            response = table.scan()
        
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "statusDescription": "200 OK",
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(response['Items'])
        }
    
    except ClientError as e:
        return {
            "isBase64Encoded": False,
            "statusCode": 500,
            "statusDescription": "500 Internal Server Error",
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": str(e)})
        }

# -------------------------------
# Fungsi untuk menangani POST
# -------------------------------
def handle_post(event, context):
    try:
        body = json.loads(event['body'])
        nama = body.get('nama', '').strip()
        pesan = body.get('pesan', '').strip()
        
        if not nama or not pesan:
            return {
                "isBase64Encoded": False,
                "statusCode": 400,
                "statusDescription": "400 Bad Request",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"message": "Nama dan pesan tidak boleh kosong"})
            }

        id = str(int(time.time()))
        message = {'id': id, 'nama': nama, 'pesan': pesan}
        
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message)
        )
        
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "statusDescription": "200 OK",
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Data tamu berhasil dikirim ke antrian!", "id": id})
        }
    
    except ClientError as e:
        return {
            "isBase64Encoded": False,
            "statusCode": 500,
            "statusDescription": "500 Internal Server Error",
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": str(e)})
        }

# -------------------------------
# Fungsi untuk menangani PUT
# -------------------------------
def handle_put(event, context):
    try:
        path = event.get('path', '')
        id = path.split('/')[-1]

        if not id:
            return {
                "isBase64Encoded": False,
                "statusCode": 400,
                "statusDescription": "400 Bad Request",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"message": "ID tidak ditemukan di path"})
            }

        body = json.loads(event['body'])
        nama = body.get('nama', '').strip()
        pesan = body.get('pesan', '').strip()
        
        if not nama or not pesan:
            return {
                "isBase64Encoded": False,
                "statusCode": 400,
                "statusDescription": "400 Bad Request",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"message": "Nama dan pesan tidak boleh kosong"})
            }

        table.update_item(
            Key={'id': id},
            UpdateExpression='SET nama = :nama, pesan = :pesan',
            ExpressionAttributeValues={
                ':nama': nama,
                ':pesan': pesan
            }
        )
        
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "statusDescription": "200 OK",
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Tamu berhasil diperbarui!"})
        }
    
    except ClientError as e:
        return {
            "isBase64Encoded": False,
            "statusCode": 500,
            "statusDescription": "500 Internal Server Error",
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": str(e)})
        }

# -------------------------------
# Fungsi untuk menangani DELETE
# -------------------------------
def handle_delete(event, context):
    try:
        path = event.get('path', '')
        id = path.split('/')[-1]

        if not id:
            return {
                "isBase64Encoded": False,
                "statusCode": 400,
                "statusDescription": "400 Bad Request",
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"message": "ID tidak ditemukan di path"})
            }

        table.delete_item(Key={'id': id})
        
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "statusDescription": "200 OK",
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Tamu berhasil dihapus!"})
        }
    
    except ClientError as e:
        return {
            "isBase64Encoded": False,
            "statusCode": 500,
            "statusDescription": "500 Internal Server Error",
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": str(e)})
        }
