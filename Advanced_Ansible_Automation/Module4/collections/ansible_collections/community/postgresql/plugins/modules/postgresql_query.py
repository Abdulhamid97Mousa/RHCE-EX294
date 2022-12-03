#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2017, Felix Archambault
# Copyright: (c) 2019, Andrew Klychkov (@Andersson007) <aaklychkov@mail.ru>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: postgresql_query
short_description: Run PostgreSQL queries
description:
- Runs arbitrary PostgreSQL queries.
- B(WARNING) The C(path_to_script) and C(as_single_query) options as well as
  the C(query_list) and C(query_all_results) return values have been B(deprecated) and
  will be removed in community.postgresql 3.0.0, please use the
  M(community.postgresql.postgresql_script) module to execute statements from scripts.
- Does not run against backup files. Use M(community.postgresql.postgresql_db) with I(state=restore)
  to run queries on files made by pg_dump/pg_dumpall utilities.
options:
  query:
    description:
    - SQL query to run. Variables can be escaped with psycopg2 syntax
      U(http://initd.org/psycopg/docs/usage.html).
    type: str
  positional_args:
    description:
    - List of values to be passed as positional arguments to the query.
      When the value is a list, it will be converted to PostgreSQL array.
    - Mutually exclusive with I(named_args).
    type: list
    elements: raw
  named_args:
    description:
    - Dictionary of key-value arguments to pass to the query.
      When the value is a list, it will be converted to PostgreSQL array.
    - Mutually exclusive with I(positional_args).
    type: dict
  path_to_script:
    description:
    - This option has been B(deprecated) and will be removed in community.postgresql 3.0.0,
      please use the M(community.postgresql.postgresql_script) module to execute
      statements from scripts.
    - Path to a SQL script on the target machine.
    - If the script contains several queries, they must be semicolon-separated.
    - To run scripts containing objects with semicolons
      (for example, function and procedure definitions), use I(as_single_query=true).
    - To upload dumps or to execute other complex scripts, the preferable way
      is to use the M(community.postgresql.postgresql_db) module with I(state=restore).
    - Mutually exclusive with I(query).
    type: path
  session_role:
    description:
    - Switch to session_role after connecting. The specified session_role must
      be a role that the current login_user is a member of.
    - Permissions checking for SQL commands is carried out as though
      the session_role were the one that had logged in originally.
    type: str
  db:
    description:
    - Name of database to connect to and run queries against.
    type: str
    aliases:
    - login_db
  autocommit:
    description:
    - Execute in autocommit mode when the query can't be run inside a transaction block
      (e.g., VACUUM).
    - Mutually exclusive with I(check_mode).
    type: bool
    default: false
  encoding:
    description:
    - Set the client encoding for the current session (e.g. C(UTF-8)).
    - The default is the encoding defined by the database.
    type: str
    version_added: '0.2.0'
  trust_input:
    description:
    - If C(false), check whether a value of I(session_role) is potentially dangerous.
    - It makes sense to use C(false) only when SQL injections via I(session_role) are possible.
    type: bool
    default: true
    version_added: '0.2.0'
  search_path:
    description:
    - List of schema names to look in.
    type: list
    elements: str
    version_added: '1.0.0'
  as_single_query:
    description:
    - This option has been B(deprecated) and will be removed in community.postgresql 3.0.0,
      please use the M(community.postgresql.postgresql_script) module to execute
      statements from scripts.
    - If C(true), when reading from the I(path_to_script) file,
      executes its whole content in a single query (not splitting it up
      into separate queries by semicolons). It brings the following changes in
      the module's behavior.
    - When C(true), the C(query_all_results) return value
      contains only the result of the last statement.
    - Whether the state is reported as changed or not
      is determined by the last statement of the file.
    - Used only when I(path_to_script) is specified, otherwise ignored.
    - If set to C(false), the script can contain only semicolon-separated queries.
      (see the I(path_to_script) option documentation).
    type: bool
    default: true
    version_added: '1.1.0'
seealso:
- module: community.postgresql.postgresql_script
- module: community.postgresql.postgresql_db
- name: PostgreSQL Schema reference
  description: Complete reference of the PostgreSQL schema documentation.
  link: https://www.postgresql.org/docs/current/ddl-schemas.html
author:
- Felix Archambault (@archf)
- Andrew Klychkov (@Andersson007)
- Will Rouesnel (@wrouesnel)
extends_documentation_fragment:
- community.postgresql.postgres
notes:
- Supports C(check_mode).
'''

EXAMPLES = r'''
- name: Simple select query to acme db
  community.postgresql.postgresql_query:
    db: acme
    query: SELECT version()

- name: Select query to db acme with positional arguments and non-default credentials
  community.postgresql.postgresql_query:
    db: acme
    login_user: django
    login_password: mysecretpass
    query: SELECT * FROM acme WHERE id = %s AND story = %s
    positional_args:
    - 1
    - test

- name: Select query to test_db with named_args
  community.postgresql.postgresql_query:
    db: test_db
    query: SELECT * FROM test WHERE id = %(id_val)s AND story = %(story_val)s
    named_args:
      id_val: 1
      story_val: test

- name: Insert query to test_table in db test_db
  community.postgresql.postgresql_query:
    db: test_db
    query: INSERT INTO test_table (id, story) VALUES (2, 'my_long_story')

- name: Use connect_params to add any additional connection parameters that libpg supports
  community.postgresql.postgresql_query:
    connect_params:
      target_session_attrs: read-write
      connect_timeout: 10
    login_host: "host1,host2"
    login_user: "test"
    login_password: "test1234"
    db: 'test'
    query: 'insert into test (test) values (now())'


# WARNING: The path_to_script and as_single_query options have been deprecated
# and will be removed in community.postgresql 3.0.0, please
# use the community.postgresql.postgresql_script module instead.
# If your script contains semicolons as parts of separate objects
# like functions, procedures, and so on, use "as_single_query: true"
- name: Run queries from SQL script using UTF-8 client encoding for session
  community.postgresql.postgresql_query:
    db: test_db
    path_to_script: /var/lib/pgsql/test.sql
    positional_args:
    - 1
    encoding: UTF-8

- name: Example of using autocommit parameter
  community.postgresql.postgresql_query:
    db: test_db
    query: VACUUM
    autocommit: true

- name: >
    Insert data to the column of array type using positional_args.
    Note that we use quotes here, the same as for passing JSON, etc.
  community.postgresql.postgresql_query:
    query: INSERT INTO test_table (array_column) VALUES (%s)
    positional_args:
    - '{1,2,3}'

# Pass list and string vars as positional_args
- name: Set vars
  ansible.builtin.set_fact:
    my_list:
    - 1
    - 2
    - 3
    my_arr: '{1, 2, 3}'

- name: Select from test table by passing positional_args as arrays
  community.postgresql.postgresql_query:
    query: SELECT * FROM test_array_table WHERE arr_col1 = %s AND arr_col2 = %s
    positional_args:
    - '{{ my_list }}'
    - '{{ my_arr|string }}'

# Select from test table looking into app1 schema first, then,
# if the schema doesn't exist or the table hasn't been found there,
# try to find it in the schema public
- name: Select from test using search_path
  community.postgresql.postgresql_query:
    query: SELECT * FROM test_array_table
    search_path:
    - app1
    - public

# If you use a variable in positional_args / named_args that can
# be undefined and you wish to set it as NULL, the constructions like
# "{{ my_var if (my_var is defined) else none | default(none) }}"
# will not work as expected substituting an empty string instead of NULL.
# If possible, we suggest to use Ansible's DEFAULT_JINJA2_NATIVE configuration
# (https://docs.ansible.com/ansible/latest/reference_appendices/config.html#default-jinja2-native).
# Enabling it fixes this problem. If you cannot enable it, the following workaround
# can be used.
# You should precheck such a value and define it as NULL when undefined.
# For example:
- name: When undefined, set to NULL
  set_fact:
    my_var: NULL
  when: my_var is undefined

# Then:
- name: Insert a value using positional arguments
  community.postgresql.postgresql_query:
    query: INSERT INTO test_table (col1) VALUES (%s)
    positional_args:
    - '{{ my_var }}'
'''

RETURN = r'''
query:
    description:
    - Executed query.
    - When reading several queries from a file, it contains only the last one.
    returned: always
    type: str
    sample: 'SELECT * FROM bar'
statusmessage:
    description:
    - Attribute containing the message returned by the command.
    - When reading several queries from a file, it contains a message of the last one.
    returned: always
    type: str
    sample: 'INSERT 0 1'
query_result:
    description:
    - List of dictionaries in column:value form representing returned rows.
    - When running queries from a file, returns result of the last query.
    returned: always
    type: list
    elements: dict
    sample: [{"Column": "Value1"},{"Column": "Value2"}]
query_list:
    description:
    - This return value has been B(deprecated) and will be removed in
      community.postgresql 3.0.0.
    - List of executed queries.
      Useful when reading several queries from a file.
    returned: always
    type: list
    elements: str
    sample: ['SELECT * FROM foo', 'SELECT * FROM bar']
query_all_results:
    description:
    - This return value has been B(deprecated) and will be removed in
      community.postgresql 3.0.0.
    - List containing results of all queries executed (one sublist for every query).
      Useful when reading several queries from a file.
    returned: always
    type: list
    elements: list
    sample: [[{"Column": "Value1"},{"Column": "Value2"}], [{"Column": "Value1"},{"Column": "Value2"}]]
rowcount:
    description:
    - Number of produced or affected rows.
    - When using a script with multiple queries,
      it contains a total number of produced or affected rows.
    returned: changed
    type: int
    sample: 5
'''

try:
    from psycopg2 import ProgrammingError as Psycopg2ProgrammingError
    from psycopg2.extras import DictCursor
except ImportError:
    # it is needed for checking 'no result to fetch' in main(),
    # psycopg2 availability will be checked by connect_to_db() into
    # ansible.module_utils.postgres
    pass

import re

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.postgresql.plugins.module_utils.database import (
    check_input,
)
from ansible_collections.community.postgresql.plugins.module_utils.postgres import (
    connect_to_db,
    convert_elements_to_pg_arrays,
    convert_to_supported,
    ensure_required_libs,
    get_conn_params,
    postgres_common_argument_spec,
    set_search_path,
    TYPES_NEED_TO_CONVERT,
)
from ansible.module_utils._text import to_native
from ansible.module_utils.six import iteritems

# ===========================================
# Module execution.
#


def insane_query(string):
    for c in string:
        if c not in (' ', '\n', '', '\t'):
            return False

    return True


def main():
    argument_spec = postgres_common_argument_spec()
    argument_spec.update(
        query=dict(type='str'),
        db=dict(type='str', aliases=['login_db']),
        positional_args=dict(type='list', elements='raw'),
        named_args=dict(type='dict'),
        session_role=dict(type='str'),
        path_to_script=dict(type='path'),
        autocommit=dict(type='bool', default=False),
        encoding=dict(type='str'),
        trust_input=dict(type='bool', default=True),
        search_path=dict(type='list', elements='str'),
        as_single_query=dict(type='bool', default=True),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=(('positional_args', 'named_args'),),
        supports_check_mode=True,
    )

    query = module.params["query"]
    positional_args = module.params["positional_args"]
    named_args = module.params["named_args"]
    path_to_script = module.params["path_to_script"]
    autocommit = module.params["autocommit"]
    encoding = module.params["encoding"]
    session_role = module.params["session_role"]
    trust_input = module.params["trust_input"]
    search_path = module.params["search_path"]
    as_single_query = module.params["as_single_query"]

    if not trust_input:
        # Check input for potentially dangerous elements:
        check_input(module, session_role)

    if autocommit and module.check_mode:
        module.fail_json(msg="Using autocommit is mutually exclusive with check_mode")

    if path_to_script and query:
        module.fail_json(msg="path_to_script is mutually exclusive with query")

    query_list = []
    if path_to_script:
        depr_msg = ("The 'path_to_script' option is deprecated. Please use the "
                    "'community.postgresql.postgresql_script' module to execute "
                    "statements from scripts")
        module.deprecate(msg=depr_msg, version="3.0.0", collection_name="community.postgresql")

        try:
            with open(path_to_script, 'rb') as f:
                query = to_native(f.read())

                if not as_single_query:
                    depr_msg = ("The 'as_single_query' option is deprecated. Please use the "
                                "'community.postgresql.postgresql_script' module to execute "
                                "statements from scripts")
                    module.deprecate(msg=depr_msg, version="3.0.0", collection_name="community.postgresql")

                    if ';' in query:
                        for q in query.split(';'):
                            if insane_query(q):
                                continue
                            else:
                                query_list.append(q)
                    else:
                        query_list.append(query)
                else:
                    query_list.append(query)

        except Exception as e:
            module.fail_json(msg="Cannot read file '%s' : %s" % (path_to_script, to_native(e)))
    else:
        query_list.append(query)

    # Ensure psycopg2 libraries are available before connecting to DB:
    ensure_required_libs(module)
    conn_params = get_conn_params(module, module.params)
    db_connection, dummy = connect_to_db(module, conn_params, autocommit=autocommit)
    if encoding is not None:
        db_connection.set_client_encoding(encoding)
    cursor = db_connection.cursor(cursor_factory=DictCursor)

    if search_path:
        set_search_path(cursor, '%s' % ','.join([x.strip(' ') for x in search_path]))

    # Prepare args:
    if positional_args:
        args = positional_args
    elif named_args:
        args = named_args
    else:
        args = None

    # Convert elements of type list to strings
    # representing PG arrays
    if args:
        args = convert_elements_to_pg_arrays(args)

    # Set defaults:
    changed = False

    query_all_results = []
    rowcount = 0
    statusmessage = ''

    # Execute query:
    for query in query_list:
        try:
            cursor.execute(query, args)
            statusmessage = cursor.statusmessage
            if cursor.rowcount > 0:
                rowcount += cursor.rowcount

            query_result = []
            try:
                for row in cursor.fetchall():
                    # Ansible engine does not support decimals.
                    # An explicit conversion is required on the module's side
                    row = dict(row)
                    for (key, val) in iteritems(row):
                        if isinstance(val, TYPES_NEED_TO_CONVERT):
                            row[key] = convert_to_supported(val)

                    query_result.append(row)

            except Psycopg2ProgrammingError as e:
                if to_native(e) == 'no results to fetch':
                    query_result = {}

            except Exception as e:
                module.fail_json(msg="Cannot fetch rows from cursor: %s" % to_native(e))

            query_all_results.append(query_result)

            if 'SELECT' not in statusmessage:
                if re.search(re.compile(r'(UPDATE|INSERT|DELETE)'), statusmessage):
                    s = statusmessage.split()
                    if len(s) == 3:
                        if s[2] != '0':
                            changed = True

                    elif len(s) == 2:
                        if s[1] != '0':
                            changed = True

                    else:
                        changed = True

                else:
                    changed = True

        except Exception as e:
            if not autocommit:
                db_connection.rollback()

            cursor.close()
            db_connection.close()
            module.fail_json(msg="Cannot execute SQL '%s' %s: %s, query list: %s" % (query, args, to_native(e), query_list))

    if module.check_mode:
        db_connection.rollback()
    else:
        if not autocommit:
            db_connection.commit()

    kw = dict(
        changed=changed,
        query=cursor.query,
        query_list=query_list,
        statusmessage=statusmessage,
        query_result=query_result,
        query_all_results=query_all_results,
        rowcount=rowcount,
    )

    cursor.close()
    db_connection.close()

    module.exit_json(**kw)


if __name__ == '__main__':
    main()
