import json
import boto3
from botocore.exceptions import ClientError
import time

# Inisialisasi klien DynamoDB dan SQS
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('BukuTamuTable')
sqs = boto3.client('sqs')
queue_url = 'https://sqs.xxxxxxxxxxxxxxxxxxxxxxxxxxx/BukuTamuQueue'  # Ganti dengan URL SQS Anda

def lambda_handler(event, context):
    try:
        # Ambil HTTP method dari event
        http_method = event['httpMethod']
        
        # Handle GET request (Mengambil semua tamu)
        if http_method == 'GET':
            return handle_get(event)
        
        # Handle POST request (Menambahkan tamu baru)
        elif http_method == 'POST':
            return handle_post(event)
        
        # Handle PUT request (Memperbarui tamu)
        elif http_method == 'PUT':
            return handle_put(event)
        
        # Handle DELETE request (Menghapus tamu)
        elif http_method == 'DELETE':
            return handle_delete(event)
        
        # Jika method tidak dikenali
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

# Fungsi untuk menangani GET request
def handle_get(event):
    try:
        # Ambil semua data dari tabel
        response = table.scan()
        
        # Jika tidak ada data, buat data awal
        if not response['Items']:
            initial_data = [
                {'id': '1', 'nama': 'Agus', 'pesan': 'Samawa ya gaes'},
                {'id': '2', 'nama': 'Bambang', 'pesan': 'Sugeng ndalu'},
                {'id': '3', 'nama': 'Cheryl', 'pesan': 'GWS yah'},
                {'id': '4', 'nama': 'Darsimin', 'pesan': 'Semoga langgeng'},
                {'id': '5', 'nama': 'Eriana', 'pesan': 'Selamat menempuh hidup baru, salam dari Bapak'}
            ]
            
            # Masukkan data awal ke tabel
            for item in initial_data:
                table.put_item(Item=item)
            
            # Ambil data lagi setelah memasukkan data awal
            response = table.scan()
        
        # Kembalikan data tamu
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

# Fungsi untuk menangani POST request
def handle_post(event):
    try:
        # Parse data dari body request
        body = json.loads(event['body'])
        nama = body['nama']
        pesan = body['pesan']
        
        # Generate ID unik (contoh menggunakan timestamp)
        id = str(int(time.time()))
        
        # Buat pesan untuk dikirim ke SQS
        message = {
            'id': id,
            'nama': nama,
            'pesan': pesan
        }
        
        # Kirim pesan ke SQS
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message)
        )
        
        # Kembalikan respons sukses
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

# Fungsi untuk menangani PUT request
def handle_put(event):
    try:
        # Ambil ID dari path (misalnya, /1741654045)
        path = event.get('path', '')  # Dapatkan path dari event
        id = path.split('/')[-1]  # Ambil ID dari path

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

        # Parse data dari body request
        body = json.loads(event['body'])
        nama = body['nama']
        pesan = body['pesan']
        
        # Perbarui data di tabel
        table.update_item(
            Key={'id': id},
            UpdateExpression='SET nama = :nama, pesan = :pesan',
            ExpressionAttributeValues={
                ':nama': nama,
                ':pesan': pesan
            }
        )
        
        # Kembalikan respons sukses
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

# Fungsi untuk menangani DELETE request
def handle_delete(event):
    try:
        # Ambil ID dari path (misalnya, /1741654045)
        path = event.get('path', '')  # Dapatkan path dari event
        id = path.split('/')[-1]  # Ambil ID dari path

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

        # Hapus data dari tabel
        table.delete_item(Key={'id': id})
        
        # Kembalikan respons sukses
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
