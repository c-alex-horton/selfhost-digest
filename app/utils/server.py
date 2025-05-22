import http.server
import socketserver
from pathlib import Path
from app.config import config

def serve_content():
    PORT = config["port"]
    output_dir = Path(config["output_path"])
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(output_dir), **kwargs)

    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Serving on http://0.0.0.0:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down.")
            httpd.server_close()

