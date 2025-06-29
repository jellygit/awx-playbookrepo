#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: policy_info
author: "Paul Arthur (@flowerysong)"
short_description: List ACLs within HashiCorp Vault
description:
  - List ACLs within HashiCorp Vault.
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.hvault.base
  - flowerysong.hvault.auth_token
'''

EXAMPLES = '''
- flowerysong.hvault.policy_info:
  register: result
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

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    client = HVaultClient(module.params, module)
    result = client.list('sys/policies/acl')
    module.exit_json(changed=False, policies=result['data']['keys'])


if __name__ == '__main__':
    main()
