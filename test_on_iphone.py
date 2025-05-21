"""
Script to prepare and run the Game of Life for testing on iPhone

This script:
1. Creates a simple HTML page for running the game
2. Deploys it using Pygbag (for WebAssembly)
3. Provides instructions for accessing on an iPhone and recording

Usage:
python test_on_iphone.py
"""

import os
import subprocess
import webbrowser
import http.server
import socketserver
import threading
import time
import shutil

# Check if pygbag is installed
try:
    import pygbag
    print("✅ Pygbag is installed")
except ImportError:
    print("⚠️ Installing pygbag...")
    subprocess.call([sys.executable, "-m", "pip", "install", "pygbag"])

# Create web build directory
web_dir = "web_build"
os.makedirs(web_dir, exist_ok=True)

# Copy the game file to the web directory with the name main.py
shutil.copy("life.py", os.path.join(web_dir, "main.py"))

# Run pygbag to build the web version
print("\n🔄 Building web version using Pygbag...")
try:
    subprocess.run(["pygbag", "--ume_block", "0", "--title", "Game of Life - iPhone 15 Pro", web_dir], 
                  check=True, timeout=60)
    print("✅ Web build completed")
except subprocess.TimeoutExpired:
    print("⚠️ Build process taking longer than expected. Check the build directory.")
except Exception as e:
    print(f"❌ Error building web version: {e}")
    
print("\n📱 Instructions for testing on iPhone:")
print("1. Connect your iPhone to the same WiFi network as this computer")
print("2. Find your computer's IP address")
print("   - On Windows: run 'ipconfig' in command prompt")
print("   - On macOS/Linux: run 'ifconfig' or 'ip addr' in terminal")
print("3. On your iPhone, open Safari and navigate to:")
print("   http://YOUR_IP_ADDRESS:8000")
print("\n📹 To record your screen on iPhone:")
print("1. Open Control Center (swipe down from top-right corner)")
print("2. Press and hold the Record button (circle icon)")
print("3. Tap 'Start Recording' and navigate to the game in Safari")
print("4. When finished, tap the red status bar and select 'Stop'")
print("5. The recording will be saved to your Photos app")

print("\n⏳ Starting local server for testing...")
print("Press Ctrl+C when you're done testing")

# Start the server in a separate thread to keep script running
try:
    os.chdir("build")
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 8000), handler) as httpd:
        print("✅ Server running at http://localhost:8000")
        print("   Access this from your iPhone using your computer's IP address")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n🛑 Server stopped")
except Exception as e:
    print(f"❌ Error starting server: {e}")