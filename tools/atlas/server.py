from __future__ import annotations
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os

STORE = os.path.join(os.getcwd(), "atlas_store")
os.makedirs(STORE, exist_ok=True)

HOST, PORT = "0.0.0.0", 8790

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(obj).encode())

    def do_GET(self):
        if self.path == "/cards":
            cards = []
            for f in os.listdir(STORE):
                if f.endswith(".json"):
                    with open(os.path.join(STORE, f), "r") as fh:
                        cards.append(json.load(fh))
            return self._send(200, {"cards": cards})
        return self._send(404, {"error": "not_found"})

    def do_POST(self):
        if self.path != "/cards":
            return self._send(404, {"error": "not_found"})
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        card = json.loads(body.decode() or "{}")

        name = card.get("title", "card").replace(" ", "_") + ".json"
        with open(os.path.join(STORE, name), "w") as f:
            json.dump(card, f, indent=2)

        return self._send(200, {"ok": True})

def run():
    httpd = HTTPServer((HOST, PORT), Handler)
    print(f"Atlas server on http://{HOST}:{PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
