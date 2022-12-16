# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from ansible_collections.community.mysql.plugins.module_utils.implementations.mariadb.user import (
    supports_identified_by_password,
)
from ..utils import dummy_cursor_class


@pytest.mark.parametrize(
    'function_return,cursor_output,cursor_ret_type',
    [
        (True, '10.5.0-mariadb', 'dict'),
        (True, '10.5.1-mariadb', 'dict'),
        (True, '10.6.0-mariadb', 'dict'),
        (True, '11.5.1-mariadb', 'dict'),
    ]
)
def test_supports_identified_by_password(function_return, cursor_output, cursor_ret_type):
    """
    Tests whether 'CREATE USER %s@%s IDENTIFIED BY PASSWORD %s' is supported,
    which is currently supported by everything besides MySQL >= 8.0.
    """
    cursor = dummy_cursor_class(cursor_output, cursor_ret_type)
    assert supports_identified_by_password(cursor) == function_return
