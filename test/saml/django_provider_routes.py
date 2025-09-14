provider_conf = {
    "title": "SAML Provider",
    "name": "saml",
    "type": "saml",
    "config": {
        "sp": {
            "entity_id": "https://localhost:8000",
            "signing_cert": "test/saml/conf/certs/localhost.pem",
            "private_key": "test/saml/conf/certs/localhost-key.pem",
        },
        "idp_meta_url": "https://mocksaml.com/api/saml/metadata",
    }
}

from drf_sso.providers.registry import from_config

SAMLProvider = from_config("saml", provider_conf)

print(SAMLProvider.get_routes())
print(SAMLProvider.get_login_url())
print(SAMLProvider.provider.get_metadata_xml())