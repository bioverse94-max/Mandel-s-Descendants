from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

def generate_self_signed_cert(
    common_name: str,
    country: str = "US",
    state: str = "California",
    locality: str = "San Francisco",
    org: str = "BioVerse",
    org_unit: str = "Engineering",
    valid_days: int = 365
):
    """Generate a self-signed certificate and private key"""
    
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    
    # Generate public key
    public_key = private_key.public_key()
    
    # Create builder
    builder = x509.CertificateBuilder()
    
    # Add certificate details
    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
        x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, org),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, org_unit),
    ]))
    
    builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ]))
    
    # Set validity period
    builder = builder.not_valid_before(datetime.today() - timedelta(days=1))
    builder = builder.not_valid_after(datetime.today() + timedelta(days=valid_days))
    
    # Set serial number
    builder = builder.serial_number(x509.random_serial_number())
    
    # Add extensions
    builder = builder.add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName(common_name),
            x509.DNSName("localhost"),
            x509.IPAddress(ip_address("127.0.0.1")),
        ]),
        critical=False
    )
    
    builder = builder.add_extension(
        x509.BasicConstraints(ca=True, path_length=None),
        critical=True,
    )
    
    # Sign the certificate
    certificate = builder.sign(
        private_key=private_key,
        algorithm=hashes.SHA256()
    )
    
    return private_key, certificate

def save_cert_and_key(
    cert_path: str,
    key_path: str,
    private_key,
    certificate
):
    """Save certificate and private key to files"""
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(cert_path), exist_ok=True)
    os.makedirs(os.path.dirname(key_path), exist_ok=True)
    
    # Save private key
    with open(key_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # Save certificate
    with open(cert_path, "wb") as f:
        f.write(certificate.public_bytes(
            encoding=serialization.Encoding.PEM
        ))

def setup_certificates(domain: str = "bioverse.local"):
    """Set up certificates for the application"""
    
    cert_dir = "certs"
    key_path = os.path.join(cert_dir, "private.key")
    cert_path = os.path.join(cert_dir, "certificate.crt")
    
    # Generate certificate and key
    private_key, certificate = generate_self_signed_cert(domain)
    
    # Save to files
    save_cert_and_key(cert_path, key_path, private_key, certificate)
    
    return cert_path, key_path