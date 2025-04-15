import logging
import os
import tempfile
import threading
import time
from contextlib import contextmanager
from http.server import HTTPServer, SimpleHTTPRequestHandler

from synapse_sdk.utils.network import get_available_ports_host


class SingleFileHttpServer(SimpleHTTPRequestHandler):
    """
    Custom HTTP request handler that serves a single specified file
    regardless of the request path.
    """

    def __init__(self, *args, file_path=None, content_type=None, **kwargs):
        self.file_path = file_path
        self.content_type = content_type
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests by serving the single file."""
        try:
            # Always serve the specified file regardless of the path requested
            self.send_response(200)
            if self.content_type:
                self.send_header('Content-type', self.content_type)
            self.send_header('Content-Length', str(os.path.getsize(self.file_path)))
            self.end_headers()

            with open(self.file_path, 'rb') as file:
                self.wfile.write(file.read())

        except Exception as e:
            self.send_error(500, str(e))


@contextmanager
def temp_file_server(image=None, file_path=None, format='JPEG', host='0.0.0.0', port=None, content_type=None):
    """
    Context manager that serves a file temporarily via HTTP.

    Args:
        image: A PIL Image object to serve (optional)
        file_path: Path to an existing file to serve (optional - used if image not provided)
        format: Image format when saving a PIL Image (default: "JPEG")
        host: Host to serve on (default: "0.0.0.0")
        port: Port to serve on (default: auto-selected free port)
        content_type: Content type header (default: auto-detected based on format)

    Returns:
        URL where the file is being served

    Usage:
        with temp_file_serve(image=my_pillow_img) as url:
            # use url to access the image
            print(f"Image available at: {url}")
    """
    if image is None and file_path is None:
        raise ValueError('Either image or file_path must be provided')

    # Use a free port if none specified
    if port is None:
        port = get_available_ports_host(start_port=8991, end_port=8999)

    temp_dir = None

    try:
        if image is not None:
            temp_dir = tempfile.mkdtemp()
            ext_map = {'JPEG': '.jpg', 'PNG': '.png', 'GIF': '.gif', 'WEBP': '.webp'}
            content_type_map = {'JPEG': 'image/jpeg', 'PNG': 'image/png', 'GIF': 'image/gif', 'WEBP': 'image/webp'}

            ext = ext_map.get(format, '.jpg')
            if content_type is None:
                content_type = content_type_map.get(format, 'image/jpeg')

            temp_file_path = os.path.join(temp_dir, f'temp_image{ext}')
            image.save(temp_file_path, format=format)
            file_path = temp_file_path

        def handler(*args, **kwargs):
            return SingleFileHttpServer(*args, file_path=file_path, content_type=content_type, **kwargs)

        server = HTTPServer((host, port), handler)

        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        time.sleep(0.1)

        url = f'http://localhost:{port}'

        try:
            yield url
        finally:
            server.shutdown()
            server.server_close()

    finally:
        if temp_dir:
            try:
                if temp_file_path and os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                os.rmdir(temp_dir)
            except Exception as e:
                logging.warning(f'Error cleaning up temporary files: {e}')
