# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from ansible_collections.community.mysql.plugins.modules.mysql_role import (
    MariaDBQueryBuilder,
    MySQLQueryBuilder,
    normalize_users,
)

# TODO: Also cover DbServer, Role, MySQLRoleImpl, MariaDBRoleImpl classes


class Module():
    def __init__(self):
        self.msg = None

    def fail_json(self, msg=None):
        self.msg = msg


module = Module()


@pytest.mark.parametrize(
    'builder,output',
    [
        (MariaDBQueryBuilder('role0'), ("SELECT count(*) FROM mysql.user WHERE user = %s AND is_role  = 'Y'", ('role0',))),
        (MySQLQueryBuilder('role0', '%'), ('SELECT count(*) FROM mysql.user WHERE user = %s AND host = %s', ('role0', '%'))),
        (MariaDBQueryBuilder('role1'), ("SELECT count(*) FROM mysql.user WHERE user = %s AND is_role  = 'Y'", ('role1',))),
        (MySQLQueryBuilder('role1', 'fake'), ('SELECT count(*) FROM mysql.user WHERE user = %s AND host = %s', ('role1', 'fake'))),
    ]
)
def test_query_builder_role_exists(builder, output):
    """Test role_exists method of the builder classes."""
    assert builder.role_exists() == output


@pytest.mark.parametrize(
    'builder,admin,output',
    [
        (MariaDBQueryBuilder('role0'), None, ('CREATE ROLE %s', ('role0',))),
        (MySQLQueryBuilder('role0', '%'), None, ('CREATE ROLE %s', ('role0',))),
        (MariaDBQueryBuilder('role1'), None, ('CREATE ROLE %s', ('role1',))),
        (MySQLQueryBuilder('role1', 'fake'), None, ('CREATE ROLE %s', ('role1',))),
        (MariaDBQueryBuilder('role0'), ('user0', ''), ('CREATE ROLE %s WITH ADMIN %s', ('role0', 'user0'))),
        (MySQLQueryBuilder('role0', '%'), ('user0', ''), ('CREATE ROLE %s', ('role0',))),
        (MariaDBQueryBuilder('role1'), ('user0', 'localhost'), ('CREATE ROLE %s WITH ADMIN %s@%s', ('role1', 'user0', 'localhost'))),
        (MySQLQueryBuilder('role1', 'fake'), ('user0', 'localhost'), ('CREATE ROLE %s', ('role1',))),
    ]
)
def test_query_builder_role_create(builder, admin, output):
    """Test role_create method of the builder classes."""
    assert builder.role_create(admin) == output


@pytest.mark.parametrize(
    'builder,user,output',
    [
        (MariaDBQueryBuilder('role0'), ('user0', ''), ('GRANT %s TO %s', ('role0', 'user0'))),
        (MySQLQueryBuilder('role0', '%'), ('user0', ''), ('GRANT %s@%s TO %s', ('role0', '%', 'user0'))),
        (MariaDBQueryBuilder('role1'), ('user0', 'localhost'), ('GRANT %s TO %s@%s', ('role1', 'user0', 'localhost'))),
        (MySQLQueryBuilder('role1', 'fake'), ('user0', 'localhost'), ('GRANT %s@%s TO %s@%s', ('role1', 'fake', 'user0', 'localhost'))),
    ]
)
def test_query_builder_role_grant(builder, user, output):
    """Test role_grant method of the builder classes."""
    assert builder.role_grant(user) == output


@pytest.mark.parametrize(
    'builder,user,output',
    [
        (MariaDBQueryBuilder('role0'), ('user0', ''), ('REVOKE %s FROM %s', ('role0', 'user0'))),
        (MySQLQueryBuilder('role0', '%'), ('user0', ''), ('REVOKE %s@%s FROM %s', ('role0', '%', 'user0'))),
        (MariaDBQueryBuilder('role1'), ('user0', 'localhost'), ('REVOKE %s FROM %s@%s', ('role1', 'user0', 'localhost'))),
        (MySQLQueryBuilder('role1', 'fake'), ('user0', 'localhost'), ('REVOKE %s@%s FROM %s@%s', ('role1', 'fake', 'user0', 'localhost'))),
    ]
)
def test_query_builder_role_revoke(builder, user, output):
    """Test role_revoke method of the builder classes."""
    assert builder.role_revoke(user) == output


@pytest.mark.parametrize(
    'input_,output,is_mariadb',
    [
        (['user'], [('user', '')], True),
        (['user'], [('user', '%')], False),
        (['user@%'], [('user', '%')], True),
        (['user@%'], [('user', '%')], False),
        (['user@localhost'], [('user', 'localhost')], True),
        (['user@localhost'], [('user', 'localhost')], False),
        (['user', 'user@%'], [('user', ''), ('user', '%')], True),
        (['user', 'user@%'], [('user', '%'), ('user', '%')], False),
    ]
)
def test_normalize_users(input_, output, is_mariadb):
    """Test normalize_users function with expected input."""
    assert normalize_users(None, input_, is_mariadb) == output


@pytest.mark.parametrize(
    'input_,is_mariadb,err_msg',
    [
        ([''], True, "Member's name cannot be empty."),
        ([''], False, "Member's name cannot be empty."),
        ([None], True, "Error occured while parsing"),
        ([None], False, "Error occured while parsing"),
    ]
)
def test_normalize_users_failing(input_, is_mariadb, err_msg):
    """Test normalize_users function with wrong input."""

    normalize_users(module, input_, is_mariadb)
    assert err_msg in module.msg
