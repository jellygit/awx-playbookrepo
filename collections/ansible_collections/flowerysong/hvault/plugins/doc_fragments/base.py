# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


class ModuleDocFragment(object):
    DOCUMENTATION = '''
options:
  vault_addr:
    description:
      - Location of the Vault service.
    type: str
    default: https://localhost:8200
  http_agent:
    description:
      - Header to identify as, generally appears in web server logs.
    type: str
    default: ansible-httpget
  use_proxy:
    description:
      - If C(no), it will not use a proxy, even if one is defined in an environment variable on the target hosts.
    type: bool
    default: yes
  validate_certs:
    description:
      - If C(no), TLS certificates will not be validated.
      - This should only be used on personally controlled sites using self-signed certificates.
    type: bool
    default: yes
  client_cert:
    description:
      - PEM formatted certificate chain file to be used for TLS client authentication.
      - This file can also include the key as well, and if the key is included, C(client_key) is not required.
    type: path
  client_key:
    description:
      - PEM formatted file that contains your private key to be used for TLS client authentication.
      - If C(client_cert) contains both the certificate and key, this option is not required.
    type: path
  timeout:
    description:
      - Request timeout, in seconds.
    type: int
    default: 60
'''

    # Ansible doesn't currently support listing environment sources in modules,
    # so they need to be split out into a separate fragment. This also allows us
    # to add ini and vars as configuration sources.
    PLUGINS = '''
options:
  vault_addr:
    env:
      - name: VAULT_ADDR
    ini:
      - section: hvault
        key: url
    vars:
      - name: ansible_hvault_addr
  http_agent:
    ini:
      - section: hvault
        key: http_agent
    vars:
      - name: ansible_hvault_http_agent
  use_proxy:
    ini:
      - section: hvault
        key: use_proxy
    vars:
      - name: ansible_hvault_use_proxy
  validate_certs:
    ini:
      - section: hvault
        key: validate_certs
    vars:
      - name: ansible_hvault_validate_certs
  client_cert:
    env:
      - name: VAULT_CLIENT_CERT
    ini:
      - section: hvault
        key: client_cert
    vars:
      - name: ansible_hvault_client_cert
  client_key:
    env:
      - name: VAULT_CLIENT_KEY
    ini:
      - section: hvault
        key: client_key
    vars:
      - name: ansible_hvault_client_key
'''
