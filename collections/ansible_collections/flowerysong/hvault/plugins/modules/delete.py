#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: delete
author: "Paul Arthur (@flowerysong)"
short_description: Delete something from HashiCorp Vault
description:
  - Delete something from HashiCorp Vault.
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.hvault.base
  - flowerysong.hvault.auth_token
options:
  path:
    description:
      - Path to delete from the Vault server.
    type: str
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
        )
    )

    module = AnsibleModule(
        supports_check_mode=False,
        argument_spec=argspec,
    )

    client = HVaultClient(module.params, module)

    client.delete(module.params['path'])

    module.exit_json(changed=True)


if __name__ == '__main__':
    main()
