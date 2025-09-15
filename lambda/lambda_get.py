import json
import boto3

# Inisialisasi klien DynamoDB dan SQS
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('BukuTamuTable')
sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/694368835432/BukuTamuQueue'  # Ganti dengan URL SQS Anda

# Fungsi untuk menangani GET request
def lambda_handler(event, context):
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
            "body": json.dumps(response['Items'])  # Pastikan body adalah string JSON
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