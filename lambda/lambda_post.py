import json
import boto3

# Inisialisasi klien DynamoDB dan SQS
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('BukuTamuTable')
sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/694368835432/BukuTamuQueue'  # Ganti dengan URL SQS Anda

# Fungsi untuk menangani POST request
def handle_post(event):
    try:
        # Parse data dari body request
        body = json.loads(event['body'])
        nama = body.get('nama', '').strip()
        pesan = body.get('pesan', '').strip()
        
        # Validasi input
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