# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Andrew Klychkov (@Andersson007) <aaklychkov@mail.ru>

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from ansible_collections.community.mysql.plugins.module_utils.implementations.mysql.replication import uses_replica_terminology
from ..utils import dummy_cursor_class


@pytest.mark.parametrize(
    'f_output,c_output,c_ret_type',
    [
        (False, '5.5.1-mysql', 'list'),
        (False, '5.7.0-mysql', 'dict'),
        (False, '8.0.0-mysql', 'list'),
        (False, '8.0.11-mysql', 'dict'),
        (False, '8.0.21-mysql', 'list'),
        (True, '8.0.22-mysql', 'list'),
        (True, '8.1.2-mysql', 'dict'),
        (True, '9.0.0-mysql', 'list'),
    ]
)
def test_uses_replica_terminology(f_output, c_output, c_ret_type):
    cursor = dummy_cursor_class(c_output, c_ret_type)
    assert uses_replica_terminology(cursor) == f_output
