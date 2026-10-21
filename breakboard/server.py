"""Break board server: one state, a control dock, and an overlay that redraws as the show changes.

Run before going live:  python breakboard/server.py
  OBS dock (Docks > Custom Browser Docks):  http://127.0.0.1:8765/control
  OBS browser source (1080 x 400):          http://127.0.0.1:8765/overlay
State is saved to breakboard/state.json on every change, so a crash or restart mid-break loses nothing.
"""
import json
import queue
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HOST, PORT = '127.0.0.1', 8765
ROOT = Path(__file__).resolve().parent
STATE_FILE = ROOT / 'state.json'
PAGES = {'/control': 'control.html', '/overlay': 'overlay.html', '/common.js': 'common.js'}
TYPES = {'.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8'}

lock = threading.Lock()
listeners = []  # one queue per connected overlay/dock
state = json.loads(STATE_FILE.read_text(encoding='utf-8')) if STATE_FILE.exists() else None


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, code, body, ctype):
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in PAGES:
            path = ROOT / PAGES[self.path]
            self.send(200, path.read_bytes(), TYPES[path.suffix])
        elif self.path == '/state':
            self.send(200, json.dumps(state).encode(), 'application/json')
        elif self.path == '/events':
            self.stream()
        else:
            self.send(404, b'not found', 'text/plain')

    def do_POST(self):
        global state
        if self.path != '/state':
            return self.send(404, b'not found', 'text/plain')
        body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        with lock:
            state = json.loads(body)
            STATE_FILE.write_text(json.dumps(state, indent=2), encoding='utf-8')
            for q in listeners:
                q.put(body)
        self.send(204, b'', 'text/plain')

    def stream(self):
        """Server-sent events: push the full state to every page whenever it changes."""
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        q = queue.Queue()
        with lock:
            listeners.append(q)
            q.put(json.dumps(state).encode())
        try:
            while True:
                try:
                    msg = q.get(timeout=15)
                    self.wfile.write(b'data: ' + msg + b'\n\n')
                except queue.Empty:
                    self.wfile.write(b': ping\n\n')  # keeps idle connections from being dropped
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass
        finally:
            with lock:
                listeners.remove(q)


if __name__ == '__main__':
    print(f'Break board running.\n  Control: http://{HOST}:{PORT}/control\n  Overlay: http://{HOST}:{PORT}/overlay')
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
