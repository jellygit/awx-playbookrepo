# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json
import os

from http.client import IncompleteRead
from time import sleep

from ansible.module_utils.basic import env_fallback
from ansible.module_utils.common.text.converters import jsonify
from ansible.module_utils.six.moves.urllib.error import (
    HTTPError,
    URLError,
)
from ansible.module_utils.urls import open_url


def hvault_argument_spec():
    return dict(
        vault_addr=dict(
            default='https://localhost:8200',
            fallback=(env_fallback, ['VAULT_ADDR']),
        ),
        token=dict(
            fallback=(env_fallback, ['VAULT_TOKEN']),
            no_log=True,
        ),
        http_agent=dict(type='str', default='ansible-httpget'),
        use_proxy=dict(type='bool', default=True),
        validate_certs=dict(type='bool', default=True),
        client_cert=dict(
            type='path',
            fallback=(env_fallback, ['VAULT_CLIENT_CERT']),
        ),
        client_key=dict(
            type='path',
            fallback=(env_fallback, ['VAULT_CLIENT_KEY']),
        ),
        timeout=dict(
            type='int',
            default=60,
        ),
    )


def hvault_token_argument_spec():
    return dict(
        token_ttl=dict(
            type='int',
            default=0,
            no_log=False,
        ),
        token_max_ttl=dict(
            type='int',
            default=0,
            no_log=False,
        ),
        token_policies=dict(
            type='list',
            elements='str',
            default=[],
            no_log=False,
        ),
        token_bound_cidrs=dict(
            type='list',
            elements='str',
            default=[],
            no_log=False,
        ),
        token_explicit_max_ttl=dict(
            type='int',
            default=0,
            no_log=False,
        ),
        token_no_default_policy=dict(
            type='bool',
            default=False,
            no_log=False,
        ),
        token_num_uses=dict(
            type='int',
            default=0,
            no_log=False,
        ),
        token_period=dict(
            type='int',
            default=0,
            no_log=False,
        ),
        token_type=dict(
            choices=[
                'default',
                'service',
                'batch',
            ],
            default='default',
            no_log=False,
        ),
    )


def hvault_compare(dict1, dict2, ignore_keys=None, unsorted_keys=None):
    diff = {}
    for key in ((set(dict1.keys()) | set(dict2.keys())) - set(ignore_keys or [])):
        v1 = dict1.get(key)
        v2 = dict2.get(key)
        if (v1 or v2):
            if key in (unsorted_keys or []):
                if v1 and not isinstance(v1, list):
                    v1 = v1.split(',')
                if v2 and not isinstance(v2, list):
                    v2 = v2.split(',')
                if sorted(v1 or []) != sorted(v2 or []):
                    diff[key] = {
                        'before': v1,
                        'after': v2,
                    }
            elif (v1 != v2):
                diff[key] = {
                    'before': v1,
                    'after': v2,
                }
    return diff


class HVaultClient():
    def __init__(self, params, module=None):
        self._module = module
        self.params = params
        self.params['vault_addr'] = params['vault_addr'].rstrip('/')
        if not params['token']:
            token_file = os.path.expanduser('~/.vault-token')
            if os.path.isfile(token_file):
                with open(token_file, 'r') as f:
                    self.params['token'] = f.read().strip()

    def _open_url(self, path, method, data=None, fatal=True):
        url = f'{self.params["vault_addr"]}/v1/{path}'

        headers = {}
        if self.params.get('token'):
            headers['X-Vault-Token'] = self.params['token']
        if data:
            headers['Content-type'] = 'application/json'

        attempt = 0
        while True:
            attempt += 1
            try:
                result = open_url(
                    url,
                    headers=headers,
                    method=method,
                    data=jsonify(data),
                    timeout=self.params['timeout'],
                    http_agent=self.params['http_agent'],
                    use_proxy=self.params['use_proxy'],
                    validate_certs=self.params['validate_certs'],
                    client_cert=self.params['client_cert'],
                    client_key=self.params['client_key'],
                ).read()
                if result:
                    return json.loads(result)
                return None

            except (ConnectionError, IncompleteRead) as e:
                if attempt < 5:
                    sleep(attempt)
                    continue
                if self._module:
                    failure = {
                        'msg': f'Failed to {method} {path}',
                    }
                    self._module.fail_json(**failure)
                raise ConnectionError(f'Failed to {method} {path}') from e

            except HTTPError as e:
                if fatal and self._module:
                    msg = f'Failed to {method} {path}: {e.reason} (HTTP {e.code})'
                    result = {}
                    try:
                        result = json.loads(e.read())
                    except Exception:   # oop
                        pass
                    failure = {
                        'msg': msg,
                        'headers': str(e.headers),
                        'result': result,
                    }
                    self._module.fail_json(**failure)
                raise

            except URLError as e:
                if fatal and self._module:
                    self._module.fail_json(msg=f'Failed to {method} {path}: {e.reason}')
                raise

    def get(self, path, fatal=True):
        return self._open_url(path, method='GET', fatal=fatal)

    def list(self, path, fatal=True):
        return self._open_url(path, method='LIST', fatal=fatal)

    def post(self, path, data, fatal=True):
        return self._open_url(path, method='POST', data=data, fatal=fatal)

    def put(self, path, data, fatal=True):
        return self._open_url(path, method='PUT', data=data, fatal=fatal)

    def delete(self, path, fatal=True):
        try:
            self._open_url(path, method='DELETE', fatal=False)
        except URLError as e:
            if getattr(e, 'code', 0) == 404:
                return False
            if fatal and self._module:
                self._module.fail_json(msg=f'Failed to DELETE {path}: {e.reason}')
            raise
        return True
