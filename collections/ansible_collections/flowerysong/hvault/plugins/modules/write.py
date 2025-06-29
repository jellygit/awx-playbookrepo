#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: write
author: "Paul Arthur (@flowerysong)"
short_description: Write something to HashiCorp Vault
description:
  - Write data to HashiCorp Vault. This can be used to add secrets, set
    configuration details, etc.
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.hvault.base
  - flowerysong.hvault.auth_token
options:
  path:
    description:
      - Path to write to on the Vault server.
    type: str
    required: true
  data:
    description:
      - Data to write
    type: raw
    required: true
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


def main():
    argspec = hvault_argument_spec()
    argspec.update(
        dict(
            path=dict(
                required=True,
            ),
            data=dict(
                type='raw',
                required=True,
            ),
        )
    )

    module = AnsibleModule(
        supports_check_mode=False,
        argument_spec=argspec,
    )

    client = HVaultClient(module.params, module)

    result = client.post(module.params['path'], module.params['data'])

    module.exit_json(changed=True, result=result)


if __name__ == '__main__':
    main()
