# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


class ModuleDocFragment(object):
    DOCUMENTATION = '''
options:
  state:
    description:
      - Desired mount state.
    type: str
    choices:
      - present
      - absent
    default: present
  path:
    description:
      - Mount path.
    type: str
    required: true
  force:
    description:
      - Allow deletion of existing mounts with an incompatible type.
    type: bool
    default: false
  description:
    description:
      - Description of the mount point.
    type: str
    default: ''
  type:
    description:
      - Engine to mount on this path.
      - Required when I(state=present)
    type: str
  plugin_version:
    description:
      - Semantic version of the plugin to use, e.g. "v1.0.0"
      - If blank the engine will select a registered unversioned plugin, the
        best registered versioned plugin, or a built-in plugin (in that order
        of precendence.)
    type: str
    default: ''
  options:
    description:
      - Options to pass to the engine.
    type: dict
  external_entropy_access:
    description:
      - Allow access to Vault's external entropy source.
      - B(ENTERPRISE ONLY)
    type: bool
    default: false
  local:
    description:
      - Whether this mount is cluster-wide or local to this node.
      - B(ENTERPRISE ONLY)
    type: bool
    default: false
  seal_wrap:
    description:
      - Enable seal wrapping.
      - B(ENTERPRISE ONLY)
    type: bool
    default: false
  force_no_cache:
    description:
      - Disable caching.
    type: bool
    default: false
  default_lease_ttl:
    description:
      - Default lease duration, in seconds.
      - I(0) will use the system default.
    type: int
    default: 0
  max_lease_ttl:
    description:
      - Maximum lease duration, in seconds.
      - I(0) will use the system default.
    type: int
    default: 0
  audit_non_hmac_request_keys:
    description:
      - Request keys that should not be hashed in the audit logs.
    type: list
    elements: str
  audit_non_hmac_response_keys:
    description:
      - Response keys that should not be hashed in the audit logs.
    type:
      list
    elements: str
  listing_visibility:
    description:
      - Whether the mount should be shown in the UI.
    type: str
    choices:
      - hidden
      - unauth
    default: hidden
  passthrough_request_headers:
    description:
      - Headers that should be passed from the request to the plugin.
    type: list
    elements: str
  allowed_response_headers:
    description:
      - Headers that the plugin is allowed to return.
    type: list
    elements: str
'''
