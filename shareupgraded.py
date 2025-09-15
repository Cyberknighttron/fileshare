from flask import Flask, request, send_from_directory, render_template_string, redirect, url_for, send_file, session
import os, zipfile, io, uuid, shutil, hashlib

app = Flask(__name__)
app.secret_key = "supersecretkey"

BASE_UPLOAD_FOLDER = os.path.abspath("shared")
os.makedirs(BASE_UPLOAD_FOLDER, exist_ok=True)

# Global app password
APP_PASSWORD = "mypassword"

# Store per-file passwords globally {filename: password}
file_passwords = {}

def get_icon(filename):
    ext = filename.split(".")[-1].lower()
    icons = {
        "pdf": "📕", "doc": "📄", "docx": "📄", "ppt": "📊", "pptx": "📊",
        "py": "🐍", "c": "💻", "cpp": "💻", "js": "📜", "java": "☕",
        "txt": "📝", "jpg": "🖼️", "jpeg": "🖼️", "png": "🖼️", "gif": "🖼️"
    }
    return icons.get(ext, "📁")

# ------------------- Auto-cleanup for old files -------------------
import time, threading

def cleanup_old_files():
    """Remove files older than 2 minutes"""
    while True:
        try:
            current_time = time.time()
            if os.path.exists(BASE_UPLOAD_FOLDER):
                for filename in os.listdir(BASE_UPLOAD_FOLDER):
                    filepath = os.path.join(BASE_UPLOAD_FOLDER, filename)
                    if os.path.isfile(filepath):
                        file_age = current_time - os.path.getmtime(filepath)
                        if file_age > 120:  # 2 minutes
                            print(f"🧹 Cleaning up old file: {filename}")
                            os.remove(filepath)
                            file_passwords.pop(filename, None)
        except Exception as e:
            print(f"Error in cleanup: {e}")
        time.sleep(30)  # Check every 30 seconds

cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
cleanup_thread.start()

@app.route("/heartbeat", methods=["POST"])
def heartbeat():
    """Keep files active by updating their timestamp"""
    try:
        for filename in os.listdir(BASE_UPLOAD_FOLDER):
            filepath = os.path.join(BASE_UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                os.utime(filepath)  # Update file timestamp
    except:
        pass
    return "OK"

# ------------------- Minimal Dark HTML Template -------------------
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔒 File Share</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            background: #0a0a0a;
            color: #e0e0e0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', monospace;
            line-height: 1.4;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: #1a1a1a;
            border-radius: 8px;
            padding: 30px;
            border: 1px solid #333;
        }
        
        h1 { 
            text-align: center; 
            margin-bottom: 30px; 
            color: #fff;
            font-size: 1.5rem;
            font-weight: 300;
        }
        
        .upload-zone {
            border: 2px dashed #444;
            border-radius: 6px;
            padding: 40px 20px;
            text-align: center;
            margin-bottom: 30px;
            background: #111;
            transition: all 0.2s;
        }
        
        .upload-zone:hover {
            border-color: #666;
            background: #161616;
        }
        
        input[type="file"] {
            background: #222;
            border: 1px solid #444;
            color: #e0e0e0;
            padding: 10px;
            border-radius: 4px;
            width: 100%;
            margin-bottom: 15px;
        }
        
        input[type="password"] {
            background: #222;
            border: 1px solid #444;
            color: #e0e0e0;
            padding: 10px;
            border-radius: 4px;
            width: 100%;
            margin-bottom: 15px;
        }
        
        input::placeholder { color: #888; }
        
        button {
            background: #333;
            border: 1px solid #555;
            color: #e0e0e0;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        button:hover {
            background: #444;
            border-color: #666;
        }
        
        .btn-primary { background: #2d5a27; border-color: #4a7c59; }
        .btn-primary:hover { background: #4a7c59; }
        
        .btn-danger { background: #5a2d2d; border-color: #7c4a4a; }
        .btn-danger:hover { background: #7c4a4a; }
        
        .logout {
            float: right;
            font-size: 0.9rem;
            color: #888;
            text-decoration: none;
            border: 1px solid #444;
            padding: 5px 10px;
            border-radius: 4px;
        }
        
        .logout:hover { color: #e0e0e0; border-color: #666; }
        
        .file-item {
            background: #222;
            border: 1px solid #333;
            border-radius: 4px;
            padding: 15px;
            margin: 10px 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .file-info {
            display: flex;
            align-items: center;
            flex: 1;
        }
        
        .file-icon {
            font-size: 1.2rem;
            margin-right: 10px;
        }
        
        .file-name {
            color: #fff;
            margin-right: 10px;
        }
        
        .protected {
            background: #3a1a1a;
            color: #ff9999;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 0.8rem;
            margin-left: 10px;
        }
        
        .file-actions {
            display: flex;
            gap: 8px;
        }
        
        .file-actions button {
            font-size: 0.85rem;
            padding: 6px 12px;
        }
        
        .stats {
            background: #111;
            border: 1px solid #333;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
            text-align: center;
            color: #aaa;
        }
        
        .bulk-actions {
            margin: 20px 0;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .empty-state {
            text-align: center;
            color: #666;
            padding: 60px 20px;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        label {
            color: #ccc;
            display: block;
            margin-bottom: 5px;
            font-size: 0.9rem;
        }
        
        .form-text {
            font-size: 0.8rem;
            color: #888;
            margin-top: 5px;
        }
        
        input[type="checkbox"] {
            margin-right: 10px;
        }
        
        @media (max-width: 600px) {
            .container { padding: 15px; }
            .file-item { flex-direction: column; gap: 10px; }
            .file-actions { justify-content: center; }
            .bulk-actions { flex-direction: column; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 Secure File Share</h1>
        <a href="{{ url_for('logout') }}" class="logout">Logout</a>
        <div style="clear: both;"></div>

        <!-- Upload -->
        <div class="upload-zone">
            <form method="POST" enctype="multipart/form-data">
                <div class="form-group">
                    <input type="file" name="files" multiple required>
                </div>
                <div class="form-group">
                    <label>🔐 Password (optional)</label>
                    <input type="password" name="password" placeholder="Leave empty for no protection">
                    <div class="form-text">Files will be shared across all your devices</div>
                </div>
                <button type="submit" class="btn-primary">📤 Upload</button>
            </form>
        </div>

        <!-- Files -->
        {% if files %}
        <div class="stats">
            📊 {{ files|length }} files uploaded
            {% if protected %} • {{ protected|length }} password protected{% endif %}
        </div>

        <form method="POST" action="{{ url_for('download_zip') }}">
            <div class="bulk-actions">
                <button type="button" onclick="selectAll()">✅ Select All</button>
                <button type="button" onclick="selectNone()">❌ Clear</button>
                <button type="submit" class="btn-primary">📦 Download ZIP</button>
            </div>

            {% for filename, icon in files %}
            <div class="file-item">
                <div class="file-info">
                    <input type="checkbox" name="selected_files" value="{{ filename }}">
                    <span class="file-icon">{{ icon }}</span>
                    <span class="file-name">{{ filename }}</span>
                    {% if filename in protected %}
                    <span class="protected">🔒 Protected</span>
                    {% endif %}
                </div>
                <div class="file-actions">
                    <button type="button" onclick="window.open('{{ url_for('preview_file', filename=filename) }}')">👁️</button>
                    <button type="button" onclick="location.href='{{ url_for('download', filename=filename) }}'">💾</button>
                    <button type="button" class="btn-danger" onclick="if(confirm('Delete {{ filename }}?')) location.href='{{ url_for('delete_file', filename=filename) }}'">🗑️</button>
                </div>
            </div>
            {% endfor %}
        </form>
        {% else %}
        <div class="empty-state">
            <h3>📂 No files yet</h3>
            <p>Upload files above - they'll sync across all your devices</p>
        </div>
        {% endif %}

        <div style="text-align: center; margin-top: 30px; color: #666; font-size: 0.85rem;">
            Files auto-delete after 2 minutes of inactivity
        </div>
    </div>

    <script>
        function selectAll() {
            document.querySelectorAll('input[name="selected_files"]').forEach(cb => cb.checked = true);
        }
        
        function selectNone() {
            document.querySelectorAll('input[name="selected_files"]').forEach(cb => cb.checked = false);
        }

        // Keep files alive with heartbeat
        setInterval(() => {
            fetch('/heartbeat', { method: 'POST' }).catch(() => {});
        }, 30000);
    </script>
</body>
</html>
"""

# ------------------- Login Page -------------------
@app.before_request
def check_global_password():
    if request.endpoint in ("static",):
        return
    if "authenticated" not in session:
        if request.endpoint != "login":
            return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == APP_PASSWORD:
            session["authenticated"] = True
            return redirect(url_for("home"))
        return render_template_string("""
        <div style="background:#0a0a0a;color:#e0e0e0;font-family:monospace;min-height:100vh;display:flex;align-items:center;justify-content:center;">
            <div style="background:#1a1a1a;padding:40px;border-radius:8px;border:1px solid #333;max-width:400px;width:100%;">
                <div style="background:#3a1a1a;color:#ff9999;padding:15px;border-radius:4px;margin-bottom:20px;text-align:center;">
                    ❌ Wrong password
                </div>
                <form method="post">
                    <h3 style="text-align:center;margin-bottom:30px;color:#fff;">🔐 Access Required</h3>
                    <input type="password" name="password" style="width:100%;padding:15px;background:#222;border:1px solid #444;color:#e0e0e0;border-radius:4px;margin-bottom:20px;" placeholder="Enter password" required>
                    <button type="submit" style="width:100%;padding:15px;background:#2d5a27;border:1px solid #4a7c59;color:#e0e0e0;border-radius:4px;cursor:pointer;">Enter</button>
                </form>
            </div>
        </div>
        """)
    
    return render_template_string("""
    <div style="background:#0a0a0a;color:#e0e0e0;font-family:monospace;min-height:100vh;display:flex;align-items:center;justify-content:center;">
        <div style="background:#1a1a1a;padding:40px;border-radius:8px;border:1px solid #333;max-width:400px;width:100%;">
            <form method="post">
                <h3 style="text-align:center;margin-bottom:30px;color:#fff;">🔐 Access Required</h3>
                <input type="password" name="password" style="width:100%;padding:15px;background:#222;border:1px solid #444;color:#e0e0e0;border-radius:4px;margin-bottom:20px;" placeholder="Enter password" required>
                <button type="submit" style="width:100%;padding:15px;background:#2d5a27;border:1px solid #4a7c59;color:#e0e0e0;border-radius:4px;cursor:pointer;">Enter</button>
            </form>
        </div>
    </div>
    """)

# ------------------- Routes -------------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        uploaded_files = request.files.getlist("files")
        password = request.form.get("password") or None
        for uploaded_file in uploaded_files:
            if uploaded_file and uploaded_file.filename:
                # Save to shared folder (not session-specific)
                path = os.path.join(BASE_UPLOAD_FOLDER, uploaded_file.filename)
                uploaded_file.save(path)
                if password:
                    file_passwords[uploaded_file.filename] = password

    # List all files in shared folder
    files = []
    if os.path.exists(BASE_UPLOAD_FOLDER):
        files = [(f, get_icon(f)) for f in os.listdir(BASE_UPLOAD_FOLDER) if os.path.isfile(os.path.join(BASE_UPLOAD_FOLDER, f))]
    
    protected = [f for f, p in file_passwords.items() if p]
    return render_template_string(HTML, files=files, protected=protected)

@app.route("/download/<filename>", methods=["GET", "POST"])
def download(filename):
    password = file_passwords.get(filename)
    file_path = os.path.join(BASE_UPLOAD_FOLDER, filename)
    
    if not os.path.exists(file_path):
        return "❌ File not found!"

    if password:
        if request.method == "GET":
            return render_template_string("""
            <div style="background:#0a0a0a;color:#e0e0e0;font-family:monospace;min-height:100vh;display:flex;align-items:center;justify-content:center;">
                <div style="background:#1a1a1a;padding:40px;border-radius:8px;border:1px solid #333;max-width:400px;width:100%;">
                    <form method="post">
                        <h4 style="text-align:center;margin-bottom:20px;color:#fff;">🔒 Password Required</h4>
                        <p style="text-align:center;color:#aaa;margin-bottom:20px;">{{ filename }}</p>
                        <input type="password" name="password" style="width:100%;padding:15px;background:#222;border:1px solid #444;color:#e0e0e0;border-radius:4px;margin-bottom:20px;" placeholder="Enter file password" required>
                        <button type="submit" style="width:100%;padding:15px;background:#2d5a27;border:1px solid #4a7c59;color:#e0e0e0;border-radius:4px;cursor:pointer;">💾 Download</button>
                        <div style="text-align:center;margin-top:15px;">
                            <a href="{{ url_for('home') }}" style="color:#888;text-decoration:none;">← Back</a>
                        </div>
                    </form>
                </div>
            </div>
            """, filename=filename)
        elif request.method == "POST":
            if request.form.get("password") == password:
                return send_from_directory(BASE_UPLOAD_FOLDER, filename, as_attachment=True)
            else:
                return render_template_string("""
                <div style="background:#0a0a0a;color:#e0e0e0;font-family:monospace;min-height:100vh;display:flex;align-items:center;justify-content:center;">
                    <div style="background:#1a1a1a;padding:40px;border-radius:8px;border:1px solid #333;max-width:400px;width:100%;text-align:center;">
                        <div style="background:#3a1a1a;color:#ff9999;padding:15px;border-radius:4px;margin-bottom:20px;">❌ Wrong password!</div>
                        <a href="{{ url_for('download', filename=filename) }}" style="color:#888;text-decoration:none;">← Try again</a>
                    </div>
                </div>
                """, filename=filename)
    else:
        return send_from_directory(BASE_UPLOAD_FOLDER, filename, as_attachment=True)

@app.route("/preview/<filename>")
def preview_file(filename):
    return send_from_directory(BASE_UPLOAD_FOLDER, filename)

@app.route("/download-zip", methods=["POST"])
def download_zip():
    selected_files = request.form.getlist("selected_files")
    if not selected_files:
        return redirect(url_for("home"))

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for file in selected_files:
            filepath = os.path.join(BASE_UPLOAD_FOLDER, file)
            if os.path.exists(filepath):
                zipf.write(filepath, arcname=file)
    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype="application/zip",
                     as_attachment=True, download_name="files.zip")

@app.route("/delete/<filename>")
def delete_file(filename):
    path = os.path.join(BASE_UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
        file_passwords.pop(filename, None)
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ------------------- Run -------------------
if __name__ == "__main__":
    print("🚀 Starting Secure File Sharing Server")
    print("📁 Files will auto-delete after 2 minutes of inactivity")
    print("🔄 Files sync across all devices/networks")
    app.run(host="0.0.0.0", port=5000, debug=True)
