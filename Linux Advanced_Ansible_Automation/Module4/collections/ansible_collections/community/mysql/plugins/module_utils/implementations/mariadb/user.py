# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.community.mysql.plugins.module_utils.version import LooseVersion
from ansible_collections.community.mysql.plugins.module_utils.mysql import get_server_version


def use_old_user_mgmt(cursor):
    version = get_server_version(cursor)

    return LooseVersion(version) < LooseVersion("10.2")


def supports_identified_by_password(cursor):
    return True
