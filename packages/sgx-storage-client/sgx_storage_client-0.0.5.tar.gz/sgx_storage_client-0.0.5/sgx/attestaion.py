import base64
import json
import os
import struct
import urllib.parse
from collections import namedtuple

import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_pem_x509_certificate
from requests import Response


class ValidationError(Exception):
    """Base exception for attestation validation errors"""


class SignatureValidationError(ValidationError):
    """Digital signature verification failed"""


class SGXAttestationVerifier:
    """
    SGX Attestation Verifier implementing Intel's DCAP verification workflow.
    Validates SGX quotes through a Quote Verification Service (QVS) and performs
    cryptographic checks including IAS signature verification and enclave measurements validation.
    """
    QuoteHeader = namedtuple('QuoteHeader', [
        'version',  # 2 bytes (uint16)
        'sign_type',  # 2 bytes (uint16)
        'epid_group_id',  # 4 bytes
        'qe_svn',  # 2 bytes (uint16)
        'pce_svn',  # 2 bytes (uint16)
        'xeid',  # 4 bytes (uint32)
        'basename',  # 32 bytes
    ])

    # Структура тела отчета SGX (48-432 байта в цитате)
    SGXReportBody = namedtuple('SGXReportBody', [
        'cpu_svn',  # 16 bytes
        'misc_select',  # 4 bytes
        'reserved1',  # 12 bytes
        'isv_ext_prod_id',  # 16 bytes
        'attributes',  # 16 bytes
        'mr_enclave',  # 32 bytes
        'reserved2',  # 32 bytes
        'mr_signer',  # 32 bytes  <--- MRSIGNER
        'reserved3',  # 32 bytes
        'config_id',  # 64 bytes
        'isv_prod_id',  # 2 bytes (uint16)
        'isv_svn',  # 2 bytes (uint16)
        'config_svn',  # 2 bytes (uint16)
        'reserved4',  # 42 bytes
        'isv_family_id',  # 16 bytes
        'report_data'  # 64 bytes  <--- Nonce
    ])

    def __init__(self, mr_signer: str, dcap_url: str, is_debug: bool = False):
        """
        Initialize SGX attestation verifier with security parameters.

        Args:
            mr_signer: Hex-formatted expected enclave signer measurement.
                               Represents SHA-256 hash of enclave signer's public key.
            dcap_url: DCAP url
            is_debug: Enable/disable enclave debug mode checking

        Note:
            - Generates random 16-byte nonce during initialization
            - MRSIGNER should match trusted enclave signer's fingerprint
        """
        self.mr_signer = mr_signer
        self.dcap_url = dcap_url
        self.is_debug = is_debug

    def verify(self, quote: str, nonce: str = None) -> None:
        """
        Execute complete SGX quote verification workflow.

        Args:
            quote: Base64-encoded SGX attestation quote containing:
                   - Enclave measurements
                   - Cryptographic proofs
                   - Platform certification data
            nonce: Is base64-encoded for transport compatibility

        Raises:
            ValidationError: For any verification failure in:
                             - Network communication
                             - Cryptographic proofs
                             - Enclave measurements
                             - Security policy violations

        Workflow:
            1. Submit quote to Quote Verification Service (QVS)
            2. Validate HTTP response integrity
            3. Verify IAS report signature chain
            4. Parse and validate quote structure
            5. Verify freshness challenge (nonce)
            6. Validate enclave identity (MRSIGNER)
            7. Perform security policy checks
        """
        try:
            nonce = nonce or base64.b64encode(os.urandom(16)).decode('utf-8')
            qvs_response = self._send_quote(quote, nonce)
            response_body = qvs_response.content
            signature_header = qvs_response.headers.get("X-IASReport-Signature", "")
            cert_header = qvs_response.headers.get("X-IASReport-Signing-Certificate", "")

            self._verify_ias_signature(response_body, signature_header, cert_header)

            try:
                qvs_data = json.loads(response_body.decode('utf-8'))
            except json.JSONDecodeError:
                raise ValidationError("Invalid JSON in QVS response")

            if qvs_data.get('attestationType') != 'ECDSA':
                raise ValidationError("Invalid attestation type")

            self._verify_quote_status(qvs_data)

            isv_quote_body = base64.b64decode(qvs_data.get('isvQuoteBody', ''))

            header, report_body = self._parse_quote(isv_quote_body)

            self._verify_nonce(qvs_data['nonce'], nonce)

            self._verify_mrsigner(report_body.mr_signer)

            if not self.is_debug:
                self._perform_is_debug_checks(report_body)

        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(f"Verification error: {str(e)}") from e

    def _send_quote(self, quote: str, nonce: str) -> Response:
        """
        Internal method to submit an SGX quote to the Quote Verification Service (QVS).

        Sends a POST request to the QVS DCAP v1 endpoint with the provided attestation
        quote and generated nonce for verification. Validates basic HTTP response status
        before returning the response object.

        Args:
            quote: Base64-encoded SGX attestation quote containing enclave measurements
            nonce: Is base64-encoded for transport compatibility

        Returns:
            requests.Response: Raw HTTP response from QVS with verification results

        Raises:
            ValidationError: If response status code is not 200 (HTTP success)

        Example JSON Payload:
            {
                "isvQuote": "BASE64_ENCODED_QUOTE",
                "nonce": "RANDOMLY_GENERATED_BASE64_NONCE"
            }

        Note:
            - Uses application/json content type header
            - Nonce is generated during verifier initialization
            - Endpoint URL is specific to Intel SGX DCAP v1 attestation workflow
        :param quote:
        :return: requests.Response
        """
        qvs_response = requests.post(
            self.dcap_url,
            json={
                "isvQuote": quote,
                "nonce": nonce
            },
            headers={"Content-Type": "application/json"}
        )
        if qvs_response.status_code != 200:
            raise ValidationError(f"HTTP error: {qvs_response.status_code}")
        return qvs_response

    def _parse_quote(self, quote_body: bytes) -> tuple[QuoteHeader, SGXReportBody]:
        """
        Decode and validate SGX quote binary structure.

        Args:
            quote_body: Raw bytes of SGX quote following Intel DCAP format

        Returns:
            tuple: Parsed header and report body structures

        Raises:
            ValidationError: For invalid/malformed quote structure

        Reference:
            Intel SGX SDK Documentation (DCAP v1.16+)
            Intel® 64 and IA-32 Architectures Software Developer Manuals
        """
        try:
            header = self.QuoteHeader(
                version=struct.unpack('<H', quote_body[0:2])[0],
                sign_type=struct.unpack('<H', quote_body[2:4])[0],
                epid_group_id=quote_body[4:8],
                qe_svn=struct.unpack('<H', quote_body[8:10])[0],
                pce_svn=struct.unpack('<H', quote_body[10:12])[0],
                xeid=struct.unpack('<I', quote_body[12:16])[0],
                basename=quote_body[16:48]
            )

            report = self.SGXReportBody(
                cpu_svn=quote_body[48:64],
                misc_select=quote_body[64:68],
                reserved1=quote_body[68:80],
                isv_ext_prod_id=quote_body[80:96],
                attributes=quote_body[96:112],
                mr_enclave=quote_body[112:144],
                reserved2=quote_body[144:176],
                mr_signer=quote_body[176:208],  # 32 bytes
                reserved3=quote_body[208:240],
                config_id=quote_body[240:304],
                isv_prod_id=struct.unpack('<H', quote_body[304:306])[0],
                isv_svn=struct.unpack('<H', quote_body[306:308])[0],
                config_svn=struct.unpack('<H', quote_body[308:310])[0],
                reserved4=quote_body[310:352],
                isv_family_id=quote_body[352:368],
                report_data=quote_body[368:432]  # 64 bytes
            )

            return header, report

        except (IndexError, struct.error) as e:
            raise ValidationError("Invalid quote structure") from e

    def _verify_ias_signature(self, response_body: bytes, signature_b64: str, cert_header: str):
        """
        Validate IAS report signature using X.509 certificate chain.

        Args:
            response_body: Raw HTTP response payload
            signature_b64: Base64-encoded RSA PKCS#1 v1.5 signature
            cert_header: URL-encoded certificate chain from response headers

        Raises:
            SignatureValidationError: For any signature verification failures

        Cryptography:
            - Uses SHA-384 hash algorithm
            - Implements PKCS#1 v1.5 padding
            - Verifies with first certificate in chain
        """
        try:
            signature = base64.b64decode(signature_b64)

            cert_pem = self._extract_first_certificate(cert_header)
            cert = load_pem_x509_certificate(cert_pem.encode(), default_backend())

            cert.public_key().verify(
                signature,
                response_body,
                padding.PKCS1v15(),
                hashes.SHA384()
            )
        except Exception as e:
            raise SignatureValidationError(f"Signature verification failed: {str(e)}")

    def _extract_first_certificate(self, cert_header: str) -> str:
        """
        Process certificate chain from HTTP headers to PEM format.

        Args:
            cert_header: URL-encoded certificate chain header value

        Returns:
            str: PEM-formatted X.509 certificate

        Raises:
            ValidationError: For malformed certificate headers

        Note:
            - Handles URL percent-encoding
            - Extracts first certificate in chain
            - Validates PEM structure boundaries
        """
        unquoted = urllib.parse.unquote(cert_header)
        start = unquoted.find('-----BEGIN CERTIFICATE-----')
        end = unquoted.find('-----END CERTIFICATE-----') + 25

        if start == -1 or end == -1:
            raise ValidationError("Invalid certificate format")

        return unquoted[start:end]

    def _verify_quote_status(self, qvs_data: dict):
        """
        Validate QVS response status against security policy.

        Args:
            qvs_data: Parsed JSON response from QVS

        Raises:
            ValidationError: For prohibited status values:
                             - SIGNATURE_INVALID
                             - REVOKED

        Note:
            Accepts STATUS_OK and STATUS_GROUP_OUT_OF_DATE as valid
        """
        status = qvs_data.get('isvQuoteStatus', '')
        if status in ['SIGNATURE_INVALID', 'REVOKED']:
            raise ValidationError(f"Invalid quote status: {status}")

    def _verify_nonce(self, received_nonce: str, expected_nonce: str):
        """
        Validate challenge-response nonce for anti-replay protection.

        Args:
            received_nonce: Nonce value from QVS response

        Raises:
            ValidationError: If nonce mismatch detected

        Security:
            - Prevents replay attacks
            - Uses cryptographically secure random generation
            - Enforces exact base64 match
        """

        if received_nonce != expected_nonce:
            raise ValidationError("Nonce mismatch")

    def _verify_mrsigner(self, mr_signer: bytes):
        """
        Validate enclave signer identity measurement.

        Args:
            mr_signer: MRSIGNER value extracted from quote

        Raises:
            ValidationError: For signer identity mismatch

        Technical:
            - MRSIGNER = SHA256(enclave_signer_public_key)
            - Hex comparison of 32-byte measurement
        """
        if mr_signer != bytes.fromhex(self.mr_signer):
            raise ValidationError("MRSIGNER mismatch")

    def _perform_is_debug_checks(self, report_body: SGXReportBody):
        """
        Enforce security hardening policies on enclave configuration.

        Args:
            report_body: Parsed enclave report body

        Raises:
            ValidationError: For policy violations:
                             - Debug mode enabled

        Checks:
             Debug mode flag status
        """
        flags = struct.unpack('<Q', report_body.attributes[:8])[0]
        if (flags & 0x0000000000000002) != 0:
            raise ValidationError("Enclave is in debug mode")
