import os


def get_cert_type() -> str:
    return os.environ.get('CERT_TYPE') or 'es256'


def get_cert_path() -> str:
    return os.environ.get('CERT') or os.path.join(
        os.path.dirname(__file__),
        'certs', 'sample', 'es256_certs.pem')


def get_private_key_path() -> str:
    return os.environ.get('CERT_PRIVATE_KEY') or os.path.join(
        os.path.dirname(__file__),
        'certs', 'sample', 'es256_private.key')
