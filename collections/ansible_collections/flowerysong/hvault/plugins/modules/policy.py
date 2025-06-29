#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: policy
author: "Paul Arthur (@flowerysong)"
short_description: Manage HashiCorp Vault policies
description:
  - Manage HashiCorp Vault policies.
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.hvault.base
  - flowerysong.hvault.auth_token
options:
  name:
    description:
      - Policy name.
    type: str
    required: true
  state:
    description:
      - Policy state.
    type: str
    choices:
      - present
      - absent
    default: present
  policy:
    description:
      - Policy document, as either a valid HCL string or a dictionary value.
      - This module does not attempt to parse HCL and compare the actual policy
        dictionary, so structurally identical policies can result in a
        C(changed) result.
      - Required when I(state=present)
    type: raw
'''

EXAMPLES = '''
- name: Create a policy
  flowerysong.hvault.policy:
    name: blackops
    policy:
      path:
        secret/*:
          capabilities: [create, read, update, delete, list]
        secret:
          capabilities:
            - list

# You can also leave out the (currently static) 'path' and 'capabilities'
# levels, and the module will add them for you automatically.
- name: Create a policy
  flowerysong.hvault.policy:
    name: blackops
    policy:
      secret/*: [create, read, update, delete, list]
      secret: [list]

- name: Create an HCL policy
  flowerysong.hvault.policy:
    name: blackops
    policy: |
      path "secret/*" {
        capabilities = ["create", "read", "update", "delete", "list"]
      }
      path "secret" {
        capabilities = ["list"]
      }

- name: Create an HCL policy from a file
  flowerysong.hvault.policy:
    name: blackops
    policy: "{{ lookup('file', 'blackops.hcl') }}"
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import jsonify
from ansible.module_utils.six import string_types
from ansible.module_utils.six.moves.urllib.error import URLError

from ..module_utils.base import (
    HVaultClient,
    hvault_argument_spec,
)


def main():
    argspec = hvault_argument_spec()
    argspec.update(
        dict(
            name=dict(required=True),
            state=dict(choices=['present', 'absent'], default='present'),
            policy=dict(type='raw'),
        )
    )

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
        required_if=[
            ['state', 'present', ['policy']],
        ],
    )

    client = HVaultClient(module.params, module)

    pol_path = 'sys/policies/acl/{0}'.format(module.params['name'])
    try:
        result = client.get(pol_path, fatal=False)
        result = result['data']
    except URLError:
        result = None

    if module.params['state'] == 'absent':
        if not result:
            module.exit_json(changed=False)
        if not module.check_mode:
            client.delete(pol_path)
        module.exit_json(changed=True)

    policy = module.params['policy']

    if not isinstance(policy, string_types):
        if not isinstance(policy, dict):
            module.fail_json(msg='policy must be either a dict or a string, got {0}'.format(type(policy)))

        # allow people to write policies with less typing
        if 'path' not in policy:
            policy = {'path': policy}
        for key in policy['path']:
            if isinstance(policy['path'][key], list):
                policy['path'][key] = {'capabilities': policy['path'][key]}

        policy = jsonify(policy, indent=2, sort_keys=True)

    changed = False
    if not result or result['policy'] != policy:
        changed = True
        if not module.check_mode:
            client.put(pol_path, data={'policy': policy})
            result = client.get(pol_path)['data']

    module.exit_json(changed=changed, policy=result)


if __name__ == '__main__':
    main()
