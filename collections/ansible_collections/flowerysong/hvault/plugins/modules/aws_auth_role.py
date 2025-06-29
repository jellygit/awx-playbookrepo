#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: aws_auth_role
author: "Paul Arthur (@flowerysong)"
short_description: Manage AWS authentication roles in HashiCorp Vault
description:
  - Manage AWS authentication roles in HashiCorp Vault.
  - The legacy 'ec2' auth type is not supported by this module, only 'iam'.
version_added: 0.2.0
extends_documentation_fragment:
  - flowerysong.hvault.base
  - flowerysong.hvault.auth_token
  - flowerysong.hvault.role
  - flowerysong.hvault.token
options:
  mount_point:
    default: aws
  bound_ami_id:
    type: list
    elements: str
    description:
      - Constrains authenticating instances based on AMI ID.
      - Requires I(inferred_entity_type=ec2_instance).
  bound_account_id:
    type: list
    elements: str
    description:
      - Constrains authenticating instances based on account ID.
      - Requires I(inferred_entity_type=ec2_instance).
  bound_region:
    type: list
    elements: str
    description:
      - Constrains authenticating instances based on launch region.
      - Requires I(inferred_entity_type=ec2_instance).
      - The documentation claims that this is checked by the iam auth type when inferencing is enabled, but inferencing is single-region...
  bound_vpc_id:
    type: list
    elements: str
    description:
      - Constrains authenticating instances based on VPC ID.
      - Requires I(inferred_entity_type=ec2_instance).
  bound_subnet_id:
    type: list
    elements: str
    description:
      - Constrains authenticating instances based on subnet ID.
      - Requires I(inferred_entity_type=ec2_instance).
  bound_iam_role_arn:
    type: list
    elements: str
    description:
      - Constrains authenticating instances based on IAM role.
      - Requires I(inferred_entity_type=ec2_instance).
  bound_iam_instance_profile_arn:
    type: list
    elements: str
    description:
      - Constrains authenticating instances based on IAM instance profile.
      - Requires I(inferred_entity_type=ec2_instance).
  bound_ec2_instance_id:
    type: list
    elements: str
    description:
      - Constrains authenticating instances based on instance ID.
      - Requires I(inferred_entity_type=ec2_instance).
  bound_iam_principal_arn:
    type: list
    elements: str
    description:
      - Constrains authentication based on IAM principal.
      - If I(resolve_aws_unique_ids=false) then non-wildcard role ARNs must
        omit any path components
        (`arn:aws:iam::123456789012:role/some/path/to/MyRoleName`
        becomes `arn:aws:iam::123456789012:role/MyRoleName`).
  inferred_entity_type:
    type: str
    choices:
      - ec2_instance
    description:
      - Enables additional constraints by telling Vault to assume that the
        authenticating entity is an EC2 instance.
      - Requires I(inferred_aws_region)
  inferred_aws_region:
    type: str
    description:
      - Region to search for instances when I(inferred_entity_type=ec2_instance).
  resolve_aws_unique_ids:
    type: bool
    default: true
    description:
      - Resolves non-wildcard values from I(bound_iam_pricipal_arn) to unique
        IDs, so that principals which are destroyed and recreated do not
        continue to receive the old privileges.
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ..module_utils.base import hvault_token_argument_spec
from ..module_utils.module import HVaultModule


def main():
    argspec = dict(
        mount_point=dict(
            default='aws',
        ),
    )

    optspec = hvault_token_argument_spec()

    optspec.update(
        dict(
            bound_ami_id=dict(
                type='list',
                elements='str',
            ),
            bound_account_id=dict(
                type='list',
                elements='str',
            ),
            bound_region=dict(
                type='list',
                elements='str',
            ),
            bound_vpc_id=dict(
                type='list',
                elements='str',
            ),
            bound_subnet_id=dict(
                type='list',
                elements='str',
            ),
            bound_iam_role_arn=dict(
                type='list',
                elements='str',
            ),
            bound_iam_instance_profile_arn=dict(
                type='list',
                elements='str',
            ),
            bound_ec2_instance_id=dict(
                type='list',
                elements='str',
            ),
            bound_iam_principal_arn=dict(
                type='list',
                elements='str',
            ),
            inferred_entity_type=dict(
                choices=["ec2_instance"],
            ),
            inferred_aws_region=dict(),
            resolve_aws_unique_ids=dict(
                type='bool',
                default=True,
            ),
        )
    )

    module = HVaultModule(
        argspec=argspec,
        optspec=optspec,
        required_together=[
            ['inferred_entity_type', 'inferred_aws_region'],
        ],
        required_by={
            'bound_ami_id': 'inferred_entity_type',
            'bound_account_id': 'inferred_entity_type',
            'bound_region': 'inferred_entity_type',
            'bound_vpc_id': 'inferred_entity_type',
            'bound_subnet_id': 'inferred_entity_type',
            'bound_iam_role_arn': 'inferred_entity_type',
            'bound_iam_instance_profile_arn': 'inferred_entity_type',
            'bound_ec2_instance_id': 'inferred_entity_type',
        }
    )

    module.run(
        path_fmt='auth/{0}/role/{1}',
        config=dict(auth_type='iam'),
        bad_keys=[
            'allow_instance_migration',
            'disallow_reauthentication',
            'role_id',
            'role_tag',
        ],
    )


if __name__ == '__main__':
    main()
