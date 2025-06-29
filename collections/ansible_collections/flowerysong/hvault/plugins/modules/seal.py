#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: seal
author: "Paul Arthur (@flowerysong)"
short_description: Manage the seal status of HashiCorp Vault
description:
  - Manage the seal status of HashiCorp Vault.
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.hvault.base
  - flowerysong.hvault.auth_token
options:
  state:
    description:
      - Desired seal state.
      - If the Vault is sealed, I(state=sealed) will reset any unsealing progress that has been made.
    type: str
    choices:
      - sealed
      - unsealed
    default: sealed
  migrate:
    description:
      - Migrate between unsealing methods during this unseal.
    type: bool
    default: false
  key:
    description:
      - Primary key or key share(s) to use for unsealing.
      - Required if I(state=unsealed)
    type: list
    elements: str
    aliases:
      - keys
'''

EXAMPLES = '''
- name: Unseal the Vault
  flowerysong.hvault.seal:
    state: unsealed
    key: 0b2bde0b6643ac2ff8d0c2eec40b36d3fa21946c059f0c133e2b0bf60f8685a3ee
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.base import (
    HVaultClient,
    hvault_argument_spec,
)


def unseal(module, client, keys, migrate):
    for key in keys:
        params = {
            'key': key,
            'migrate': migrate,
        }

        result = client.put('sys/unseal', params)
        if not result['sealed']:
            return result

    return result


def main():
    argspec = hvault_argument_spec()
    argspec.update(
        dict(
            state=dict(choices=['sealed', 'unsealed'], default='sealed'),
            migrate=dict(type='bool', default=False),
            key=dict(type='list', elements='str', aliases=['keys'], no_log=True),
        )
    )

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
        required_if=[
            ['state', 'unsealed', ['key']],
        ],
    )

    client = HVaultClient(module.params, module)

    result = client.get('sys/seal-status')

    changed = False
    if module.params['state'] == 'sealed':
        if result['sealed']:
            if result['progress'] > 0:
                changed = True
                if not module.check_mode:
                    result = client.put('sys/unseal', {'reset': True})
        else:
            changed = True
            if not module.check_mode:
                result = client.put('sys/seal', None)

    elif result['sealed']:
        changed = True
        if not module.check_mode:
            result = unseal(module, client, module.params['key'], module.params['migrate'])

    module.exit_json(changed=changed, status=result)


if __name__ == '__main__':
    main()
