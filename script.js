$(document).ready(function() {
    const apiUrl = 'https://uhe49hnny0.execute-api.us-east-1.amazonaws.com/dev/bukutamu';

    let selectedGuestId = null; // ID tamu yang akan diperbarui

    // Fungsi menampilkan notifikasi
    function showNotification(message, type) {
        const notification = $('#notification');
        notification.removeClass('hidden notification-success notification-error notification-info');
        notification.addClass(`notification-${type}`);
        notification.text(message).removeClass('hidden');

        setTimeout(() => {
            notification.addClass('hidden');
        }, 3000);
    }

    // Fungsi memuat daftar tamu (GET)
    function loadGuests() {
        $.ajax({
            url: apiUrl,
            method: 'GET',
            success: function(data) {
                console.log('Respons API:', data); 

                // Pastikan data yang diterima adalah array
                if (!Array.isArray(data)) {
                    console.error('Response is not an array');
                    showNotification('Gagal memuat daftar tamu: Respons tidak valid', 'error');
                    return;
                }

                // Urutkan berdasarkan ID (terbaru ke terlama)
                const sortedData = data.sort((a, b) => b.id - a.id);
                $('#guestList').empty();

                if (sortedData.length === 0) {
                    showNotification('Daftar tamu kosong.', 'info');
                } else {
                    showNotification('Daftar tamu berhasil dimuat.', 'success');
                }

                // Tampilkan tamu ke dalam tabel
                sortedData.forEach((guest, index) => {
                    $('#guestList').append(`
                        <tr>
                            <td class="p-2">${index + 1}</td>
                            <td class="p-2">${guest.nama || 'Nama tidak tersedia'}</td>
                            <td class="p-2">${guest.pesan || 'Pesan tidak tersedia'}</td>
                            <td class="p-2">
                                <button class="btn-edit px-2 py-1 rounded-md" onclick="editGuest('${guest.id}', '${guest.nama}', '${guest.pesan}')">Edit</button>
                                <button class="btn-delete px-2 py-1 rounded-md" onclick="deleteGuest('${guest.id}')">Hapus</button>
                            </td>
                        </tr>
                    `);
                });
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                showNotification('Gagal memuat daftar tamu!', 'error');
            }
        });
    }

    // Tambah/Edit tamu (POST/PUT)
    $('#guestForm').submit(function(event) {
        event.preventDefault();
        const name = $('#name').val();
        const message = $('#message').val();
        const method = selectedGuestId ? 'PUT' : 'POST';
        const url = selectedGuestId ? `${apiUrl}/${selectedGuestId}` : apiUrl;
    
        console.log("Mengirim data:", { nama: name, pesan: message }); // Debugging
    
        $.ajax({
            url: url,
            method: method,
            data: JSON.stringify({ nama: name, pesan: message }),
            contentType: 'application/json',
            headers: {
                "Access-Control-Allow-Origin": "*", // Tambahkan ini jika API mendukung
            },
            success: function(response) {
                console.log("Respons API setelah POST:", response); // Debugging
                $('#name').val('');
                $('#message').val('');
                selectedGuestId = null;
                loadGuests();
                showNotification(method === 'POST' ? 'Tamu berhasil ditambahkan!' : 'Tamu berhasil diperbarui!', 'success');
            },
            error: function(xhr) {
                console.error("Gagal menambahkan tamu!", xhr.responseText);
                showNotification(method === 'POST' ? 'Gagal menambahkan tamu!' : 'Gagal memperbarui tamu!', 'error');
            }
        });
    });
    

    // Edit tamu (memasukkan data ke form)
    window.editGuest = function(id, name, message) {
        selectedGuestId = id;
        $('#name').val(name);
        $('#message').val(message);
        showNotification('Edit mode: Silakan perbarui data tamu.', 'info');
    };

    // Hapus tamu (DELETE)
    window.deleteGuest = function(id) {
        $.ajax({
            url: `${apiUrl}/${id}`,
            method: 'DELETE',
            success: function() {
                loadGuests();
                showNotification('Tamu berhasil dihapus!', 'success');
            },
            error: function() {
                showNotification('Gagal menghapus tamu!', 'error');
            }
        });
    };

    // Muat daftar tamu saat halaman dimuat
    loadGuests();
});
