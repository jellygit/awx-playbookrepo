# (c) 2021 Paul Arthur MacIain
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
name: list
author: Paul Arthur (@flowerysong)
short_description: Lookup for HashiCorp Vault
description:
  - A simple lookup for HashiCorp Vault.
options:
  _terms:
    description: Paths to look up.
    required: True
  raw:
    description: Controls whether the entire API response is returned, or just the data.
    type: bool
    default: false
extends_documentation_fragment:
  - flowerysong.hvault.base
  - flowerysong.hvault.base.PLUGINS
  - flowerysong.hvault.auth_token
  - flowerysong.hvault.auth_token.PLUGINS
"""

EXAMPLES = """
- name: List secrets
  debug:
    msg: The results are {{ lookup('flowerysong.hvault.list', 'secret/') }}
"""

RETURN = """
  _raw:
    description:
      - Secrets
    type: list
    elements: dict
"""

from ansible.errors import AnsibleError
from ansible.module_utils.six.moves.urllib.error import URLError
from ansible.utils.display import Display

from ..plugin_utils.lookup import HVaultLookupBase

display = Display()


class LookupModule(HVaultLookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.init_options(variables=variables, direct=kwargs)
        self.config_client()

        ret = []

        for term in terms:
            display.debug('flowerysong.hvault lookup term: {0}'.format(term))

            try:
                secret = self.client.list(term)
            except URLError as e:
                raise AnsibleError('Unable to list endpoint') from e

            display.vvvv('flowerysong.hvault lookup found {0}'.format(secret))

            if not secret:
                raise AnsibleError('No data from endpoint "{0}"'.format(term))

            if self.get_option('raw'):
                ret.append(secret)
            else:
                ret.extend(secret['data']['keys'])

        return ret
