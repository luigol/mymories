#!/usr/bin/env python3
"""
Simple HTTP Server for Mymory
Serves the files locally to avoid CORS issues
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

def start_server():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Set up the server
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("=" * 50)
            print("Mymory Local Server")
            print("=" * 50)
            print(f"Server running at: http://localhost:{PORT}")
            print(f"Serving directory: {script_dir}")
            print("")
            print("Your files:")
            print(f"  • Main page: http://localhost:{PORT}/index.html")
            print(f"  • Memories: http://localhost:{PORT}/mymory.html")
            print(f"  • Goals: http://localhost:{PORT}/goals.html")
            print(f"  • Bitcoin: http://localhost:{PORT}/bitcoin.html")
            print("")
            print("To update bubbles:")
            print("  1. Create new bubble folders")
            print("  2. Run: python scan_bubbles.py")
            print("  3. Refresh browser")
            print("")
            print("Press Ctrl+C to stop the server")
            print("=" * 50)
            
            # Try to open browser automatically
            try:
                webbrowser.open(f'http://localhost:{PORT}/index.html')
                print("Browser opened automatically!")
            except:
                print("Could not open browser automatically")
                print("   Please open: http://localhost:8000/index.html")
            
            print("")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\nServer stopped. Goodbye!")
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"ERROR: Port {PORT} is already in use!")
            print("   Try closing other applications or use a different port.")
        else:
            print(f"ERROR: Error starting server: {e}")

if __name__ == "__main__":
    start_server()
