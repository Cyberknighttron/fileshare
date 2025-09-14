# File Share (Flask)

A lightweight, privacy-focused file sharing application built with **Flask**.  
It enables users to upload, download, preview, and password-protect files directly through a web interface.  
Designed to run locally, it allows secure file transfers across devices connected to the same network.

---

## Features
- Upload single or multiple files
- Optional password protection for downloads
- Image preview for supported formats (JPG, PNG, GIF)
- Download multiple files as a ZIP archive
- Delete files from the list when no longer needed
- Modern dark-themed user interface
- Runs locally with no external dependencies or databases

---

## Privacy and Security
- All files are stored **locally** in the `shared/` directory
- No third-party servers or cloud storage are involved
- Only devices connected to the **same WiFi or hotspot** can access the application
- Optional password protection adds an extra security layer for sensitive files
- Users remain in full control of their data at all times

---

## Requirements
- Python 3.8 or later  
- Pip (Python package manager)  

Install dependencies globally:
```bash
sudo pip3 install -r requirements.txt
```

---

## Running the Application Locally

Clone the repository:
```bash
git clone https://github.com/cyberknighttron/fileshare.git
cd fileshare
```

Install dependencies:
```bash
sudo pip3 install -r requirements.txt
```

Run the application:
```bash
python3 share.py
```

By default, the application runs at:
- `http://127.0.0.1:5000` – accessible only on the local machine  
- `http://192.168.x.xxx:5000` – accessible to other devices on the same network  

Open the LAN address in a browser on another device (connected to the same network) to access the interface.

---

## Project Structure
```
fileshare/
│── share.py          # Flask application
│── requirements.txt  # Python dependencies
│── README.md         # Documentation
│── shared/           # Uploaded files (auto-created, ignored in Git)
```

---

## Network Access
- The application is designed for **local network use**  
- Other devices on the same LAN or WiFi can access the interface using the server address  
- Global sharing can be achieved with additional tools such as **Ngrok** or by deploying to platforms like **Render**, **Railway**, or **Glitch**

---

## License
This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute it under the terms of this license.
