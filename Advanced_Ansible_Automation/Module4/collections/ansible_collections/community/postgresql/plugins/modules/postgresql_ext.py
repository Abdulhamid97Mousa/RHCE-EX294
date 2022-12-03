#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: postgresql_ext
short_description: Add or remove PostgreSQL extensions from a database
description:
- Add or remove PostgreSQL extensions from a database.
options:
  name:
    description:
    - Name of the extension to add or remove.
    required: true
    type: str
    aliases:
    - ext
  db:
    description:
    - Name of the database to add or remove the extension to/from.
    required: true
    type: str
    aliases:
    - login_db
  schema:
    description:
    - Name of the schema to add the extension to.
    type: str
  session_role:
    description:
    - Switch to session_role after connecting.
    - The specified session_role must be a role that the current login_user is a member of.
    - Permissions checking for SQL commands is carried out as though the session_role were the one that had logged in originally.
    type: str
  state:
    description:
    - The database extension state.
    default: present
    choices: [ absent, present ]
    type: str
  cascade:
    description:
    - Automatically install/remove any extensions that this extension depends on
      that are not already installed/removed (supported since PostgreSQL 9.6).
    type: bool
    default: false
  login_unix_socket:
    description:
      - Path to a Unix domain socket for local connections.
    type: str
  ssl_mode:
    description:
      - Determines whether or with what priority a secure SSL TCP/IP connection will be negotiated with the server.
      - See U(https://www.postgresql.org/docs/current/static/libpq-ssl.html) for more information on the modes.
      - Default of C(prefer) matches libpq default.
    type: str
    default: prefer
    choices: [ allow, disable, prefer, require, verify-ca, verify-full ]
  ca_cert:
    description:
      - Specifies the name of a file containing SSL certificate authority (CA) certificate(s).
      - If the file exists, the server's certificate will be verified to be signed by one of these authorities.
    type: str
    aliases: [ ssl_rootcert ]
  version:
    description:
      - Extension version to add or update to. Has effect with I(state=present) only.
      - If not specified and extension is not installed in the database,
        the latest version available will be created.
      - If extension is already installed, will update to the given version if a valid update
        path exists.
      - Downgrading is only supported if the extension provides a downgrade path otherwise
        the extension must be removed and a lower version of the extension must be made available.
      - Set I(version=latest) to always update the extension to the latest available version.
    type: str
  trust_input:
    description:
    - If C(false), check whether values of parameters I(ext), I(schema),
      I(version), I(session_role) are potentially dangerous.
    - It makes sense to use C(false) only when SQL injections via the parameters are possible.
    type: bool
    default: true
    version_added: '0.2.0'
seealso:
- name: PostgreSQL extensions
  description: General information about PostgreSQL extensions.
  link: https://www.postgresql.org/docs/current/external-extensions.html
- name: CREATE EXTENSION reference
  description: Complete reference of the CREATE EXTENSION command documentation.
  link: https://www.postgresql.org/docs/current/sql-createextension.html
- name: ALTER EXTENSION reference
  description: Complete reference of the ALTER EXTENSION command documentation.
  link: https://www.postgresql.org/docs/current/sql-alterextension.html
- name: DROP EXTENSION reference
  description: Complete reference of the DROP EXTENSION command documentation.
  link: https://www.postgresql.org/docs/current/sql-droppublication.html
notes:
- Supports C(check_mode).
- The default authentication assumes that you are either logging in as
  or sudo'ing to the C(postgres) account on the host.
- This module uses I(psycopg2), a Python PostgreSQL database adapter.
- You must ensure that C(psycopg2) is installed on the host before using this module.
- If the remote host is the PostgreSQL server (which is the default case),
  then PostgreSQL must also be installed on the remote host.
- For Ubuntu-based systems, install the C(postgresql), C(libpq-dev),
  and C(python-psycopg2) packages on the remote host before using this module.
- Incomparable versions, for example PostGIS ``unpackaged``, cannot be installed.
requirements: [ psycopg2 ]
author:
- Daniel Schep (@dschep)
- Thomas O'Donnell (@andytom)
- Sandro Santilli (@strk)
- Andrew Klychkov (@Andersson007)
- Keith Fiske (@keithf4)
extends_documentation_fragment:
- community.postgresql.postgres

'''

EXAMPLES = r'''
- name: Adds postgis extension to the database acme in the schema foo
  community.postgresql.postgresql_ext:
    name: postgis
    db: acme
    schema: foo

- name: Removes postgis extension to the database acme
  community.postgresql.postgresql_ext:
    name: postgis
    db: acme
    state: absent

- name: Adds earthdistance extension to the database template1 cascade
  community.postgresql.postgresql_ext:
    name: earthdistance
    db: template1
    cascade: true

# In the example below, if earthdistance extension is installed,
# it will be removed too because it depends on cube:
- name: Removes cube extension from the database acme cascade
  community.postgresql.postgresql_ext:
    name: cube
    db: acme
    cascade: true
    state: absent

- name: Create extension foo of version 1.2 or update it to that version if it's already created and a valid update path exists
  community.postgresql.postgresql_ext:
    db: acme
    name: foo
    version: 1.2

- name: Create the latest available version of extension foo. If already installed, update it to the latest version
  community.postgresql.postgresql_ext:
    db: acme
    name: foo
    version: latest
'''

RETURN = r'''
query:
  description: List of executed queries.
  returned: always
  type: list
  sample: ["DROP EXTENSION \"acme\""]

'''

import traceback

try:
    from psycopg2.extras import DictCursor
except ImportError:
    # psycopg2 is checked by connect_to_db()
    # from ansible.module_utils.postgres
    pass

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.postgresql.plugins.module_utils.database import (
    check_input,
)
from ansible_collections.community.postgresql.plugins.module_utils.postgres import (
    connect_to_db,
    ensure_required_libs,
    get_conn_params,
    postgres_common_argument_spec,
)
from ansible.module_utils._text import to_native

executed_queries = []


# ===========================================
# PostgreSQL module specific support methods.
#


def ext_delete(cursor, ext, current_version, cascade):
    """Remove the extension from the database.

    Return True if success.

    Args:
      cursor (cursor) -- cursor object of psycopg2 library
      ext (str) -- extension name
      current_version (str) -- installed version of the extension.
        Value obtained from ext_get_versions and used to
        determine if the extension was installed.
      cascade (boolean) -- Pass the CASCADE flag to the DROP commmand
    """
    if current_version:
        query = "DROP EXTENSION \"%s\"" % ext
        if cascade:
            query += " CASCADE"
        cursor.execute(query)
        executed_queries.append(cursor.mogrify(query))
        return True
    else:
        return False


def ext_update_version(cursor, ext, version):
    """Update extension version.

    Return True if success.

    Args:
      cursor (cursor) -- cursor object of psycopg2 library
      ext (str) -- extension name
      version (str) -- extension version
    """
    query = "ALTER EXTENSION \"%s\" UPDATE" % ext
    params = {}

    if version != 'latest':
        query += " TO %(ver)s"
        params['ver'] = version

    cursor.execute(query, params)
    executed_queries.append(cursor.mogrify(query, params))

    return True


def ext_create(cursor, ext, schema, cascade, version):
    """
    Create the extension objects inside the database.

    Return True if success.

    Args:
      cursor (cursor) -- cursor object of psycopg2 library
      ext (str) -- extension name
      schema (str) -- target schema for extension objects
      version (str) -- extension version
    """
    query = "CREATE EXTENSION \"%s\"" % ext
    params = {}

    if schema:
        query += " WITH SCHEMA \"%s\"" % schema
    if version != 'latest':
        query += " VERSION %(ver)s"
        params['ver'] = version
    if cascade:
        query += " CASCADE"

    cursor.execute(query, params)
    executed_queries.append(cursor.mogrify(query, params))
    return True


def ext_get_versions(cursor, ext):
    """
    Get the currently created extension version if it is installed
    in the database and versions that are available if it is
    installed on the system.

    Return tuple (current_version, [list of available versions]).

    Note: the list of available versions contains only versions
          that higher than the current created version.
          If the extension is not created, this list will contain all
          available versions.

    Args:
      cursor (cursor) -- cursor object of psycopg2 library
      ext (str) -- extension name
    """

    current_version = None
    params = {}
    params['ext'] = ext

    # 1. Get the current extension version:
    query = ("SELECT extversion FROM pg_catalog.pg_extension "
             "WHERE extname = %(ext)s")

    cursor.execute(query, params)

    res = cursor.fetchone()
    if res:
        current_version = res[0]

    # 2. Get available versions:
    query = ("SELECT version FROM pg_available_extension_versions "
             "WHERE name = %(ext)s")

    cursor.execute(query, params)

    available_versions = set(r[0] for r in cursor.fetchall())

    if current_version is None:
        current_version = False

    return (current_version, available_versions)


def ext_valid_update_path(cursor, ext, current_version, version):
    """
    Check to see if the installed extension version has a valid update
    path to the given version. A version of 'latest' is always a valid path.

    Return True if a valid path exists. Otherwise return False.

    Args:
      cursor (cursor) -- cursor object of psycopg2 library
      ext (str) -- extension name
      current_version (str) -- installed version of the extension.
      version (str) -- target extension version to update to.
        A value of 'latest' is always a valid path and will result
        in the extension update command always being run.
    """

    valid_path = False
    params = {}
    if version != 'latest':
        query = ("SELECT path FROM pg_extension_update_paths(%(ext)s) "
                 "WHERE source = %(cv)s "
                 "AND target = %(ver)s")

        params['ext'] = ext
        params['cv'] = current_version
        params['ver'] = version

        cursor.execute(query, params)
        res = cursor.fetchone()
        if res is not None:
            valid_path = True
    else:
        valid_path = True

    return (valid_path)


# ===========================================
# Module execution.
#


def main():
    argument_spec = postgres_common_argument_spec()
    argument_spec.update(
        db=dict(type="str", required=True, aliases=["login_db"]),
        ext=dict(type="str", required=True, aliases=["name"]),
        schema=dict(type="str"),
        state=dict(type="str", default="present", choices=["absent", "present"]),
        cascade=dict(type="bool", default=False),
        session_role=dict(type="str"),
        version=dict(type="str"),
        trust_input=dict(type="bool", default=True),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    ext = module.params["ext"]
    schema = module.params["schema"]
    state = module.params["state"]
    cascade = module.params["cascade"]
    version = module.params["version"]
    session_role = module.params["session_role"]
    trust_input = module.params["trust_input"]
    changed = False

    if not trust_input:
        check_input(module, ext, schema, version, session_role)

    if version and state == 'absent':
        module.warn("Parameter version is ignored when state=absent")

    # Ensure psycopg2 libraries are available before connecting to DB:
    ensure_required_libs(module)
    conn_params = get_conn_params(module, module.params)
    db_connection, dummy = connect_to_db(module, conn_params, autocommit=True)
    cursor = db_connection.cursor(cursor_factory=DictCursor)

    try:
        # Get extension info and available versions:
        curr_version, available_versions = ext_get_versions(cursor, ext)

        if state == "present":

            # If version passed
            if version:
                # If extension is installed, update to passed version if a valid path exists
                if curr_version:
                    # Given version already installed
                    if curr_version == version:
                        changed = False
                    # Attempt to update to given version or latest version defined in extension control file
                    # ALTER EXTENSION is actually run if valid, so 'changed' will be true even if nothing updated
                    else:
                        valid_update_path = ext_valid_update_path(cursor, ext, curr_version, version)
                        if valid_update_path:
                            if module.check_mode:
                                changed = True
                            else:
                                changed = ext_update_version(cursor, ext, version)
                        else:
                            module.fail_json(msg="Passed version '%s' has no valid update path from "
                                                 "the currently installed version '%s' or "
                                                 "the passed version is not available" % (version, curr_version))
                else:
                    # If not requesting latest version and passed version not available
                    if version != 'latest' and version not in available_versions:
                        module.fail_json(msg="Passed version '%s' is not available" % version)
                    # Else install the passed version when available
                    else:
                        if module.check_mode:
                            changed = True
                        else:
                            changed = ext_create(cursor, ext, schema, cascade, version)

            # If version is not passed:
            else:
                # Extension exists, no request to update so no change
                if curr_version:
                    changed = False
                else:
                    # If the ext doesn't exist and is available:
                    if available_versions:
                        if module.check_mode:
                            changed = True
                        else:
                            changed = ext_create(cursor, ext, schema, cascade, 'latest')

                    # If the ext doesn't exist and is not available:
                    else:
                        module.fail_json(msg="Extension %s is not available" % ext)

        elif state == "absent":
            if curr_version:
                if module.check_mode:
                    changed = True
                else:
                    changed = ext_delete(cursor, ext, curr_version, cascade)
            else:
                changed = False

    except Exception as e:
        db_connection.close()
        module.fail_json(msg="Management of PostgreSQL extension failed: %s" % to_native(e), exception=traceback.format_exc())

    db_connection.close()
    module.exit_json(changed=changed, db=module.params["db"], ext=ext, queries=executed_queries)


if __name__ == '__main__':
    main()
