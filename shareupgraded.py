from flask import Flask, request, send_from_directory, render_template_string, redirect, url_for, send_file, session
import os, zipfile, io, uuid, threading, time, shutil

app = Flask(__name__)
app.secret_key = "supersecretkey"  # needed for session cookies
BASE_FOLDER = os.path.abspath("shared")
os.makedirs(BASE_FOLDER, exist_ok=True)

# store passwords for files { session_id: { filename: password or None } }
file_passwords = {}

# track last activity for cleanup
last_active = {}
SESSION_TIMEOUT = 600  # 10 minutes


def get_icon(filename):
    ext = filename.split(".")[-1].lower()
    icons = {
        "pdf": "📕",
        "doc": "📄", "docx": "📄",
        "ppt": "📊", "pptx": "📊",
        "py": "🐍",
        "c": "💻", "cpp": "💻",
        "js": "📜",
        "java": "☕",
        "txt": "📝",
        "jpg": "🖼️", "jpeg": "🖼️", "png": "🖼️", "gif": "🖼️"
    }
    return icons.get(ext, "📁")


def get_session_id():
    if "id" not in session:
        session["id"] = str(uuid.uuid4())
    return session["id"]


def user_folder():
    sid = get_session_id()
    path = os.path.join(BASE_FOLDER, sid)
    os.makedirs(path, exist_ok=True)
    last_active[sid] = time.time()
    return path


def cleanup_sessions():
    while True:
        now = time.time()
        for sid, ts in list(last_active.items()):
            if now - ts > SESSION_TIMEOUT:
                shutil.rmtree(os.path.join(BASE_FOLDER, sid), ignore_errors=True)
                file_passwords.pop(sid, None)
                del last_active[sid]
        time.sleep(60)


threading.Thread(target=cleanup_sessions, daemon=True).start()

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>📂 File Share</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
    body { background-color: #1e1e2f; color: #eee; }
    .container { max-width: 700px; margin-top: 60px; }
    .card { border-radius: 12px; background-color: #2c2c3c; box-shadow: 0px 4px 15px rgba(0,0,0,0.3); }
    h2 { color: #fff; }
    h5 { color: #4fc3f7; font-weight: 600; margin-top: 20px; border-bottom: 2px solid #4fc3f7; padding-bottom: 6px; }
    .file-list a { text-decoration: none; font-weight: 500; color: #9cdcfe; }
    .file-list li { padding: 8px; border-bottom: 1px solid #444; display: flex; align-items: center; justify-content: space-between; }
    .file-list li:last-child { border-bottom: none; }
    .file-icon { margin-right: 10px; font-size: 1.2em; }
    .delete-btn { font-size: 0.8em; }
    .preview-img { max-height: 50px; margin-left: 10px; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="card p-4">
            <h2 class="text-center mb-4">📂 File Share</h2>
            
            <!-- Upload Form -->
            <form id="upload-form" method="post" enctype="multipart/form-data" class="mb-3">
                <div class="mb-2">
                    <input id="file-input" class="form-control" type="file" name="files" multiple required accept="*/*">
                </div>
                <div class="mb-2">
                    <input class="form-control" type="text" name="password" placeholder="Set password (optional)">
                </div>
                <button class="btn btn-primary" type="submit">Upload</button>
            </form>
            
            <h5>Available Files:</h5>
            <form method="post" action="/download-zip">
                <ul class="file-list list-unstyled">
                    {% for file, icon in files %}
                        <li>
                            <span>
                                <input type="checkbox" name="selected_files" value="{{ file }}">
                                <span class="file-icon">{{ icon }}</span>
                                <a href="{{ url_for('download', filename=file) }}" target="_blank">{{ file }}</a>
                                {% if file.endswith(('.png','.jpg','.jpeg','.gif')) %}
                                    <img src="{{ url_for('preview_file', filename=file) }}" class="preview-img">
                                {% endif %}
                                {% if file in protected %}
                                    🔒
                                {% endif %}
                            </span>
                            <a href="{{ url_for('delete_file', filename=file) }}" class="btn btn-danger btn-sm delete-btn">Delete</a>
                        </li>
                    {% endfor %}
                </ul>
                <button class="btn btn-success mt-2" type="submit">Download Selected as ZIP</button>
            </form>
        </div>
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    sid = get_session_id()
    folder = user_folder()
    if request.method == "POST":
        uploaded_files = request.files.getlist("files")
        password = request.form.get("password") or None
        for uploaded_file in uploaded_files:
            if uploaded_file:
                path = os.path.join(folder, uploaded_file.filename)
                uploaded_file.save(path)
                file_passwords.setdefault(sid, {})[uploaded_file.filename] = password
    files = [(f, get_icon(f)) for f in os.listdir(folder)]
    protected = [f for f, p in file_passwords.get(sid, {}).items() if p]
    return render_template_string(HTML, files=files, protected=protected)


@app.route("/download/<filename>", methods=["GET", "POST"])
def download(filename):
    sid = get_session_id()
    folder = user_folder()
    password = file_passwords.get(sid, {}).get(filename)
    if password:  # file has a password
        if request.method == "GET":
            return f"""
            <form method="post">
                <p>Enter password to download <b>{filename}</b>:</p>
                <input type="password" name="password">
                <button type="submit">Download</button>
            </form>
            """
        elif request.method == "POST":
            if request.form.get("password") == password:
                return send_from_directory(folder, filename, as_attachment=True)
            else:
                return "❌ Wrong password!"
    else:
        return send_from_directory(folder, filename, as_attachment=True)


@app.route("/preview/<filename>")
def preview_file(filename):
    return send_from_directory(user_folder(), filename)


@app.route("/download-zip", methods=["POST"])
def download_zip():
    folder = user_folder()
    selected_files = request.form.getlist("selected_files")
    if not selected_files:
        return redirect(url_for("home"))
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for file in selected_files:
            filepath = os.path.join(folder, file)
            if os.path.exists(filepath):
                zipf.write(filepath, arcname=file)
    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype="application/zip",
                     as_attachment=True, download_name="files.zip")


@app.route("/delete/<filename>")
def delete_file(filename):
    folder = user_folder()
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        os.remove(path)
        sid = get_session_id()
        file_passwords.get(sid, {}).pop(filename, None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
