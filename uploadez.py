import requests
import os

def upload_file(url, file_path):
    """
    Fungsi untuk mengunggah file ke URL yang diberikan.
    
    :param url: URL tujuan upload (contoh: https://example.com/upload)
    :param file_path: Path lokal ke file yang akan diunggah
    :return: Link file yang diunggah jika berhasil, atau pesan error
    """
    try:
        # Buka file dalam mode binary
        with open(file_path, 'rb') as file:
            # Buat dictionary untuk file
            files = {'file': (os.path.basename(file_path), file)}
            
            # Kirim POST request ke URL tujuan
            response = requests.post(url, files=files)
            
            # Cek jika upload berhasil (status code 200)
            if response.status_code == 200:
                # Jika server mengembalikan link, tampilkan
                if 'link' in response.json():
                    return f"File berhasil diunggah! Link: {response.json()['link']}"
                else:
                    return "File berhasil diunggah, tetapi server tidak mengembalikan link."
            else:
                return f"Gagal mengunggah file. Kode status: {response.status_code}"
    except Exception as e:
        return f"Terjadi error: {str(e)}"

def main():
    print("=== File Uploader ===")
    
    # Input URL tujuan upload
    url = input("Masukkan URL tujuan upload (contoh: https://example.com/upload): ")
    
    # Input path file yang akan diunggah
    file_path = input("Masukkan path file yang akan diunggah: ")
    
    # Validasi path file
    if not os.path.isfile(file_path):
        print("File tidak ditemukan. Pastikan path file benar.")
    else:
        # Panggil fungsi upload_file
        result = upload_file(url, file_path)
        print(result)

if __name__ == '__main__':
    main()