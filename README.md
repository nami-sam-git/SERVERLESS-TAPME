# Alur Kerja Pembuatan Web Static Buku Tamu 4

Proyek ini adalah **buku tamu digital** yang digunakan pada acara resepsi pernikahan. Aplikasi ini terdiri dari:
1. **Halaman Web Static** yang dihosting di **AWS S3**.
2. **API Gateway** untuk menangani request **GET, POST, PUT, dan DELETE**.
3. **AWS Lambda (Python)** sebagai backend untuk memproses permintaan.
4. **DynamoDB** untuk menyimpan data tamu.
1. **Halaman Web Static** yang dihosting di **AWS S3**.
2. **API Gateway** untuk menangani request **GET**, **POST**, **PUT**, dan **DELETE**.
3. **AWS Lambda (Python)** sebagai backend untuk memproses permintaan.
4. **DynamoDB** untuk menyimpan data tamu.
5. **Amazon SQS** untuk mengantrikan data tamu sebelum diproses.
6. **AWS Backup** untuk melakukan backup otomatis pada DynamoDB.
7. **S3 Bucket Replica** untuk membuat salinan bucket utama yang berisi web statis.

![Arsitektur](serverless-4.png)

---

## **1. Membuat Halaman Web Static (S3)**
**Langkah-langkah:**
1. Buat **bucket S3** melalui AWS Console dengan nama `buku-tamu-serverless-4-namadepan`.
2. Upload file **index.html** dan **script.js**.
3. Aktifkan **Static Website Hosting** pada bucket S3.
4. Pastikan pengaturan CORS telah diatur agar API dapat diakses dari frontend.

---

## **2. Membuat S3 Bucket Replica**
**Langkah-langkah:**
1. Buat **bucket S3 replica** melalui AWS Console dengan nama `buku-tamu-serverless-4-namadepan-replica`.
2. Aktifkan **Replication Rules** pada bucket utama untuk menyalin semua objek ke bucket replica secara otomatis.
3. Pastikan bucket replica memiliki pengaturan **Static Website Hosting** yang sama dengan bucket utama.

---

## **3. Membuat API Gateway**
**API Gateway digunakan untuk menangani request HTTP**, dengan endpoint berikut:
| Method  | Endpoint             | Deskripsi                   |
|---------|----------------------|-----------------------------|
| `GET`   | `/bukutamu/`                  | Mendapatkan semua tamu      |
| `POST`  | `/bukutamu/`                  | Menambahkan tamu baru       |
| `PUT`   | `/bukutamu/{id}`              | Memperbarui data tamu       |
| `DELETE`| `/bukutamu/{id}`              | Menghapus data tamu         |

update file **script.js** Anda untuk menambahkan URL API

---

## **4. Membuat Lambda**
**Setiap metode HTTP dihubungkan ke Lambda Function berikut:**
- `POST`  : `lambda_post.py`
- `GET`   : `lambda_get.py`
- `PUT`   : `lambda_put.py`
- `DELETE`: `lambda_delete.py`
  
**Tanpa metode:**
- `lambda_sqs.py` (memproses pesan dari SQS dan menyimpan ke DynamoDB)

---

## **5. Menambahkan Amazon SQS**
**Langkah-langkah:**
1. Buat **SQS Queue** dengan nama `BukuTamuQueue`.
2. Atur trigger SQS pada `lambda_sqs.py` untuk memproses pesan secara otomatis.

---

## **6. Menyimpan Data ke DynamoDB**
Buat tabel **DynamoDB** dengan nama `BukuTamuTable` dengan:
- **Partition Key**: `id` (String)
- **Atribut Lain (opsional)**: `nama`, `pesan`

**Struktur Data:**
```json
{
  "id": "1707898761",
  "nama": "Andi",
  "pesan": "Selamat menikah!"
}
```

---

## **7. Mengaktifkan AWS Backup untuk DynamoDB**
**Langkah-langkah:**
1. Buka **AWS Backup** di AWS Console.
2. Buat **backup plan** baru.
3. Pilih **DynamoDB** sebagai sumber backup.
4. Tentukan jadwal backup.
5. Pilih **retention period**.
6. Aktifkan backup plan.

---

### Catatan:
`Pastikan IAM Role untuk Lambda Function memiliki izin yang cukup untuk mengakses SQS, DynamoDB, dan S3.`
