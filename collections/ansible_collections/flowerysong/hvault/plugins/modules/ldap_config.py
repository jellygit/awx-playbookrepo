#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: ldap_config
author: "Paul Arthur (@flowerysong)"
short_description: Manage LDAP authentication in HashiCorp Vault
description:
  - Manage LDAP authentication in HashiCorp Vault.
version_added: 0.2.0
extends_documentation_fragment:
  - flowerysong.hvault.base
  - flowerysong.hvault.auth_token
  - flowerysong.hvault.token
options:
  mount_point:
    type: str
    default: ldap
    description:
      - Path under auth/ where the LDAP backend is mounted.
  url:
    type: list
    required: true
    elements: str
    description:
      - LDAP server(s) to connect to.
  case_sensitive_names:
    type: bool
    default: false
    description:
      - Determines whether user and group names are normalized to lowercase
        before being matched against policies.
      - Login requests are not affected by this setting, only policy matching.
  connection_timeout:
    type: int
    default: 30
    description:
      - Time, in seconds, before giving up on a connection attempt and trying the next LDAP server.
  request_timeout:
    type: int
    default: 90
    description:
      - Time, in seconds, to wait for a response from the LDAP server.
  max_page_size:
    type: int
    default: 0
    description:
      - Maximum number of results to request from the LDAP server at once.
      - The default value of 0 disables pagination.
  starttls:
    type: bool
    default: false
    description:
      - Negotiate TLS using STARTTLS.
  tls_min_version:
    type: str
    choices:
      - tls10
      - tls11
      - tls12
      - tls13
    default: tls12
    description:
      - Minimum TLS version to use.
  tls_max_version:
    type: str
    choices:
      - tls10
      - tls11
      - tls12
      - tls13
    default: tls12
    description:
      - Maximum TLS version to use.
  insecure_tls:
    type: bool
    default: false
    description:
      - Disable verification of the LDAP server's certificate.
  certificate:
    type: str
    description:
      - CA certificate to use for verifying the LDAP server's certificae, in X.509 PEM format.
  client_tls_cert:
    type: str
    description:
      - Client certificate to present during TLS negotiation, in X.509 PEM format.
  client_tls_key:
    type: str
    description:
      - Client key to use during TLS negotiation, in X.509 PEM format.
  binddn:
    type: str
    description:
      - Object to bind as before performing user searches.
  bindpass:
    type: str
    description:
      - Password for I(binddn).
  userdn:
    type: str
    description:
      - Base DN for user searches.
  userattr:
    type: str
    default: cn
    description:
      - Object attribute that will match the username passed during authentication.
  discoverdn:
    type: bool
    default: false
    description:
      - Perform an anonymous bind to discover the DN of a user.
  deny_null_bind:
    type: bool
    default: true
    description:
      - Prevent users from bypassing authentication by providing an empty password.
  dereference_aliases:
    type: str
    default: never
    choices:
      - never
      - finding
      - searching
      - always
    description:
      - How aliases are dereferenced when performing the search.
  upndomain:
    type: str
    description:
      - userPrincipalDomain used to construct the UPN string for the authenticating user.
  anonymous_group_search:
    type: bool
    default: false
    description:
      - Perform an anonymous bind to search for groups.
  groupfilter:
    type: str
    default: (|(memberUid={{.Username}})(member={{.UserDN}})(uniqueMember={{.UserDN}}))
    description:
      - Go template used to construct the group membership query.
  groupdn:
    type: str
    description:
      - Base DN for group searches.
  groupattr:
    type: str
    default: cn
    description:
      - LDAP attribute of objects returned by I(groupfilter) which should be
        used as the group name(s).
      - If the search returns user objects, this should be something like C(memberOf).
  use_token_groups:
    type: bool
    default: false
    description:
      - Use the Active Directory tokenGroups attribute to discover group membership.
  username_as_alias:
    type: bool
    default: false
    description:
      - Force authentication to use the username passed by the user as the alias name.
  userfilter:
    type: str
    default: ({{.UserAttr}}={{.Username}})
    description:
      - Go template used to construct a user search filter.
'''

EXAMPLES = '''
- name: Configure LDAP authentication
  flowerysong.hvault.ldap_config:
    url: ldaps://ldap.umich.edu
    userdn: ou=People,dc=umich,dc=edu
    userattr: cn
    groupdn: ou=User Groups,ou=Groups,dc=umich,dc=edu
    groupfilter: !unsafe (member={{.UserDN}})
    groupattr: cn
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.base import (
    HVaultClient,
    hvault_argument_spec,
    hvault_compare,
    hvault_token_argument_spec,
)
from ..module_utils.module import (
    optspec_to_argspec,
    optspec_to_config,
)


def main():
    argspec = hvault_argument_spec()
    argspec.update(
        dict(
            mount_point=dict(
                default='ldap',
            ),
        )
    )

    optspec = hvault_token_argument_spec()
    optspec.update(
        dict(
            url=dict(
                type='list',
                elements='str',
                required=True,
                join=True,
                sorted=True,
            ),
            case_sensitive_names=dict(
                type='bool',
                default=False,
            ),
            connection_timeout=dict(
                type='int',
                default='30',
            ),
            request_timeout=dict(
                type='int',
                default=90,
            ),
            max_page_size=dict(
                type='int',
                default=0,
            ),
            starttls=dict(
                type='bool',
                default=False,
            ),
            tls_min_version=dict(
                choices=['tls10', 'tls11', 'tls12', 'tls13'],
                default='tls12',
            ),
            tls_max_version=dict(
                choices=['tls10', 'tls11', 'tls12', 'tls13'],
                default='tls12',
            ),
            insecure_tls=dict(
                type='bool',
                default=False,
            ),
            certificate=dict(),
            client_tls_cert=dict(),
            client_tls_key=dict(no_log=True),
            binddn=dict(),
            bindpass=dict(no_log=True),
            userdn=dict(),
            userattr=dict(
                default='cn',
            ),
            discoverdn=dict(
                type='bool',
                default=False,
            ),
            deny_null_bind=dict(
                type='bool',
                default=True,
            ),
            dereference_aliases=dict(
                choices=[
                    'never',
                    'finding',
                    'searching',
                    'always',
                ],
                default='never',
            ),
            upndomain=dict(),
            anonymous_group_search=dict(
                type='bool',
                default='false',
            ),
            groupfilter=dict(
                default='(|(memberUid={{.Username}})(member={{.UserDN}})(uniqueMember={{.UserDN}}))'
            ),
            groupdn=dict(),
            groupattr=dict(
                default='cn',
            ),
            use_token_groups=dict(
                type='bool',
                default=False,
            ),
            username_as_alias=dict(
                type='bool',
                default=False,
            ),
            userfilter=dict(
                default='({{.UserAttr}}={{.Username}})',
            )
        )
    )
    argspec.update(optspec_to_argspec(optspec))

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    path = 'auth/{0}/config'.format(module.params['mount_point'])
    client = HVaultClient(module.params, module)

    config = client.get(path)['data']
    for k in ['bindpass', 'client_tls_cert', 'client_tls_key']:
        if k not in config:
            config[k] = None

    new_config = optspec_to_config(optspec, module.params)
    new_config['use_pre111_group_cn_behavior'] = False

    changed = False
    diff = hvault_compare(config, new_config, ignore_keys=['request_timeout'])
    if diff:
        changed = True
        if module.check_mode:
            config = new_config
        else:
            client.post(path, new_config)
            config = client.get(path)['data']

    module.exit_json(changed=changed, config=config, diff=diff)


if __name__ == '__main__':
    main()
