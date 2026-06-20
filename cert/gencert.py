import socket
import subprocess


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
finally:
    s.close()

config = f"""
[req]
default_bits = 4096
prompt = no
default_md = sha256
distinguished_name = dn
x509_extensions = v3_req

[dn]
CN = {ip}

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
IP.1 = 127.0.0.1
IP.2 = {ip}
"""

with open("openssl.cnf", "w") as f:
    f.write(config)


subprocess.run(
    [
        "openssl",
        "req",
        "-x509",
        "-nodes",
        "-days", "3650",
        "-newkey", "rsa:4096",
        "-keyout", "server.key",
        "-out", "server.crt",
        "-config", "openssl.cnf",
        "-extensions", "v3_req",
    ],
    check=True,
)