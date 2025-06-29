# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


class ModuleDocFragment(object):
    DOCUMENTATION = '''
options:
  mount_point:
    description:
      - Path where the backend is mounted.
    type: str
  name:
    description:
      - Name of the role to manage.
    type: str
    required: true
  state:
    description:
      - Desired state of the role.
    type: str
    choices:
      - present
      - absent
    default: present
'''
