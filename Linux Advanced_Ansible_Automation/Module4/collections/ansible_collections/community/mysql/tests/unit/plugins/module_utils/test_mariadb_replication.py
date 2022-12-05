# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Andrew Klychkov (@Andersson007) <aaklychkov@mail.ru>

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from ansible_collections.community.mysql.plugins.module_utils.implementations.mariadb.replication import uses_replica_terminology
from ..utils import dummy_cursor_class


@pytest.mark.parametrize(
    'f_output,c_output,c_ret_type',
    [
        (False, '10.5.0-mariadb', 'dict'),
        (True, '10.5.1-mariadb', 'dict'),
        (True, '10.6.0-mariadb', 'dict'),
        (True, '11.5.1-mariadb', 'dict'),
    ]
)
def test_uses_replica_terminology(f_output, c_output, c_ret_type):
    cursor = dummy_cursor_class(c_output, c_ret_type)
    assert uses_replica_terminology(cursor) == f_output
