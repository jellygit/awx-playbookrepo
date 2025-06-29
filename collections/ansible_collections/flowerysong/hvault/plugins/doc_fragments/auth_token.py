# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


class ModuleDocFragment(object):
    DOCUMENTATION = '''
options:
  token:
    description:
      - Authentication token to use.
      - If this is not set then the contents of C(~/.vault-token) will be checked.
    type: str
'''

    # Ansible doesn't currently support listing environment sources in modules,
    # so they need to be split out into a separate fragment. This also allows us
    # to add ini and vars as configuration sources.
    PLUGINS = '''
options:
  token:
    env:
      - name: VAULT_TOKEN
    ini:
      - section: hvault
        key: token
    vars:
      - name: ansible_hvault_token
'''
