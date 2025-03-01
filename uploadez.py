import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_upload_forms(url):
    """
    Mencari form upload di halaman website.
    :param url: URL website yang akan diperiksa.
    :return: List of dictionaries berisi informasi form upload.
    """
    try:
        # Ambil konten HTML dari website
        response = requests.get(url)
        response.raise_for_status()  # Raise exception jika status code bukan 200
        soup = BeautifulSoup(response.text, "html.parser")

        # Cari semua form dengan enctype "multipart/form-data"
        forms = soup.find_all("form", attrs={"enctype": "multipart/form-data"})

        if not forms:
            print("Tidak ada form upload yang ditemukan.")
            return []

        print(f"Ditemukan {len(forms)} form upload.")
        form_info = []

        for form in forms:
            # Dapatkan action URL (endpoint tujuan upload)
            action = form.get("action", "")
            action_url = urljoin(url, action)  # Handle relative URL

            # Dapatkan metode HTTP (GET/POST)
            method = form.get("method", "GET").upper()

            # Cari input file di dalam form
            file_inputs = form.find_all("input", attrs={"type": "file"})
            if not file_inputs:
                print("Form ditemukan, tetapi tidak ada field untuk upload file.")
                continue

            # Simpan informasi form
            form_data = {
                "action_url": action_url,
                "method": method,
                "file_inputs": [input.get("name") for input in file_inputs],
            }
            form_info.append(form_data)
            print(f"Form ditemukan: {form_data}")

        return form_info

    except requests.exceptions.RequestException as e:
        print(f"Error saat mengakses website: {e}")
        return []

def upload_file(url, file_path, field_name="file", method="POST"):
    """
    Mengunggah file ke endpoint yang diberikan.
    :param url: URL tujuan upload.
    :param file_path: Path file yang akan diunggah.
    :param field_name: Nama field untuk upload file.
    :param method: Metode HTTP (POST/GET).
    :return: None
    """
    try:
        with open(file_path, "rb") as file:
            files = {field_name: file}
            if method == "POST":
                response = requests.post(url, files=files)
            else:
                response = requests.get(url, files=files)
            print("\nHasil Upload:")
            print(f"Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
    except FileNotFoundError:
        print(f"File {file_path} tidak ditemukan.")
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengunggah file: {e}")

def main():
    # Masukkan URL website yang akan diperiksa
    website_url = input("Masukkan URL website (contoh: https://example.com): ").strip()

    # Cari form upload di website
    upload_forms = find_upload_forms(website_url)

    if upload_forms:
        print("\nForm upload ditemukan:")
        for i, form in enumerate(upload_forms, start=1):
            print(f"\nForm {i}:")
            print(f"  - URL Tujuan: {form['action_url']}")
            print(f"  - Metode HTTP: {form['method']}")
            print(f"  - Field Upload: {', '.join(form['file_inputs'])}")

            # Coba unggah file ke form ini
            file_to_upload = input("Masukkan path file .jpg yang akan diunggah: ").strip()
            if file_to_upload.lower().endswith(".jpg"):
                for field_name in form["file_inputs"]:
                    print(f"\nMengunggah file ke {form['action_url']} menggunakan field '{field_name}'...")
                    upload_file(form["action_url"], file_to_upload, field_name, form["method"])
            else:
                print("File harus berekstensi .jpg.")
    else:
        print("Tidak ada form upload yang ditemukan.")

if __name__ == "__main__":
    main()