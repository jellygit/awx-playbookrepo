#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: auth_approle
author: "Paul Arthur (@flowerysong)"
short_description: Authenticate to HashiCorp Vault using AppRole
description:
  - Authenticate to HashiCorp Vault using AppRole.
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.hvault.base
options:
  role_id:
    type: str
    required: true
    description:
      - Role ID to use for authentication.
  secret_id:
    type: str
    required: false
    description:
      - SecretID to use for authentication.
  mount_point:
    type: str
    default: approle
    description:
      - Path under auth/ where the backend is mounted.
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.base import (
    HVaultClient,
    hvault_argument_spec,
)
from ..module_utils.module import optspec_to_config


def main():
    argspec = hvault_argument_spec()
    argspec.pop('token')
    argspec.update(
        dict(
            mount_point=dict(
                default='approle',
            ),
        )
    )

    optspec = dict(
        secret_id=dict(
            no_log=True,
        ),
        role_id=dict(
            required=True,
            no_log=True,
        ),
    )
    argspec.update(optspec)

    module = AnsibleModule(
        supports_check_mode=False,
        argument_spec=argspec,
    )

    module.params['token'] = None
    client = HVaultClient(module.params, module)

    base_path = '/'.join([
        'auth',
        module.params['mount_point'].strip('/'),
        'login',
    ])

    config = optspec_to_config(optspec, module.params)

    result = client.post(base_path, config)['auth']

    module.exit_json(changed=True, auth=result)


if __name__ == '__main__':
    main()
