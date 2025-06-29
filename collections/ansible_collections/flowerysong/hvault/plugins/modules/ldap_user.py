#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: ldap_user
author: "Paul Arthur (@flowerysong)"
short_description: Manage LDAP user policies in HashiCorp Vault
description:
  - Manage LDAP user policies in HashiCorp Vault.
version_added: 0.2.0
extends_documentation_fragment:
  - flowerysong.hvault.base
  - flowerysong.hvault.auth_token
options:
  mount_point:
    description:
      - Path where the backend is mounted.
    type: str
    default: ldap
  name:
    description:
      - Name of the user to manage.
    type: str
    required: true
  state:
    description:
      - Desired state of the user.
    type: str
    choices:
      - present
      - absent
    default: present
  policies:
    type: list
    elements: str
    default: []
    description:
      - Policies to associate with the user.
  groups:
    type: list
    elements: str
    default: []
    description:
      - Groups to associate with the user.
'''

EXAMPLES = '''
- name: Set up a user
  flowerysong.hvault.ldap_user:
    name: flowerysong
    policies:
      - default
      - me
    groups: people
'''

RETURN = '''
'''

from ..module_utils.module import HVaultModule


def main():
    argspec = dict(
        mount_point=dict(
            default='ldap',
        ),
        name=dict(required=True),
        state=dict(
            choices=['present', 'absent'],
            default='present',
        ),
    )

    optspec = dict(
        policies=dict(
            type='list',
            elements='str',
            default=[],
        ),
        groups=dict(
            type='list',
            elements='str',
            default=[],
            join=True,
        ),
    )

    module = HVaultModule(
        argspec=argspec,
        optspec=optspec,
    )

    module.run(
        path_fmt='auth/{0}/users/{1}',
        config=dict(),
        result_key='user',
    )


if __name__ == '__main__':
    main()
