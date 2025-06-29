#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: kv
author: "Paul Arthur (@flowerysong)"
short_description: Manage KV secrets in HashiCorp Vault
description:
  - Manage KV secrets in HashiCorp Vault.
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.hvault.base
  - flowerysong.hvault.auth_token
options:
  mount_point:
    description:
      - Path where the KV backend is mounted.
    type: str
    default: secret
  key:
    description:
      - Name of the secret to manage.
    type: str
    required: true
  state:
    description:
      - Desired state of the secret.
    type: str
    choices:
      - present
      - absent
    default: present
  value:
    description:
      - Data to write.
      - Required if I(state=present).
    type: dict
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError

from ..module_utils.base import (
    HVaultClient,
    hvault_argument_spec,
)


def main():
    argspec = hvault_argument_spec()
    argspec.update(
        dict(
            mount_point=dict(
                default='secret',
            ),
            key=dict(
                required=True,
                no_log=False,
            ),
            state=dict(
                choices=['present', 'absent'],
                default='present',
            ),
            value=dict(
                type='dict',
            ),
        )
    )

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
        required_if=[
            ['state', 'present', ['value']],
        ],
    )

    client = HVaultClient(module.params, module)

    path = '{0}/{1}'.format(module.params['mount_point'].rstrip('/'), module.params['key'])

    changed = False
    try:
        result = client.get(path, fatal=False)
    except URLError:
        result = {}

    if module.params['state'] == 'present' and result.get('data') != module.params['value']:
        changed = True
        if not module.check_mode:
            client.post(path, module.params['value'])
    elif module.params['state'] == 'absent' and result:
        changed = True
        if not module.check_mode:
            client.delete(path)

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
