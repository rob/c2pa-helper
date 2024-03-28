import os

import c2pa
from lib.manifest import get_manifest


def sign_file(media_path: str, output_path: str, data_path) -> None:
    cert_path = os.environ.get('CERT_KEY')
    if not cert_path or not os.path.exists(cert_path):
        raise FileNotFoundError("Certificate path not found or not provided.")

    private_key_path = os.environ.get('CERT_PRIVATE_KEY')
    if not private_key_path or not os.path.exists(private_key_path):
        raise FileNotFoundError("Private key path not found or not provided.")

    media_path = os.path.normpath(media_path)
    if not os.path.exists(media_path):
        raise FileNotFoundError("Media path not found.")

    output_path = os.path.normpath(output_path)

    certs = open(os.path.normpath(cert_path), "rb").read()
    prv_key = open(os.path.normpath(private_key_path), "rb").read()

    cert_timestamp_url = os.environ.get('CERT_TIMESTAMP_URL', "https://timestamp.digicert.com")

    signer = c2pa.SignerInfo("ps256", certs, prv_key, cert_timestamp_url)

    manifest = get_manifest(media_path)

    if not manifest:
        raise RuntimeError("Manifest not found or not provided.")

    c2pa.sign_file(media_path, output_path, manifest, signer, data_path)
