========================================
Community MySQL Collection Release Notes
========================================

.. contents:: Topics

This changelog describes changes after version 2.0.0.

v3.5.1
======

Release Summary
---------------

This is the patch release of the ``community.mysql`` collection.
This changelog contains all changes to the modules and plugins in this collection
that have been made after the previous release.

Bugfixes
--------

- mysql_user, mysql_role - mysql/mariadb recent versions translate 'ALL PRIVILEGES' to a list of specific privileges. That caused a change every time we modified user privileges. This fix compares privs before and after user modification to avoid this infinite change (https://github.com/ansible-collections/community.mysql/issues/77).

v3.5.0
======

Release Summary
---------------

This is the minor release of the ``community.mysql`` collection.
This changelog contains all changes to the modules in this collection
that have been added after the release of ``community.mysql`` 3.4.0.

Minor Changes
-------------

- mysql_replication - add a new option: ``primary_ssl_verify_server_cert`` (https://github.com//pull/435).

Bugfixes
--------

- mysql_user - grant option was revoked accidentally when modifying users. This fix revokes grant option only when privs are setup to do that (https://github.com/ansible-collections/community.mysql/issues/77#issuecomment-1209693807).

v3.4.0
======

Release Summary
---------------

This is the minor release of the ``community.mysql`` collection.
This changelog contains all changes to the modules in this collection
that have been added after the release of ``community.mysql`` 3.3.0.

Major Changes
-------------

- mysql_db - the ``pipefail`` argument's default value will be changed to ``true`` in community.mysql 4.0.0. If your target machines do not use ``bash`` as a default interpreter, set ``pipefail`` to ``false`` explicitly. However, we strongly recommend setting up ``bash`` as a default and ``pipefail=true`` as it will protect you from getting broken dumps you don't know about (https://github.com/ansible-collections/community.mysql/issues/407).

Minor Changes
-------------

- mysql_db - add the ``chdir`` argument to avoid failings when a dump file contains relative paths (https://github.com/ansible-collections/community.mysql/issues/395).
- mysql_db - add the ``pipefail`` argument to avoid broken dumps when ``state`` is ``dump`` and compression is used (https://github.com/ansible-collections/community.mysql/issues/256).

Bugfixes
--------

- Include ``simplified_bsd.txt`` license file for various module utils.
- mysql_db - Using compression masks errors messages from mysql_dump. By default the fix is inactive to ensure retro-compatibility with system without bash. To activate the fix, use the module option ``pipefail=true`` (https://github.com/ansible-collections/community.mysql/issues/256).
- mysql_replication - when the ``primary_ssl`` argument is set to ``no``, the module will turn off SSL (https://github.com/ansible-collections/community.mysql/issues/393).

v3.3.0
======

Release Summary
---------------

This is the minor release of the ``community.mysql`` collection.
This changelog contains all changes to the modules in this collection
that have been added after the release of ``community.mysql`` 3.2.1.

Minor Changes
-------------

- mysql_role - add the argument ``members_must_exist`` (boolean, default true). The assertion that the users supplied in the ``members`` argument exist is only executed when the new argument ``members_must_exist`` is ``true``, to allow opt-out (https://github.com/ansible-collections/community.mysql/pull/369).
- mysql_user - Add the option ``on_new_username`` to argument ``update_password`` to reuse the password (plugin and authentication_string) when creating a new user if some user with the same name already exists. If the existing user with the same name have varying passwords, the password from the arguments is used like with ``update_password: always`` (https://github.com/ansible-collections/community.mysql/pull/365).
- mysql_user - Add the result field ``password_changed`` (boolean). It is true, when the user got a new password. When the user was created with ``update_password: on_new_username`` and an existing password was reused, ``password_changed`` is false (https://github.com/ansible-collections/community.mysql/pull/365).

Bugfixes
--------

- mysql_query - fix false change reports when ``IF EXISTS/IF NOT EXISTS`` clause is used (https://github.com/ansible-collections/community.mysql/issues/268).
- mysql_role - don't add members to a role when creating the role and ``detach_members: true`` is set (https://github.com/ansible-collections/community.mysql/pull/367).
- mysql_role - in some cases (when "SHOW GRANTS" did not use backticks for quotes), no unwanted members were detached from the role (and redundant "GRANT" statements were executed for wanted members). This is fixed by querying the existing role members from the mysql.role_edges (MySQL) or mysql.roles_mapping (MariaDB) tables instead of parsing the "SHOW GRANTS" output (https://github.com/ansible-collections/community.mysql/pull/368).
- mysql_user - fix logic when ``update_password`` is set to ``on_create`` for users using ``plugin*`` arguments (https://github.com/ansible-collections/community.mysql/issues/334). The ``on_create`` sets ``password`` to None for old mysql_native_authentication but not for authentiation methods which uses the ``plugin*`` arguments. This PR changes this so ``on_create`` also exchange ``plugin``, ``plugin_hash_string``, ``plugin_auth_string`` to None in the list of arguments to change

v3.2.1
======

Release Summary
---------------

This is the patch release of the ``community.mysql`` collection.
This changelog contains all changes to the modules in this collection
that have been added after the release of ``community.mysql`` 3.2.0.

Bugfixes
--------

- Include ``PSF-license.txt`` file for ``plugins/module_utils/_version.py``.

v3.2.0
======

Release Summary
---------------

This is the minor release of the ``community.mysql`` collection.
This changelog contains all changes to the modules in this collection
that have been added after the release of ``community.mysql`` 3.1.3.

Major Changes
-------------

- The community.mysql collection no longer supports ``Ansible 2.9`` and ``ansible-base 2.10``. While we take no active measures to prevent usage and there are no plans to introduce incompatible code to the modules, we will stop testing against ``Ansible 2.9`` and ``ansible-base 2.10``. Both will very soon be End of Life and if you are still using them, you should consider upgrading to the ``latest Ansible / ansible-core 2.11 or later`` as soon as possible (https://github.com/ansible-collections/community.mysql/pull/343).

Minor Changes
-------------

- mysql_user and mysql_role: Add the argument ``subtract_privs`` (boolean, default false, mutually exclusive with ``append_privs``). If set, the privileges given in ``priv`` are revoked and existing privileges are kept (https://github.com/ansible-collections/community.mysql/pull/333).

Bugfixes
--------

- mysql_user - fix missing dynamic privileges after revoke and grant privileges to user (https://github.com/ansible-collections/community.mysql/issues/120).
- mysql_user - fix parsing privs when a user has roles assigned (https://github.com/ansible-collections/community.mysql/issues/231).

v3.1.3
======

Release Summary
---------------

This is the patch release of the ``community.mysql`` collection.
This changelog contains all changes to the modules in this collection
that have been added after the release of ``community.mysql`` 3.1.2.

Bugfixes
--------

- mysql_replication - fails when using the `primary_use_gtid` option with `slave_pos` or `replica_pos` (https://github.com/ansible-collections/community.mysql/issues/335).
- mysql_role - remove redundant connection closing (https://github.com/ansible-collections/community.mysql/pull/330).
- mysql_user - fix the possibility for a race condition that breaks certain (circular) replication configurations when ``DROP USER`` is executed on multiple nodes in the replica set. Adding ``IF EXISTS`` avoids the need to use ``sql_log_bin: no`` making the statement always replication safe (https://github.com/ansible-collections/community.mysql/pull/287).

v3.1.2
======

Release Summary
---------------

This is the patch release of the ``community.mysql`` collection.
This changelog contains all changes to the modules in this collection
that have been added after the release of ``community.mysql`` 3.1.1.

Bugfixes
--------

- Collection core functions - fixes related to the mysqlclient Python connector (https://github.com/ansible-collections/community.mysql/issues/292).

v3.1.1
======

Release Summary
---------------

This is the patch release of the ``community.mysql`` collection.
This changelog contains all changes to the modules in this collection
that have been added after the release of ``community.mysql`` 3.1.0.

Bugfixes
--------

- mysql_role - make the ``set_default_role_all`` parameter actually working (https://github.com/ansible-collections/community.mysql/pull/282).

v3.1.0
======

Release Summary
---------------

This is the minor release of the ``community.mysql`` collection.
This changelog contains all changes to the modules in this collection
that have been added after the release of ``community.mysql`` 3.0.0.

Minor Changes
-------------

- Added explicit description of the supported versions of databases and connectors. Changes to the collection are **NOT** tested against database versions older than `mysql 5.7.31` and `mariadb 10.2.37` or connector versions older than `pymysql 0.7.10` and `mysqlclient 2.0.1`. (https://github.com/ansible-collections/community.mysql/discussions/141)
- mysql_user - added the ``force_context`` boolean option to set the default database context for the queries to be the ``mysql`` database. This way replication/binlog filters can catch the statements (https://github.com/ansible-collections/community.mysql/issues/265).

Bugfixes
--------

- Collection core functions - use vendored version of ``distutils.version`` instead of the deprecated Python standard library ``distutils`` (https://github.com/ansible-collections/community.mysql/pull/269).

v3.0.0
======

Release Summary
---------------

This is the major release of the ``community.mysql`` collection.
This changelog contains all breaking changes to the modules in this collection
that have been added after the release of ``community.mysql`` 2.3.2.

Breaking Changes / Porting Guide
--------------------------------

- mysql_replication - remove ``Is_Slave`` and ``Is_Master`` return values (were replaced with ``Is_Primary`` and ``Is_Replica`` (https://github.com/ansible-collections    /community.mysql/issues/145).
- mysql_replication - remove the mode options values containing ``master``/``slave`` and the master_use_gtid option ``slave_pos`` (were replaced with corresponding ``primary``/``replica`` values) (https://github.com/ansible-collections/community.mysql/issues/145).
- mysql_user - remove support for the `REQUIRESSL` special privilege as it has ben superseded by the `tls_requires` option (https://github.com/ansible-collections/community.mysql/discussions/121).
- mysql_user - validate privileges using database engine directly (https://github.com/ansible-collections/community.mysql/issues/234 https://github.com/ansible-collections/community.mysql/pull/243). Do not validate privileges in this module anymore.
