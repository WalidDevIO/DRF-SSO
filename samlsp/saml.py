from .config import SPConfig, IdPConfig, Binding
from .request import create_authn_request, AuthnRequest
from .response import SAMLResponse

import requests

class SAMLSP:
    def __init__(self, sp_config: SPConfig, idp_config: IdPConfig | str):
        self.sp = sp_config
        if isinstance(idp_config, str):
            response = requests.get(idp_config)
            response.raise_for_status()
            self.idp = IdPConfig(response.text)
        else:
            self.idp = idp_config
            
    def get_login_request(self, binding: Binding = Binding.HTTP_REDIRECT) -> tuple[str, str, AuthnRequest]:
        return create_authn_request(self.sp, self.idp, binding)

    def parse_response(self, b64_response: str) -> SAMLResponse:
        return SAMLResponse(b64_response, self.sp, self.idp)

    def get_metadata_xml(self, binding: Binding = Binding.HTTP_POST) -> str:
        from .metadata import generate_metadata
        return generate_metadata(self.sp, binding)

    def write_metadata(self, path, binding: Binding = Binding.HTTP_POST):
        from .metadata import write_metadata_to_file
        write_metadata_to_file(self.sp, path, binding)