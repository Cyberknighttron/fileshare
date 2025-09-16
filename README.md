# 🔒 Secure File Sharing

A lightweight, secure, temporary file sharing web application built with Flask. Perfect for quickly sharing files across devices with automatic cleanup and optional password protection.

## ✨ Features

### 🚀 **Core Functionality**
- **Cross-device sync**: Upload from laptop, access from mobile instantly
- **Multi-file upload**: Drag & drop or select multiple files at once
- **Bulk operations**: Select multiple files for ZIP download
- **File preview**: View files directly in browser before downloading
- **Real-time updates**: Files appear immediately across all devices

### 🔐 **Security Features**
- **Global password protection**: App-level access control
- **Per-file passwords**: Individual password protection for sensitive files
- **Session isolation**: Each user session is completely separate
- **Automatic cleanup**: Files self-destruct after inactivity

### ⏰ **Smart Auto-Cleanup**
- **2-minute rule**: Files auto-delete after 2 minutes of inactivity
- **Heartbeat system**: Active browsers keep files alive automatically  
- **Multi-device protection**: Files stay as long as ANY device is active
- **Background operation**: Cleanup runs automatically, no user intervention needed

### 🎨 **Minimal Dark UI**
- **Clean design**: Distraction-free, professional interface
- **Mobile responsive**: Works perfectly on phones, tablets, and desktops
- **Dark theme**: Easy on the eyes, modern aesthetic
- **Fast loading**: Lightweight CSS, no external dependencies

## 📋 Requirements

- Python 3.6+
- Flask 2.0+
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🚀 Quick Start

### 1. **Installation**
```bash
# Clone or download the project
git clone <repository-url>
cd secure-file-sharing

# Install Flask (if not already installed)
pip install flask

# Run the application
python shareupgraded.py
```

### 2. **Access the Application**
- Open browser and go to: `http://localhost:5000`
- Enter the global password: `mypassword`
- Start uploading and sharing files!

### 3. **Network Access**
To access from other devices on your network:
```bash
# Find your IP address
# Windows: ipconfig
# Mac/Linux: ifconfig

# Access from other devices: http://YOUR_IP:5000
# Example: http://192.168.1.100:5000
```

## 🔧 Configuration

### Change Global Password
Edit the `APP_PASSWORD` variable in the code:
```python
APP_PASSWORD = "your_new_password"  # Change this!
```

### Adjust Auto-Cleanup Timer
Modify cleanup timing in the `cleanup_old_files()` function:
```python
if file_age > 120:  # 120 = 2 minutes, change as needed
```

### Change Heartbeat Frequency
Update heartbeat interval in the JavaScript:
```javascript
setInterval(() => {
    fetch('/heartbeat', { method: 'POST' });
}, 30000);  // 30000 = 30 seconds
```

## 📱 Usage Guide

### **Basic File Sharing**
1. **Upload**: Select files → optionally set password → click Upload
2. **Share**: Files instantly available on all your devices
3. **Download**: Click download button or select multiple for ZIP
4. **Auto-cleanup**: Files delete automatically when inactive

### **Password Protection**
- **No password**: Files accessible to anyone with app access
- **With password**: Additional protection for sensitive files
- **Mixed protection**: Some files can be public, others password-protected

### **Cross-Device Access**
- Upload from laptop → immediately visible on phone
- All devices share the same file pool
- Real-time synchronization across all sessions

### **File Management**
- **Preview**: Click 👁️ to view files in browser
- **Download**: Click 💾 for individual downloads  
- **Bulk download**: Select multiple files → Download ZIP
- **Delete**: Click 🗑️ to remove files manually

## ⚙️ How It Works

### **Architecture**
```
Browser ←→ Flask App ←→ File System
   ↓           ↓           ↓
Heartbeat → Timestamp → Auto-cleanup
```

### **File Lifecycle**
1. **Upload** → File saved to shared folder
2. **Access** → Available across all devices/networks
3. **Activity** → Heartbeat updates file timestamp
4. **Inactivity** → No heartbeat for 2 minutes
5. **Cleanup** → File automatically deleted

### **Security Model**
- **App Level**: Global password protects entire application
- **File Level**: Optional individual password per file
- **Network Level**: Only accessible on your local network (unless exposed)
- **Time Level**: Automatic deletion prevents permanent storage

## 📂 File Structure

```
secure-file-sharing/
│
├── shareupgraded.py      # Main application file
├── shared/               # Auto-created folder for uploaded files
│   ├── file1.pdf        # Uploaded files stored here
│   ├── image.jpg        # Files auto-delete after 2 minutes
│   └── document.docx    # Cross-device accessible
│
└── README.md            # This file
```

## 🛠️ Technical Details

### **Dependencies**
- **Flask**: Web framework
- **Standard Library**: os, zipfile, io, uuid, shutil, time, threading, hashlib

### **Key Components**
- **File Storage**: Simple filesystem storage in `shared/` directory
- **Password Management**: In-memory dictionary for file passwords
- **Cleanup System**: Background thread checking every 30 seconds
- **Heartbeat System**: Browser-to-server keepalive mechanism
- **Cross-device Sync**: Single shared folder for all sessions

### **Supported File Types**
The app recognizes and displays icons for:
- **Documents**: PDF, DOC, DOCX, PPT, PPTX, TXT
- **Images**: JPG, JPEG, PNG, GIF  
- **Code**: PY, C, CPP, JS, JAVA
- **Generic**: Any other file type (📁 icon)

## 🛡️ Privacy-Focused Design

### **Zero Third-Party Dependencies**
This application is built with privacy as the core principle:
- ✅ **No cloud services**: Files never leave your local network
- ✅ **No external APIs**: Zero communication with outside servers
- ✅ **No tracking or analytics**: Your activity is never monitored
- ✅ **No corporate oversight**: You own and control everything
- ✅ **Self-contained**: Runs entirely on your own hardware

### **Complete Data Control**
- ✅ **Local storage only**: Files stored on your own device/server
- ✅ **Automatic cleanup**: 2-minute auto-deletion prevents data accumulation  
- ✅ **No persistent logging**: No record of your file sharing activity
- ✅ **Network isolation**: Only accessible within your local network
- ✅ **Open source**: Full transparency, no hidden functionality

### **Privacy by Design Features**
- ✅ **Temporary sharing**: Files automatically self-destruct
- ✅ **Session-based**: No permanent user accounts or profiles
- ✅ **Minimal data collection**: Only stores what's necessary for operation
- ✅ **Local authentication**: Passwords never sent to external services
- ✅ **No metadata retention**: File information deleted with cleanup

### **Security Considerations**

#### **Privacy Strengths**
- ✅ Password-protected access (app + individual files)
- ✅ Automatic file cleanup prevents data persistence
- ✅ Session isolation between users
- ✅ No third-party data sharing
- ✅ Complete local control

#### **Technical Limitations**
- ⚠️ Files stored unencrypted on local disk
- ⚠️ No HTTPS by default (local network use)
- ⚠️ Basic authentication system
- ⚠️ No secure deletion (files not overwritten)

#### **Ideal Use Cases**
- ✅ **Privacy-conscious file sharing**
- ✅ **Local network collaboration** 
- ✅ **Temporary document exchange**
- ✅ **Cross-device transfer within your network**
- ✅ **Quick sharing without cloud services**

#### **Not Suitable For**
- ❌ **Public internet deployment**
- ❌ **Highly classified documents** (without additional encryption)
- ❌ **Permanent file storage**
- ❌ **Large-scale file sharing**

### **Privacy Enhancement Options**
For maximum privacy, consider these additional measures:

```python
# Disable all logging
import logging
logging.getLogger('werkzeug').setLevel(logging.ERROR)
app.logger.disabled = True

# Add no-cache headers
@app.after_request
def no_cache(response):
    response.headers['Cache-Control'] = 'no-cache, no-store'
    return response
```

**🔐 Privacy Score: 9/10** - Excellent for users who want complete control over their file sharing without relying on third-party services.

## 🚨 Troubleshooting

### **Files Not Appearing on Other Devices**
- Check if both devices use the same app password
- Verify devices are on the same network
- Ensure the server is running and accessible

### **Files Disappearing Too Quickly**
- Check if browser is actually closed (background tabs count as active)
- Verify heartbeat is working (check browser console)
- Confirm 2-minute timeout hasn't elapsed

### **Cannot Access from Mobile**
- Find your computer's IP address
- Use `http://YOUR_IP:5000` instead of localhost
- Check firewall settings aren't blocking port 5000

### **Upload Failures**
- Check file size (very large files may timeout)
- Verify disk space is available
- Ensure `shared/` folder permissions are correct

## 🔄 Customization Ideas

### **Extended Features**
- **File size limits**: Add maximum file size restrictions
- **User accounts**: Replace global password with user system
- **Encryption**: Encrypt files at rest
- **Upload progress**: Show progress bars for large files
- **File categories**: Organize files into folders

### **UI Enhancements**
- **Drag & drop zone**: Visual file dropping area
- **File thumbnails**: Preview images directly in list
- **Search functionality**: Find files by name
- **Sorting options**: Sort by date, name, size, type

### **Advanced Security**
- **HTTPS support**: SSL certificate integration
- **Rate limiting**: Prevent abuse with upload limits
- **IP whitelisting**: Restrict access to specific networks
- **Audit logging**: Track all file operations

## 📄 License

This project is provided as-is for educational and personal use. Feel free to modify and adapt for your needs.

## 🤝 Contributing

This is a simple, self-contained project perfect for:
- Learning Flask development
- Understanding file handling in web apps
- Exploring real-time web features
- Practicing security concepts

---

**⚡ Quick Command Reference:**
```bash
# Start server
python shareupgraded.py

# Access locally
http://localhost:5000

# Access from network
http://YOUR_IP:5000

# Default password
mypassword
```

**🔐 Remember:** This is designed for temporary, local network file sharing. Always consider your security requirements before use!
