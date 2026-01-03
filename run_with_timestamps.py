#!/usr/bin/env python3
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

LOG_PATH = Path('/tmp/uvicorn_timestamped.log')

def timestamped_lines(proc, out_file):
    for line in proc.stdout:
        try:
            decoded = line.decode('utf-8', errors='replace').rstrip('\n')
        except Exception:
            decoded = str(line).rstrip('\n')
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        out_file.write(f"{ts} {decoded}\n")
        out_file.flush()

def main():
    host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    port = sys.argv[2] if len(sys.argv) > 2 else '7000'

    cmd = [sys.executable, '-m', 'uvicorn', 'wespider_api.wespider_api.app:app', '--host', host, '--port', port]

    with LOG_PATH.open('a', encoding='utf-8') as out_file:
        # Start uvicorn subprocess
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        try:
            timestamped_lines(proc, out_file)
        except KeyboardInterrupt:
            proc.terminate()
            proc.wait(timeout=5)

if __name__ == '__main__':
    main()
