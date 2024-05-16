import http.server
import socketserver
import webbrowser
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import threading
import time

# Global PORT
PORT = 8000

class MyServer(threading.Thread):
    def run(self):
        self.server = ThreadingHTTPServer(('localhost', PORT), SimpleHTTPRequestHandler)
        self.server.serve_forever()
    def stop(self):
        self.server.shutdown()

def open_browser(url):
    print(f"Opening web browser to URL: {url}")
    webbrowser.open(url)

def connect_bluetooth():
    URL = f"http://127.0.0.1:{PORT}/connect_dwarf.html"

    # Start processing requests
    server = MyServer()
    server.start()

    time.sleep(3)  # Adjust delay as needed
    
    try:
        # Open the web page in the default web browser
        open_browser(URL)

        # Wait for user input to stop the server
        input("Press Enter to stop the server...")

    except KeyboardInterrupt:
        # Handle Ctrl+C to stop the server
        pass
    finally:
        # Stop the server (set server_running flag)
        server.stop()

    # Optional: Add additional delay or cleanup steps if needed
    time.sleep(3)

