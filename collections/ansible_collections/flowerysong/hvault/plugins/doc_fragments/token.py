# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


class ModuleDocFragment(object):
    DOCUMENTATION = '''
options:
  token_ttl:
    type: int
    default: 0
    description:
      - The incremental lifetime for renewed tokens.
  token_max_ttl:
    type: int
    default: 0
    description:
      - The maximum lifetime for generated tokens.
  token_policies:
    type: list
    elements: str
    default: []
    description:
      - List of policies to add to generated tokens.
      - Depending on the auth method, this list may be supplemented by
        user/group/other values.
  token_bound_cidrs:
    type: list
    elements: str
    default: []
    description:
      - CIDR blocks that are allowed to authenticate.
      - The resulting token will also be tied to these blocks.
  token_explicit_max_ttl:
    type: int
    default: 0
    description:
      - Explicit max TTL for generated tokens.
      - This is a hard cap even if I(token_ttl) and I(token_max_ttl) would
        still allow a renewal.
  token_no_default_policy:
    type: bool
    default: false
    description:
      - Disable adding the default policy to generated tokens.
      - Normally this policy is added in addition to the explicit policies in
        I(token_policies).
  token_num_uses:
    type: int
    default: 0
    description:
      - The maximum number of times a generated token can be used.
      - C(0) is unlimited.
      - If this is set to a non-zero value the token will not be able to create
        child tokens.
  token_period:
    type: int
    default: 0
    description:
      - The period to set on the token.
  token_type:
    description:
      - Type of token that should be returned.
      - C(default) uses the setting from the mount.
    type: str
    choices:
      - default
      - service
      - batch
    default: default
'''
