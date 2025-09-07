import json
import boto3

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