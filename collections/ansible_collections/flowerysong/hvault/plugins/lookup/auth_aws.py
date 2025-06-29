# (c) 2021 Paul Arthur MacIain
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
name: auth_aws
author: Paul Arthur (@flowerysong)
short_description: AWS authentication for HashiCorp Vault
description:
  - AWS authentication for HashiCorp Vault.
options:
  _terms:
    description: role to log in using.
    required: true
  request_headers:
    description:
      - Headers for use in the STS call.
    type: dict
    default: {}
  mount_point:
    description:
      - Path under auth/ where the AWS backend is mounted.
    type: str
    default: aws
  raw:
    description: Controls whether the entire API response is returned, or just the token.
    type: bool
    default: false
extends_documentation_fragment:
  - flowerysong.hvault.base
  - flowerysong.hvault.base.PLUGINS
"""

EXAMPLES = """
- name: Look up a standard secret using AWS authentication
  debug:
    msg: The result is {{ lookup('flowerysong.hvault.read', 'secret/ping', **hashi_conf) }}
  vars:
    hashi_conf:
      token: "{{ lookup('flowerysong.hvault.auth_aws', 'myrole') }}"
"""

RETURN = """
  _raw:
    description:
      - Tokens.
    type: list
    elements: str
"""

import json

from base64 import b64encode

BOTOCORE_IMPORT_ERROR = None
try:
    import botocore.session
except ImportError as e:
    BOTOCORE_IMPORT_ERROR = e

from ansible.errors import AnsibleError
from ansible.module_utils.six.moves.urllib.error import URLError
from ..plugin_utils.lookup import HVaultLookupBase


class LookupModule(HVaultLookupBase):
    def run(self, terms, variables=None, **kwargs):
        if BOTOCORE_IMPORT_ERROR:
            raise AnsibleError('This plugin requires botocore') from BOTOCORE_IMPORT_ERROR

        self.init_options(variables=variables, direct=kwargs)
        self.config_client()

        boto_client = botocore.session.get_session().create_client('sts')
        boto_endpoint = boto_client._endpoint
        boto_operation_model = boto_client._service_model.operation_model('GetCallerIdentity')
        try:
            boto_request_dict = boto_client._convert_to_request_dict({}, boto_operation_model, endpoint_url=boto_endpoint.host)
        except TypeError:
            # Older versions of botocore don't require the endpoint_url
            boto_request_dict = boto_client._convert_to_request_dict({}, boto_operation_model)
        for h in self.get_option('request_headers').items():
            boto_request_dict['headers'][h[0]] = h[1]

        url = '/'.join(['auth', self.get_option('mount_point').strip('/'), 'login'])

        ret = []
        for term in terms:
            sts_request = boto_endpoint.create_request(boto_request_dict, boto_operation_model)

            config = {
                'role': term,
                'iam_http_request_method': sts_request.method,
                'iam_request_url': b64encode(sts_request.url.encode('utf-8')),
                'iam_request_body': b64encode(sts_request.body.encode('utf-8')),
                'iam_request_headers': json.dumps({x[0]: (x[1] if isinstance(x[1], str) else x[1].decode('utf-8')) for x in sts_request.headers.items()}),
            }

            try:
                secret = self.client.post(url, config)
            except URLError as e:
                raise AnsibleError(f'Unable to authenticate: {e}')

            if secret:
                if self.get_option('raw'):
                    ret.append(secret)
                else:
                    ret.append(secret['auth']['client_token'])
            else:
                raise AnsibleError('Unable to authenticate')

        return ret
