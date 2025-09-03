provider_conf = {
    "title": "SAML Provider",
    "name": "saml",
    "type": "saml",
    "config": {
        "sp": {
            "entity_id": "https://daccib-api.genavir.dev",
            "signing_cert": "test/saml/conf/certs/cert.pem",
            "private_key": "test/saml/conf/certs/key.pem",
            "public_key": "test/saml/conf/certs/key.pub"
        },
        "idp_meta_url": "https://idp-notilus.ifremer.fr/idp/metadata",
    }
}

from drf_sso.providers.registry import from_config

SAMLProvider = from_config("saml", provider_conf)

print(SAMLProvider.get_routes())
print(SAMLProvider.get_login_url())
print(SAMLProvider.provider.get_metadata_xml())