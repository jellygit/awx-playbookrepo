#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: auth_method
author: "Paul Arthur (@flowerysong)"
short_description: Manage mounted authentication methods within HashiCorp Vault
description:
  - Manage mounted authentication methods within HashiCorp Vault.
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.hvault.base
  - flowerysong.hvault.auth_token
  - flowerysong.hvault.mount
options:
  token_type:
    description:
      - Type of token that should be returned.
      - C(default-service) and C(default-batch) set a default that can be
        overridden by the auth method, while C(service) and C(batch) take
        precedence over the auth method's preference.
    type: str
    choices:
        - default-service
        - default-batch
        - service
        - batch
    default: default-service
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ..module_utils.mount import HVaultMountModule


def main():
    module = HVaultMountModule(
        'sys/auth',
        extra_config=dict(
            token_type=dict(
                choices=[
                    'default-service',
                    'default-batch',
                    'service',
                    'batch',
                ],
                default='default-service',
            ),
        ),
    )

    module.run()


if __name__ == '__main__':
    main()
