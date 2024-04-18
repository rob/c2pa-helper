import os

import c2pa
from config import get_cert_path, get_cert_type, get_private_key_path
from lib.manifest import generate_manifest


def sign_file(media_path: str, output_path: str) -> None:
    cert_path = get_cert_path()
    if not cert_path or not os.path.exists(cert_path):
        raise FileNotFoundError("Certificate path not found or not provided.")

    private_key_path = get_private_key_path()
    if not private_key_path or not os.path.exists(private_key_path):
        raise FileNotFoundError("Private key path not found or not provided.")

    media_path = os.path.normpath(media_path)
    if not os.path.exists(media_path):
        raise FileNotFoundError("Media path not found.")

    output_path = os.path.normpath(output_path)

    with open(os.path.normpath(cert_path), "rb") as cert_file:
        certs: bytes = cert_file.read()

    with open(os.path.normpath(private_key_path), "rb") as key_file:
        prv_key: bytes = key_file.read()

    cert_timestamp_url = os.environ.get('CERT_TIMESTAMP_URL', "https://timestamp.digicert.com")

    signer = c2pa.SignerInfo(get_cert_type(), certs, prv_key, cert_timestamp_url)

    manifest = generate_manifest(media_path)

    if not manifest:
        raise RuntimeError("Manifest not found or not provided.")

    c2pa.sign_file(media_path, output_path, manifest, signer, None)
