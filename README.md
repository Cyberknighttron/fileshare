# Secure File Share

A minimal, dark-themed, password-protected file sharing web application built with **Flask**. This app allows you to upload, preview, download, and password-protect files, with auto-cleanup for inactive files.

---

## Features

* **Secure Access:** Global app password for authentication.
* **Per-File Passwords:** Optional password protection for individual files.
* **Auto Cleanup:** Files automatically deleted after 2 minutes of inactivity.
* **Preview & Download:** View or download individual files.
* **Bulk Download:** Download multiple selected files as a ZIP archive.
* **Minimal Dark UI:** Responsive, clean, and modern interface.
* **Cross-Device Sync:** Files are shared across all devices on the network (session-independent).

---

## Requirements

* Python 3.8+
* Flask

Install dependencies using:

```bash
pip install flask
```

---

## Setup & Usage

1. **Clone the repository or copy the code:**

```bash
git clone <repo-url>
cd secure-file-share
```

2. **Run the application:**

```bash
python app.py
```

3. **Access the app:**

Open your browser and navigate to:

```
http://localhost:5000
```

4. **Login:**

Use the global app password defined in `APP_PASSWORD` in the code. Example:

```python
APP_PASSWORD = "mypassword"
```

5. **Upload Files:**

* Drag and drop files into the upload area.
* Optionally, add a password for individual file protection.

6. **Download or Preview:**

* Click **💾** to download.
* Click **👁️** to preview.
* Use bulk download to download selected files as a ZIP.

7. **Logout:**

Click the `Logout` button on the top-right to end the session.

---

## Notes

* Files older than 2 minutes are automatically deleted.
* File passwords are optional and stored in memory only.
* All uploads are stored in the `shared` folder.
* The app runs on `0.0.0.0:5000` by default.

---

## License

This project is open-source and free to use.
