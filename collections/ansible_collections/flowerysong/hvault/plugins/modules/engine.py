#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: engine
author: "Paul Arthur (@flowerysong)"
short_description: Manage secrets engines within HashiCorp Vault
description:
  - Manage mounted secrets engines within HashiCorp Vault.
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.hvault.base
  - flowerysong.hvault.auth_token
  - flowerysong.hvault.mount
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ..module_utils.mount import HVaultMountModule


def main():
    module = HVaultMountModule(
        'sys/mounts',
    )

    module.run()


if __name__ == '__main__':
    main()
