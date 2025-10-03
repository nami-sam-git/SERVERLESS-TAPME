import json
import boto3
from botocore.exceptions import ClientError
import time

# Inisialisasi klien DynamoDB dan SQS
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('BukuTamuTable')

def lambda_handler(event, context):
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