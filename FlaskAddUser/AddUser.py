import os
import threading
from functools import wraps
from flask import Flask, request, render_template_string, send_from_directory, Response
from werkzeug.serving import make_server
from werkzeug.utils import secure_filename


class FileServer(threading.Thread):
    def __init__(self, bind_host,auth_username, auth_passkey, port=5000, upload_folder="AuthUsers", max_files = 5):
        super().__init__()
        self.bind_host = bind_host
        self.port = port
        self.max_files = max_files
        self.next_slot = 0
        self.auth_username = auth_username
        self.auth_passkey = auth_passkey


        # ensure upload folder exists
        base = os.path.abspath(os.path.dirname(__file__))
        self.upload_folder = os.path.join(base, upload_folder)
        os.makedirs(self.upload_folder, exist_ok=True)

        # build Flask app
        self.app = Flask(__name__)
        self._setup_routes()

        # create a WSGI server for controlled startup/shutdown
        self.server = make_server(self.bind_host, self.port, self.app)
        self.ctx = self.app.app_context()
        self.ctx.push()

        # mark thread as daemon if you want it to die on main thread exit
        self.daemon = True

    def _auth(self, user, passkey):
        return user == self.auth_username and passkey == self.auth_passkey

    def _authenticate(self):
        """Send 401 response to enable basic authentication."""
        return Response(
            "Authentication required", 401,
            {"WWW-Authenticate": 'Basic realm="Login Required"'}
        )

    def _require_auth(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not self._auth(auth.username, auth.password):
                return self._authenticate()
            return f(*args, **kwargs)
        return decorated

    def _setup_routes(self):
        HTML = """
        <!doctype html><title>Prometheus Auth User Add</title>
        <h1>Upload User Encodings To Your Device</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        <h2>Known Users:</h2><ul>
        {% for fn in files %}
          <li><a href="/uploads/{{fn}}">{{fn}}</a></li>
          <img src="/uploads/{{fn}}"/>
        {% endfor %}
        </ul>
        """

        @self.app.route("/", methods=["GET", "POST"])
        @self._require_auth
        def index():
            if request.method == "POST":
                f = request.files.get("file")
                if f and f.filename:
                    # ring-buffer naming
                    ext = os.path.splitext(secure_filename(f.filename))[1] or ""
                    slotname = f"AuthUser{self.next_slot}{ext}"
                    dest = os.path.join(self.upload_folder, slotname)
                    f.save(dest)
                    self.next_slot = (self.next_slot + 1) % self.max_files
            files = sorted(os.listdir(self.upload_folder))
            return render_template_string(HTML, files=files, max_files = self.max_files)

        @self.app.route("/uploads/<path:filename>")
        @self._require_auth
        def serve_file(filename):
            return send_from_directory(self.upload_folder, filename, as_attachment=True)

    def run(self):
        """Thread entry point – blocks here serving requests."""
        print(f"[Flask Server] Starting file server on http://{self.bind_host}:{self.port}\n")
        self.server.serve_forever()

    def shutdown(self):
        """Stop the WSGI server and clean up."""
        print("[Flask Server] Shutting down file server...")
        self.server.shutdown()
        self.ctx.pop()

if __name__ == "__main__":
    fs = FileServer(bind_host="10.181.114.19", auth_username='Admin',auth_passkey='passkey')
    fs.start()              # daemon thread serving HTTP
    print("Server is running. Press ENTER to stop.")
    input()
    fs.shutdown()
    print("Done.")