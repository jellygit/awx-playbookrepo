# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.base import (
    HVaultClient,
    hvault_argument_spec,
    hvault_compare,
)


class HVaultMountModule():
    def __init__(self, base_path, extra_config=None):
        self.base_path = base_path
        self.config_spec = dict(
            default_lease_ttl=dict(type='int', default=0),
            max_lease_ttl=dict(type='int', default=0),
            force_no_cache=dict(type='bool', default=False),
            audit_non_hmac_request_keys=dict(type='list', elements='str', no_log=False),
            audit_non_hmac_response_keys=dict(type='list', elements='str', no_log=False),
            listing_visibility=dict(choices=['hidden', 'unauth'], default='hidden'),
            passthrough_request_headers=dict(type='list', elements='str', no_log=False),
            allowed_response_headers=dict(type='list', elements='str'),
        )
        if extra_config:
            self.config_spec.update(extra_config)

        argspec = hvault_argument_spec()
        argspec.update(self.config_spec)
        argspec.update(
            dict(
                state=dict(choices=['present', 'absent'], default='present'),
                path=dict(required=True),
                force=dict(type='bool', default=False),
                type=dict(),
                description=dict(default=''),
                options=dict(type='dict'),
                local=dict(type='bool', default=False),
                plugin_version=dict(default=''),
                seal_wrap=dict(type='bool', default=False),
                external_entropy_access=dict(type='bool', default=False),
            )
        )

        self.module = AnsibleModule(
            supports_check_mode=True,
            argument_spec=argspec,
            required_if=[
                ['state', 'present', ['type']],
            ],
        )
        self.params = self.module.params
        self.client = HVaultClient(self.params, self.module)

    def _get_mount(self, path):
        return self.client.get(self.base_path)['data'].get(path + '/')

    def run(self):
        path = self.params['path'].rstrip('/')
        mount = self._get_mount(path)

        changed = False
        diff = {}
        if self.params['state'] == 'absent':
            if not mount:
                self.module.exit_json(changed=False)

            if not self.module.check_mode:
                self.client.delete(f'{self.base_path}/{path}')
            self.module.exit_json(changed=True, mount=mount)

        changed = False
        payload = {
            'options': {},
        }
        for key in ('type', 'description', 'local', 'seal_wrap', 'external_entropy_access'):
            payload[key] = self.params[key]

        for key in self.config_spec.keys():
            val = self.params[key]
            if val is not None:
                if 'config' not in payload:
                    payload['config'] = {}
                payload['config'][key] = val

        if self.params['options']:
            # FIXME: options is really annoying and obtuse; the only usage
            # that seems to exist is for versioning KV secret mount, which
            # is a string.
            for key, val in self.params['options'].items():
                payload['options'][key] = str(val)

        mount_path = f'{self.base_path}/{path}'
        if not mount:
            changed = True
            if not self.module.check_mode:
                self.client.post(mount_path, data=payload)
                mount = self._get_mount(path)
        else:
            diff = hvault_compare(mount, payload, ignore_keys=['accessor', 'deprecation_status', 'running_plugin_version', 'running_sha256', 'uuid'])
            if diff:
                changed = True

                if not self.module.check_mode:
                    if mount['type'] != payload['type']:
                        if not self.params['force']:
                            self.module.fail_json(f'Existing mount at {mount_path} is {mount["type"]} and force is false')
                        self.client.delete(mount_path)
                        self.client.post(mount_path, data=payload)
                    else:
                        # different structure than creation
                        payload.pop('type')
                        payload.update(payload.pop('config'))

                        # handle removed keys
                        for key in mount['config'].keys():
                            if key not in payload:
                                payload[key] = None

                        self.client.post(f'{self.base_path}/{path}/tune', data=payload)
                    mount = self._get_mount(path)

        self.module.exit_json(changed=changed, mount=mount, diff=diff)
