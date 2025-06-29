#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: aws_secret_role_iam
author: "Paul Arthur (@flowerysong)"
short_description: Manage AWS iam_user secret roles in HashiCorp Vault
description:
  - Manage AWS iam_user secret roles in HashiCorp Vault.
  - The underlying API is the same one used by C(aws_secret_role_sts), so either
    module can delete roles created by the other.
seealso:
  - module: flowerysong.hvault.aws_secret_role_sts
version_added: 0.2.0
extends_documentation_fragment:
  - flowerysong.hvault.base
  - flowerysong.hvault.auth_token
  - flowerysong.hvault.role
options:
  mount_point:
    default: aws
  policy_arns:
    type: list
    elements: str
    description:
      - AWS managed policy ARNs to attach to created users.
  policy_document:
    type: str
    description:
      - Policy document to attach to created users.
  iam_groups:
    type: list
    elements: str
    description:
      - IAM groups to which created users will be added.
  iam_tags:
    type: list
    elements: str
    description:
      - Tags to add to created users..
      - Each tag should be represented as a C(key=value) string.
  user_path:
    type: str
    default: /
    description:
      - Path for the username.
  permissions_boundary_arn:
    type: str
    description:
      - AWS permissions boundary to attach to created users.
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ..module_utils.module import HVaultModule


def main():
    argspec = dict(
        mount_point=dict(
            default='aws',
        ),
    )

    optspec = dict(
        policy_arns=dict(
            type='list',
            elements='str',
        ),
        policy_document=dict(),
        iam_groups=dict(
            type='list',
            elements='str',
        ),
        iam_tags=dict(
            type='list',
            elements='str',
        ),
        user_path=dict(default='/'),
        permissions_boundary_arn=dict(),
    )

    module = HVaultModule(
        argspec=argspec,
        optspec=optspec,
        required_if=[
            ['state', 'present', ['policy_arns', 'policy_document'], True],
        ],
    )

    module.run(
        path_fmt='{0}/roles/{1}',
        config=dict(
            credential_type='iam_user',
            role_arns=None,
        ),
    )


if __name__ == '__main__':
    main()
