# (c) 2021 Paul Arthur MacIain
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.errors import AnsibleError
from ansible.module_utils.six.moves.urllib.error import URLError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

from ..module_utils.base import (
    HVaultClient,
    hvault_argument_spec,
)

display = Display()


class HVaultLookupBase(LookupBase):
    def config_client(self):
        client_opts = {}
        for opt in hvault_argument_spec():
            try:
                client_opts[opt] = self._templar.template(self.get_option(opt), fail_on_undefined=True)
            except KeyError:
                client_opts[opt] = None

        self.client = HVaultClient(client_opts)

    def init_options(self, variables, direct):
        if variables is not None:
            self._templar.available_variables = variables
        self.set_options(var_options=variables, direct=direct)

    def run(self, terms, variables=None, **kwargs):
        ret = []

        for term in terms:
            display.debug(f'flowerysong.hvault lookup term: {term}')

            try:
                secret = self.client.get(term)
            except URLError as e:
                raise AnsibleError(f'Unable to fetch secret {term}: {e}"')

            display.vvvv(f'flowerysong.hvault lookup found {secret}')

            if secret:
                if 'data' in secret and (not self.has_option('raw') or not self.get_option('raw')):
                    secret = secret['data']
                ret.append(secret)
            else:
                raise AnsibleError(f'Unable to find secret matching "{term}"')

        return ret
