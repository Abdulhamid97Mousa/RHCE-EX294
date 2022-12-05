#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Andrew Klychkov (@Andersson007) <aaklychkov@mail.ru>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: postgresql_script

short_description: Run PostgreSQL statements from a file

description:
- Runs arbitrary PostgreSQL statements from a file.
- The module always reports that the state has changed.
- Does not run against backup files.
  Use M(community.postgresql.postgresql_db) with I(state=restore)
  to run queries on files made by pg_dump/pg_dumpall utilities.

version_added: '2.1.0'

options:
  positional_args:
    description:
    - List of values to substitute variable placeholders within the file content.
    - When the value is a list, it will be converted to PostgreSQL array.
    - Mutually exclusive with I(named_args).
    type: list
    elements: raw
  named_args:
    description:
    - Dictionary of key-value arguments to substitute
      variable placeholders within the file content.
    - When the value is a list, it will be converted to PostgreSQL array.
    - Mutually exclusive with I(positional_args).
    type: dict
  path:
    description:
    - Path to a SQL script on the target machine.
    - To upload dumps, the preferable way
      is to use the M(community.postgresql.postgresql_db) module with I(state=restore).
    type: path
  session_role:
    description:
    - Switch to C(session_role) after connecting. The specified role must
      be a role that the current C(login_user) is a member of.
    - Permissions checking for SQL commands is carried out as though
      the C(session_role) were the one that had logged in originally.
    type: str
  db:
    description:
    - Name of database to connect to and run queries against.
    type: str
    aliases:
    - login_db
  encoding:
    description:
    - Set the client encoding for the current session (e.g. C(UTF-8)).
    - The default is the encoding defined by the database.
    type: str
  trust_input:
    description:
    - If C(false), check whether a value of I(session_role) is potentially dangerous.
    - It makes sense to use C(false) only when SQL injections
      via I(session_role) are possible.
    type: bool
    default: true
  search_path:
    description:
    - Overrides the list of schemas to search for db objects in.
    type: list
    elements: str

seealso:
- module: community.postgresql.postgresql_db
- module: community.postgresql.postgresql_query
- name: PostgreSQL Schema reference
  description: Complete reference of the PostgreSQL schema documentation.
  link: https://www.postgresql.org/docs/current/ddl-schemas.html

author:
- Douglas J Hunley (@hunleyd)
- A. Hart (@jtelcontar)
- Daniel Scharon (@DanScharon)
- Andrew Klychkov (@Andersson007)

extends_documentation_fragment:
- community.postgresql.postgres

notes:
- Does not support C(check_mode).
'''

EXAMPLES = r'''
# Assuming that the file contains
# SELECT * FROM id_talbe WHERE id = %s,
# '%s' will be substituted with 1
- name: Run query from SQL script using UTF-8 client encoding for session and positional args
  community.postgresql.postgresql_script:
    db: test_db
    path: /var/lib/pgsql/test.sql
    positional_args:
      - 1
    encoding: UTF-8

# Assuming that the file contains
# SELECT * FROM test WHERE id = %(id_val)s AND story = %(story_val)s,
# %-values will be substituted with 1 and 'test'
- name: Select query to test_db with named_args
  community.postgresql.postgresql_script:
    db: test_db
    path: /var/lib/pgsql/test.sql
    named_args:
      id_val: 1
      story_val: test

- block:
  # Assuming that the the file contains
  # SELECT * FROM test_array_table WHERE arr_col1 = %s AND arr_col2 = %s
  # Pass list and string vars as positional_args
  - name: Set vars
    ansible.builtin.set_fact:
      my_list:
      - 1
      - 2
      - 3
      my_arr: '{1, 2, 3}'
  - name: Passing positional_args as arrays
    community.postgresql.postgresql_script:
      path: /var/lib/pgsql/test.sql
      positional_args:
        - '{{ my_list }}'
        - '{{ my_arr|string }}'

# Assuming that the the file contains
# SELECT * FROM test_table,
# look into app1 schema first, then,
# if the schema doesn't exist or the table hasn't been found there,
# try to find it in the schema public
- name: Select from test using search_path
  community.postgresql.postgresql_script:
    path: /var/lib/pgsql/test.sql
    search_path:
    - app1
    - public

- block:
    # If you use a variable in positional_args/named_args that can
    # be undefined and you wish to set it as NULL, constructions like
    # "{{ my_var if (my_var is defined) else none | default(none) }}"
    # will not work as expected substituting an empty string instead of NULL.
    # If possible, we suggest using Ansible's DEFAULT_JINJA2_NATIVE configuration
    # (https://docs.ansible.com/ansible/latest/reference_appendices/config.html#default-jinja2-native).
    # Enabling it fixes this problem. If you cannot enable it, the following workaround
    # can be used.
    # You should precheck such a value and define it as NULL when undefined.
    # For example:
    - name: When undefined, set to NULL
      set_fact:
        my_var: NULL
      when: my_var is undefined

    # Then, assuming that the file contains
    # INSERT INTO test_table (col1) VALUES (%s)
    - name: Insert a value using positional arguments
      community.postgresql.postgresql_script:
        path: /var/lib/pgsql/test.sql
        positional_args:
          - '{{ my_var }}'
'''

RETURN = r'''
query:
    description:
    - Executed query.
    - When the C(positional_args) or C(named_args) options are used,
      the query contains all variables that were substituted
      inside the database connector.
    returned: always
    type: str
    sample: 'SELECT * FROM bar'
statusmessage:
    description:
    - Attribute containing the message returned by the database connector
      after executing the script content.
    - When there are several statements in the script, returns a message
      related to the last statement.
    returned: always
    type: str
    sample: 'INSERT 0 1'
query_result:
    description:
    - List of dictionaries in the column:value form representing returned rows.
    - When there are several statements in the script,
      returns result of the last statement.
    returned: always
    type: list
    elements: dict
    sample: [{"Column": "Value1"},{"Column": "Value2"}]
rowcount:
    description:
    - Number of produced or affected rows.
    - When there are several statements in the script,
      returns a number of rows affected by the last statement.
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
    list_to_pg_array,
    postgres_common_argument_spec,
    set_search_path,
    TYPES_NEED_TO_CONVERT,
)
from ansible.module_utils._text import to_native
from ansible.module_utils.six import iteritems

# ===========================================
# Module execution.
#


def main():
    argument_spec = postgres_common_argument_spec()
    argument_spec.update(
        path=dict(type='path'),
        db=dict(type='str', aliases=['login_db']),
        positional_args=dict(type='list', elements='raw'),
        named_args=dict(type='dict'),
        session_role=dict(type='str'),
        encoding=dict(type='str'),
        trust_input=dict(type='bool', default=True),
        search_path=dict(type='list', elements='str'),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=(('positional_args', 'named_args'),),
        supports_check_mode=False,
    )

    path = module.params["path"]
    positional_args = module.params["positional_args"]
    named_args = module.params["named_args"]
    encoding = module.params["encoding"]
    session_role = module.params["session_role"]
    trust_input = module.params["trust_input"]
    search_path = module.params["search_path"]

    if not trust_input:
        # Check input for potentially dangerous elements:
        check_input(module, session_role)

    try:
        with open(path, 'rb') as f:
            script_content = to_native(f.read())

    except Exception as e:
        module.fail_json(msg="Cannot read file '%s' : %s" % (path, to_native(e)))

    # Ensure psycopg2 libraries are available before connecting to DB:
    ensure_required_libs(module)
    conn_params = get_conn_params(module, module.params)
    db_connection, dummy = connect_to_db(module, conn_params, autocommit=True)
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

    # Execute script content:
    try:
        cursor.execute(script_content, args)
    except Exception as e:
        cursor.close()
        db_connection.close()
        module.fail_json(msg="Cannot execute SQL '%s' %s: %s" % (script_content, args, to_native(e)))

    statusmessage = cursor.statusmessage

    rowcount = cursor.rowcount

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
        if to_native(e) == "no results to fetch":
            query_result = {}

    except Exception as e:
        module.fail_json(msg="Cannot fetch rows from cursor: %s" % to_native(e))

    kw = dict(
        changed=True,
        query=cursor.query,
        statusmessage=statusmessage,
        query_result=query_result,
        rowcount=rowcount,
    )

    cursor.close()
    db_connection.close()

    module.exit_json(**kw)


if __name__ == '__main__':
    main()
