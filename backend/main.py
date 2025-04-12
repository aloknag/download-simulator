# server.py
from flask import Flask, Response, jsonify, request, redirect, abort
from flask_cors import CORS
import os
import time

app = Flask(__name__)
CORS(app)

@app.route("/healthcheck")
def health():
    return jsonify(status="ok")

@app.route("/api/download")
def basic_download():
    size_mb = int(request.args.get("size", 10))
    abort_after_mb = int(request.args.get("abortAfter", size_mb))

    chunk_size = 1024 * 1024
    total_bytes = size_mb * chunk_size
    abort_bytes = abort_after_mb * chunk_size
    bytes_sent = 0

    def stream():
        nonlocal bytes_sent
        while bytes_sent < total_bytes:
            chunk = os.urandom(chunk_size)
            if bytes_sent + chunk_size > abort_bytes:
                yield chunk[:abort_bytes - bytes_sent]
                break
            yield chunk
            bytes_sent += chunk_size
            time.sleep(0.1)

    responds = Response(stream(), mimetype="application/octet-stream")
    # Accept Range for download resumption
    responds.headers["Accept-Ranges"] = "bytes"
    responds.headers["Content-Disposition"] = "attachment; filename=file.bin"
    responds.headers["Content-Length"] = total_bytes
    return responds


@app.route('/api/download-no-length')
def download_no_content_length():
    size_mb = int(request.args.get('size', 10))
    chunk_size = 1024 * 1024  # 1MB

    def generate():
        for _ in range(size_mb):
            yield os.urandom(chunk_size)
            time.sleep(0.1)  # simulate delay

    headers = {
        "Content-Disposition": "attachment; filename=file-no-length.bin",
        # Note: No Content-Length header
    }

    return Response(generate(), headers=headers, mimetype='application/octet-stream')


@app.route('/api/redirect-download')
def redirect_download():
    redirects = int(request.args.get('redirects', 0))
    size_mb = int(request.args.get('size', 10))
    print(f"Redirects: {redirects}, Size: {size_mb} MB")

    if redirects > 0:
        next_url = f"/api/redirect-download?redirects={redirects - 1}&size={size_mb}"
        return redirect(next_url, code=302)

    def generate():
        yield os.urandom(size_mb * 1024 * 1024)

    headers = {
        "Content-Disposition": "attachment; filename=redirected_file.bin"
    }
    return Response(generate(), headers=headers, mimetype='application/octet-stream')


@app.route('/api/download-4xx')
def simulate_4xx():
    try:
        code = int(request.args.get('code', 401))
        message = f"Simulated HTTP {code} error"
        return message, code
    except ValueError:
        return "Invalid code", 400


if __name__ == '__main__':
    app.run(debug=True)
