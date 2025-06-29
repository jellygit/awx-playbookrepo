#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: approle_secret_id
author: "Paul Arthur (@flowerysong)"
short_description: Manage AppRole SecretIDs in HashiCorp Vault
description:
  - Manage AppRole SecretIDs in HashiCorp Vault.
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.hvault.base
  - flowerysong.hvault.auth_token
options:
  state:
    type: str
    choices:
      - present
      - absent
    default: present
    description:
      - Desired state of the SecretID.
  secret_id:
    type: str
    required: false
    description:
      - SecretID to manage.
      - Can be used with I(state=present) to manage "custom" SecretIDs.
      - Required if I(state=absent).
  role_name:
    type: str
    required: true
    description:
     - Name of the AppRole.
  mount_point:
    type: str
    default: approle
    description:
      - Path under auth/ where the backend is mounted.
  metadata:
    type: json
    required: false
    description:
      - Mapping of key/value pairs to associate with this SecretID.
      - The metadata will be logged in audit logs as plain text.
  cidr_list:
    type: list
    elements: str
    default: []
    aliases:
      - secret_id_bound_cidrs
    description:
      - CIDR blocks that are allowed to authenticate using this SecretID.
      - If C(secret_id_bound_cidrs) is set on the role, this must be a subset of those blocks.
  token_bound_cidrs:
    type: list
    elements: str
    default: []
    description:
      - CIDR blocks that are allowed to use tokens generated using this SecretID.
      - If C(token_bound_cidrs) is set on the role, this must be a subset of those blocks.
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
from ..module_utils.module import optspec_to_config


def main():
    argspec = hvault_argument_spec()
    argspec.update(
        dict(
            state=dict(
                choices=['present', 'absent'],
                default='present',
            ),
            mount_point=dict(
                default='approle',
            ),
            secret_id=dict(
                no_log=False,
            ),
            role_name=dict(
                required=True,
            ),
        )
    )

    optspec = dict(
        metadata=dict(
            type='json',
            required=False,
        ),
        cidr_list=dict(
            type='list',
            elements='str',
            default=[],
            no_log=False,
            aliases=['secret_id_bound_cidrs'],
        ),
        token_bound_cidrs=dict(
            type='list',
            elements='str',
            default=[],
            no_log=False,
        ),
    )
    argspec.update(optspec)

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
        required_if=[
            ['state', 'absent', ['secret_id']],
        ],
    )

    client = HVaultClient(module.params, module)

    base_path = '/'.join([
        'auth',
        module.params['mount_point'].strip('/'),
        'role',
        module.params['role_name'],
    ])

    if module.params['state'] == 'absent':
        changed = False
        secret_id = False
        accessor = False
        result = client.post(base_path + '/secret-id/lookup', dict(secret_id=module.params['secret_id']), fatal=False)
        if result:
            secret_id = True
        else:
            try:
                client.post(base_path + '/secret-id-accessor/lookup', dict(secret_id_accessor=module.params['secret_id']), fatal=False)
                accessor = True
            except URLError:
                pass

        if secret_id:
            changed = True
            if not module.check_mode:
                client.post(base_path + '/secret-id/destroy', dict(secret_id=module.params['secret_id']))
        elif accessor:
            changed = True
            if not module.check_mode:
                client.post(base_path + '/secret-id-accessor/destroy', dict(secret_id_accessor=module.params['secret_id']))

        module.exit_json(changed=changed)

    config = optspec_to_config(optspec, module.params)

    # If it's not a custom SecretID, we always create one
    if not module.params['secret_id']:
        if module.check_mode:
            module.exit_json(changed=True)

        result = client.post(base_path + '/secret-id', config)
        module.exit_json(changed=True, secret_id=result['data'])

    result = client.post(base_path + '/secret-id/lookup', dict(secret_id=module.params['secret_id']), fatal=False)
    if result:
        result['data']['secret_id'] = module.params['secret_id']
        module.exit_json(changed=False, secret_id=result['data'])

    if module.check_mode:
        result = {}
    else:
        config['secret_id'] = module.params['secret_id']
        result = client.post(base_path + '/custom-secret-id', config)['data']
    module.exit_json(changed=True, secret_id=result)


if __name__ == '__main__':
    main()
