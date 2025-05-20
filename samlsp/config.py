import xml.etree.ElementTree as ET
from pathlib import Path
from enum import Enum

NAMESPACES = {
    "saml": "urn:oasis:names:tc:SAML:2.0:assertion",
    "samlp": "urn:oasis:names:tc:SAML:2.0:protocol",
    "md": "urn:oasis:names:tc:SAML:2.0:metadata",
    "ds": "http://www.w3.org/2000/09/xmldsig#",
}

class Binding(Enum):
    HTTP_REDIRECT = "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
    HTTP_POST = "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
    HTTP_POST_SIMPLE_SIGN = "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST-SimpleSign"
    SOAP = "urn:oasis:names:tc:SAML:2.0:bindings:SOAP"

class SPConfig:
    def __init__(self, data: dict):
        self.entity_id = data["entity_id"]
        self.acs_url = data["acs_url"]
        self.sls_url = data.get("sls_url")
        self.signing_cert_path = Path(data["signing_cert"])
        self.private_key_path = Path(data["private_key"])
        self.want_assertions_signed = data.get("want_assertions_signed", True)
        self.authn_requests_signed = data.get("authn_requests_signed", True)

        self.signing_cert = self._read_file(self.signing_cert_path)
        self.private_key = self._read_file(self.private_key_path)

    def _read_file(self, path: Path) -> str:
        with open(path, "r") as f:
            return f.read()


class IdPConfig:
    def __init__(self, metadata_xml: str):
        self.entity_id = None
        self.sso_services = {}  # Binding -> URL
        self.sls_services = {}  # Binding -> URL
        self.signing_cert = None
        self.encryption_cert = None
        self._parse(metadata_xml)

    def _parse(self, xml_str: str):
        root = ET.fromstring(xml_str)
        self.entity_id = root.attrib.get("entityID")

        for sso in root.findall(".//md:IDPSSODescriptor/md:SingleSignOnService", NAMESPACES):
            binding = sso.attrib.get("Binding")
            location = sso.attrib.get("Location")
            if binding and location:
                self.sso_services[binding] = location

        for sls in root.findall(".//md:IDPSSODescriptor/md:SingleLogoutService", NAMESPACES):
            binding = sls.attrib.get("Binding")
            location = sls.attrib.get("Location")
            if binding and location:
                self.sls_services[binding] = location

        certs = root.findall(".//md:IDPSSODescriptor/md:KeyDescriptor", NAMESPACES)
        for cert in certs:
            use = cert.attrib.get("use", "signing")
            x509 = cert.find(".//ds:X509Certificate", NAMESPACES)
            if x509 is not None:
                if use == "signing":
                    self.signing_cert = x509.text.strip()
                elif use == "encryption":
                    self.encryption_cert = x509.text.strip()