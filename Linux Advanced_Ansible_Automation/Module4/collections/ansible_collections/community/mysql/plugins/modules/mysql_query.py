#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Andrew Klychkov (@Andersson007) <aaklychkov@mail.ru>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: mysql_query
short_description: Run MySQL queries
description:
- Runs arbitrary MySQL queries.
- Pay attention, the module does not support check mode!
  All queries will be executed in autocommit mode.
- To run SQL queries from a file, use M(community.mysql.mysql_db) module.
version_added: '0.1.0'
options:
  query:
    description:
    - SQL query to run. Multiple queries can be passed using YAML list syntax.
    - Must be a string or YAML list containing strings.
    - Note that if you use the C(IF EXISTS/IF NOT EXISTS) clauses in your query
      and C(mysqlclient) connector, the module will report that
      the state has been changed even if it has not. If it is important in your
      workflow, use the C(PyMySQL) connector instead.
    type: raw
    required: yes
  positional_args:
    description:
    - List of values to be passed as positional arguments to the query.
    - Mutually exclusive with I(named_args).
    type: list
  named_args:
    description:
    - Dictionary of key-value arguments to pass to the query.
    - Mutually exclusive with I(positional_args).
    type: dict
  login_db:
    description:
    - Name of database to connect to and run queries against.
    type: str
  single_transaction:
    description:
    - Where passed queries run in a single transaction (C(yes)) or commit them one-by-one (C(no)).
    type: bool
    default: no
seealso:
- module: community.mysql.mysql_db
author:
- Andrew Klychkov (@Andersson007)
extends_documentation_fragment:
- community.mysql.mysql

'''

EXAMPLES = r'''
# If you encounter the "Please explicitly state intended protocol" error,
# use the login_unix_socket argument
- name: Simple select query to acme db
  community.mysql.mysql_query:
    login_db: acme
    query: SELECT * FROM orders
    login_unix_socket: /run/mysqld/mysqld.sock

- name: Select query to db acme with positional arguments
  community.mysql.mysql_query:
    login_db: acme
    query: SELECT * FROM acme WHERE id = %s AND story = %s
    positional_args:
    - 1
    - test

- name: Select query to test_db with named_args
  community.mysql.mysql_query:
    login_db: test_db
    query: SELECT * FROM test WHERE id = %(id_val)s AND story = %(story_val)s
    named_args:
      id_val: 1
      story_val: test

- name: Run several insert queries against db test_db in single transaction
  community.mysql.mysql_query:
    login_db: test_db
    query:
    - INSERT INTO articles (id, story) VALUES (2, 'my_long_story')
    - INSERT INTO prices (id, price) VALUES (123, '100.00')
    single_transaction: yes
'''

RETURN = r'''
executed_queries:
    description: List of executed queries.
    returned: always
    type: list
    sample: ['SELECT * FROM bar', 'UPDATE bar SET id = 1 WHERE id = 2']
query_result:
    description:
    - List of lists (sublist for each query) containing dictionaries
      in column:value form representing returned rows.
    returned: changed
    type: list
    sample: [[{"Column": "Value1"},{"Column": "Value2"}], [{"ID": 1}, {"ID": 2}]]
rowcount:
    description: Number of affected rows for each subquery.
    returned: changed
    type: list
    sample: [5, 1]
'''

import warnings

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.mysql.plugins.module_utils.mysql import (
    mysql_connect,
    mysql_common_argument_spec,
    mysql_driver,
    mysql_driver_fail_msg,
)
from ansible.module_utils._text import to_native

DML_QUERY_KEYWORDS = ('INSERT', 'UPDATE', 'DELETE', 'REPLACE')
# TRUNCATE is not DDL query but it also returns 0 rows affected:
DDL_QUERY_KEYWORDS = ('CREATE', 'DROP', 'ALTER', 'RENAME', 'TRUNCATE')


# ===========================================
# Module execution.
#

def main():
    argument_spec = mysql_common_argument_spec()
    argument_spec.update(
        query=dict(type='raw', required=True),
        login_db=dict(type='str'),
        positional_args=dict(type='list'),
        named_args=dict(type='dict'),
        single_transaction=dict(type='bool', default=False),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=(
            ('positional_args', 'named_args'),
        ),
    )

    db = module.params['login_db']
    connect_timeout = module.params['connect_timeout']
    login_user = module.params['login_user']
    login_password = module.params['login_password']
    ssl_cert = module.params['client_cert']
    ssl_key = module.params['client_key']
    ssl_ca = module.params['ca_cert']
    check_hostname = module.params['check_hostname']
    config_file = module.params['config_file']
    query = module.params["query"]

    if not isinstance(query, (str, list)):
        module.fail_json(msg="the query option value must be a string or list, passed %s" % type(query))

    if isinstance(query, str):
        query = [query]

    for elem in query:
        if not isinstance(elem, str):
            module.fail_json(msg="the elements in query list must be strings, passed '%s' %s" % (elem, type(elem)))

    if module.params["single_transaction"]:
        autocommit = False
    else:
        autocommit = True
    # Prepare args:
    if module.params.get("positional_args"):
        arguments = module.params["positional_args"]
    elif module.params.get("named_args"):
        arguments = module.params["named_args"]
    else:
        arguments = None

    if mysql_driver is None:
        module.fail_json(msg=mysql_driver_fail_msg)

    # Connect to DB:
    try:
        cursor, db_connection = mysql_connect(module, login_user, login_password,
                                              config_file, ssl_cert, ssl_key, ssl_ca, db,
                                              check_hostname=check_hostname,
                                              connect_timeout=connect_timeout,
                                              cursor_class='DictCursor', autocommit=autocommit)
    except Exception as e:
        module.fail_json(msg="unable to connect to database, check login_user and "
                             "login_password are correct or %s has the credentials. "
                             "Exception message: %s" % (config_file, to_native(e)))

    # Set defaults:
    changed = False

    max_keyword_len = len(max(DML_QUERY_KEYWORDS + DDL_QUERY_KEYWORDS, key=len))

    # Execute query:
    query_result = []
    executed_queries = []
    rowcount = []

    already_exists = False
    for q in query:
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings(action='error',
                                        message='.*already exists*',
                                        category=mysql_driver.Warning)

                try:
                    cursor.execute(q, arguments)
                except mysql_driver.Warning:
                    # When something is run with IF NOT EXISTS
                    # and there's "already exists" MySQL warning,
                    # set the flag as True.
                    # PyMySQL throws the warning, mysqlclinet does NOT.
                    already_exists = True

        except Exception as e:
            if not autocommit:
                db_connection.rollback()

            cursor.close()
            module.fail_json(msg="Cannot execute SQL '%s' args [%s]: %s" % (q, arguments, to_native(e)))

        try:
            if not already_exists:
                query_result.append([dict(row) for row in cursor.fetchall()])

        except Exception as e:
            if not autocommit:
                db_connection.rollback()

            module.fail_json(msg="Cannot fetch rows from cursor: %s" % to_native(e))

        # Check DML or DDL keywords in query and set changed accordingly:
        q = q.lstrip()[0:max_keyword_len].upper()
        for keyword in DML_QUERY_KEYWORDS:
            if keyword in q and cursor.rowcount > 0:
                changed = True

        for keyword in DDL_QUERY_KEYWORDS:
            if keyword in q:
                if already_exists:
                    # Indicates the entity already exists
                    changed = False
                    already_exists = False  # Reset flag
                else:
                    changed = True
        try:
            executed_queries.append(cursor._last_executed)
        except AttributeError:
            # MySQLdb removed cursor._last_executed as a duplicate of cursor._executed
            executed_queries.append(cursor._executed)
        rowcount.append(cursor.rowcount)

    # When the module run with the single_transaction == True:
    if not autocommit:
        db_connection.commit()

    # Create dict with returned values:
    kw = {
        'changed': changed,
        'executed_queries': executed_queries,
        'query_result': query_result,
        'rowcount': rowcount,
    }

    # Exit:
    module.exit_json(**kw)


if __name__ == '__main__':
    main()
