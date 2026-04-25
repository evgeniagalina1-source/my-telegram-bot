"""Configuration for certificates required to work with GigaChat API."""

import os

# Path to the Russian government trusted root CA certificate
CERT_PATH = os.path.join(os.path.dirname(__file__), "russian_trusted_root_ca_pem.crt")


def verify_cert_exists():
    """Check if the certificate file exists."""
    return os.path.exists(CERT_PATH)
