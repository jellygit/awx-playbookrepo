# (c) 2021 Paul Arthur MacIain
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
name: auth_approle
author: Paul Arthur (@flowerysong)
short_description: AppRole authentication for HashiCorp Vault
description:
  - AppRole authentication for HashiCorp Vault.
options:
  _terms:
    description: RoleID to log in using.
    required: true
  secret_id:
    description:
      - SecretID for the AppRole.
    type: str
    required: false
  mount_point:
    description:
      - Path under auth/ where the AppRole backend is mounted.
    type: str
    default: approle
  raw:
    description: Controls whether the entire API response is returned, or just the token.
    type: bool
    default: false
extends_documentation_fragment:
  - flowerysong.hvault.base
  - flowerysong.hvault.base.PLUGINS
"""

EXAMPLES = """
- name: Look up a standard secret using AppRole authentication
  debug:
    msg: The result is {{ lookup('flowerysong.hvault.read', 'secret/ping', **hashi_conf) }}
  vars:
    hashi_conf:
      token: "{{ lookup('flowerysong.hvault.auth_approle', '59d6d1ca-47bb-4e7e-a40b-8be3bc5a0ba8', secret_id='84896a0c-1347-aa90-a4f6-aca8b7558780') }}"
"""

RETURN = """
  _raw:
    description:
      - Tokens.
    type: list
    elements: str
"""

from ansible.errors import AnsibleError
from ansible.module_utils.six.moves.urllib.error import URLError
from ..plugin_utils.lookup import HVaultLookupBase


class LookupModule(HVaultLookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.init_options(variables=variables, direct=kwargs)
        self.config_client()

        url = '/'.join(['auth', self.get_option('mount_point').strip('/'), 'login'])

        ret = []
        for term in terms:
            config = {
                'role_id': term,
            }
            secret_id = self.get_option('secret_id')
            if secret_id:
                config['secret_id'] = secret_id

            try:
                secret = self.client.post(url, config)
            except URLError as e:
                raise AnsibleError('Unable to authenticate') from e

            if secret:
                if self.get_option('raw'):
                    ret.append(secret)
                else:
                    ret.append(secret['auth']['client_token'])
            else:
                raise AnsibleError('Unable to authenticate')

        return ret
