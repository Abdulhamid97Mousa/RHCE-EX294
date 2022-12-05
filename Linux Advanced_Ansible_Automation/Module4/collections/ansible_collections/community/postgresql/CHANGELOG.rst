=============================================
Community PostgreSQL Collection Release Notes
=============================================

.. contents:: Topics


v2.3.1
======

Release Summary
---------------

This is the bugfix release of the ``community.postgresql`` collection.
This changelog contains all changes to the modules in this collection that
have been added after release 2.3.0.

Bugfixes
--------

- postgresql_privs - fails with ``type=default_privs``, ``privs=ALL``, ``objs=ALL_DEFAULT`` (https://github.com/ansible-collections/community.postgresql/issues/373).

v2.3.0
======

Release Summary
---------------

This is the minor release of the ``community.postgresql`` collection.
This changelog contains all changes to the modules in this collection that
have been added after the release of ``community.postgresql`` 2.2.0.

Minor Changes
-------------

- postgresql_* - add the ``connect_params`` parameter dict to allow any additional ``libpg`` connection parameters (https://github.com/ansible-collections/community.postgresql/pull/329).

Bugfixes
--------

- postgresql_info - make arguments passed to SHOW command properly quoted to prevent the interpreter evaluating them (https://github.com/ansible-collections/community.postgresql/issues/314).
- postgresql_pg_hba - support the connection types ``hostgssenc`` and ``hostnogssenc`` (https://github.com/ansible-collections/community.postgresql/pull/351).
- postgresql_privs - add support for alter default privileges grant usage on schemas (https://github.com/ansible-collections/community.postgresql/issues/332).
- postgresql_privs - cannot grant select on objects in all schemas; add the ``not-specified`` value to the ``schema`` parameter to make this possible (https://github.com/ansible-collections/community.postgresql/issues/332).
- postgresql_set - avoid postgres puts extra quotes when passing values containing commas (https://github.com/ansible-collections/community.postgresql/issues/78).
- postgresql_user - make the module idempotent when password is scram hashed (https://github.com/ansible-collections/community.postgresql/issues/301).

v2.2.0
======

Release Summary
---------------

This is the minor release of the ``community.postgresql`` collection.
This changelog contains all changes to the modules in this collection that
have been added after the release of ``community.postgresql`` 2.1.5.

Major Changes
-------------

- postgresql_user - the ``groups`` argument has been deprecated and will be removed in ``community.postgresql 3.0.0``. Please use the ``postgresql_membership`` module to specify group/role memberships instead (https://github.com/ansible-collections/community.postgresql/issues/277).

Minor Changes
-------------

- postgresql_membership - add the ``exact`` state value to be able to specify a list of only groups a user must be a member of (https://github.com/ansible-collections/community.postgresql/issues/277).
- postgresql_pg_hba - add argument ``overwrite`` (bool, default: false) to remove unmanaged rules (https://github.com/ansible-collections/community.postgresql/issues/297).
- postgresql_pg_hba - add argument ``rules_behavior`` (choices: conflict (default), combine) to fail when ``rules`` and normal rule-specific arguments are given or, when ``combine``, use them as defaults for the ``rules`` items (https://github.com/ansible-collections/community.postgresql/issues/297).
- postgresql_pg_hba - add argument ``rules`` to specify a list of rules using the normal rule-specific argument in each item (https://github.com/ansible-collections/community.postgresql/issues/297).

Bugfixes
--------

- Include ``simplified_bsd.txt`` license file for various module utils.
- postgresql_info - fix pg version parsing (https://github.com/ansible-collections/community.postgresql/issues/315).
- postgresql_ping - fix pg version parsing (https://github.com/ansible-collections/community.postgresql/issues/315).
- postgresql_privs.py - add functionality when the PostgreSQL version is 9.0.0 or greater to incorporate ``ALL x IN SCHEMA`` syntax (https://github.com/ansible-collections/community.postgresql/pull/282). Please see the official documentation for details regarding grants (https://www.postgresql.org/docs/9.0/sql-grant.html).
- postgresql_subscription - fix idempotence by casting the ``connparams`` dict variable (https://github.com/ansible-collections/community.postgresql/issues/280).
- postgresql_user - add ``alter user``-statements in the return value ``queries`` (https://github.com/ansible-collections/community.postgresql/issues/307).

v2.1.5
======

Release Summary
---------------

This is the bugfix release of the ``community.postgresql`` collection.
This changelog contains all changes to the modules in this collection that
have been added after the release of ``community.postgresql`` 2.1.4

Bugfixes
--------

- Include ``PSF-license.txt`` file for ``plugins/module_utils/_version.py``.
- collection core functions - fix attribute error `nonetype` by always calling `ensure_required_libs` (https://github.com/ansible-collections/community.postgresql/issues/252).

v2.1.4
======

Release Summary
---------------

This is the minor release of the ``community.postgresql`` collection.
This changelog contains all changes to the modules in this collection that
have been added after the release of ``community.postgresql`` 2.1.3.

Major Changes
-------------

- The community.postgresql collection no longer supports ``Ansible 2.9`` and ``ansible-base 2.10``. While we take no active measures to prevent usage and there are no plans to introduce incompatible code to the modules, we will stop testing against ``Ansible 2.9`` and ``ansible-base 2.10``. Both will very soon be End of Life and if you are still using them, you should consider upgrading to the ``latest Ansible / ansible-core 2.11 or later`` as soon as possible (https://github.com/ansible-collections/community.postgresql/pull/245).

v2.1.3
======

Release Summary
---------------

This is the minor release of the ``community.postgresql`` collection.
This changelog contains all changes to the modules in this collection that
have been added after the release of ``community.postgresql`` 2.1.2.

Major Changes
-------------

- postgresql_user - the ``priv`` argument has been deprecated and will be removed in ``community.postgresql 3.0.0``. Please use the ``postgresql_privs`` module to grant/revoke privileges instead (https://github.com/ansible-collections/community.postgresql/issues/212).

Bugfixes
--------

- postgresql_db - get rid of the deprecated psycopg2 connection alias ``database`` in favor of ``dbname`` when psycopg2 is 2.7+ is used (https://github.com/ansible-collections/community.postgresql/issues/194, https://github.com/ansible-collections/community.postgresql/pull/196).

v2.1.2
======

Release Summary
---------------

This is the patch release of the `community.postgresql` collection. This changelog contains all changes to the modules in this collection that have been added after the release of `community.postgresql` 2.1.1.

Major Changes
-------------

- postgresql_privs - the ``usage_on_types`` feature have been deprecated and will be removed in ``community.postgresql 3.0.0``. Please use the ``type`` option with the ``type`` value to explicitly grant/revoke privileges on types (https://github.com/ansible-collections/community.postgresql/issues/207).

v2.1.1
======

Release Summary
---------------

This is the bugfix release of the community.postgresql collection.
This changelog contains all changes to the modules in this collection that have been added after the release of community.postgresql 2.1.0.

Bugfixes
--------

- module core functions - get rid of the deprecated psycopg2 connection alias ``database`` in favor of ``dbname`` when psycopg2 is 2.7+ (https://github.com/ansible-collections/community.postgresql/pull/196).
- postgresql_query - cannot handle .sql file with \\n at end of file (https://github.com/ansible-collections/community.postgresql/issues/180).

v2.1.0
======

Release Summary
---------------

This is the minor release of the ``community.postgresql`` collection.
This changelog contains all changes to the modules in this collection that
have been added after the release of ``community.postgresql`` 2.0.0.

Major Changes
-------------

- postgresql_query - the ``path_to_script`` and ``as_single_query`` options as well as the ``query_list`` and ``query_all_results`` return values have been deprecated and will be removed in ``community.postgresql 3.0.0``. Please use the ``community.postgresql.postgresql_script`` module to execute statements from scripts (https://github.com/ansible-collections/community.postgresql/issues/189).

New Modules
-----------

- postgresql_script - Run PostgreSQL statements from a file

v2.0.0
======

Release Summary
---------------

This is the major release of the ``community.postgresql`` collection.
This changelog contains all changes to the modules in this collection that
have been added after the release of ``community.postgresql`` 1.7.0.

Major Changes
-------------

- postgresql_query - the default value of the ``as_single_query`` option changes to ``yes``. If the related behavior of your tasks where the module is involved changes, please adjust the parameter's value correspondingly (https://github.com/ansible-collections/community.postgresql/issues/85).

v1.6.1
======

Release Summary
---------------

This is the bugfix release of the ``community.postgresql`` collection.
This changelog contains all changes to the modules in this collection that
have been added after the release of ``community.postgresql`` 1.6.1.

Bugfixes
--------

- Collection core functions - use vendored version of ``distutils.version`` instead of the deprecated Python standard library ``distutils`` (https://github.com/ansible-collections/community.postgresql/pull/179).
- postgres_info - It now works on AWS RDS Postgres.
- postgres_info - Specific info (namespaces, extensions, languages) of each database was not being shown properly. Instead, the info from the DB that was connected was always being shown (https://github.com/ansible-collections/community.postgresql/issues/172).

v1.6.0
======

Release Summary
---------------

This is the minor release of the ``community.postgresql`` collection.
This changelog contains all changes to the modules in this collection that
have been added after the release of ``community.postgresql`` 1.5.0.

Bugfixes
--------

- postgresql_ext - Handle postgresql extension updates through path validation instead of version comparison (https://github.com/ansible-collections/community.postgresql/issues/129).

v1.5.0
======

Release Summary
---------------

This is the minor release of the ``community.postgresql`` collection.
This changelog contains all changes to the modules in this collection that
have been added after the release of ``community.postgresql`` 1.4.0.

Minor Changes
-------------

- postgresql_db - Add the ``force`` boolean option to drop active connections first and then remove the database (https://github.com/ansible-collections/community.postgresql/issues/109).
- postgresql_info - Add the ``raw`` return value for extension version (https://github.com/ansible-collections/community.postgresql/pull/138).
- postgresql_pg_hba - Add the parameters ``keep_comments_at_rules`` and ``comment`` (https://github.com/ansible-collections/community.postgresql/issues/134).

Bugfixes
--------

- postgresql_ext - Fix extension version handling when it has 0 value (https://github.com/ansible-collections/community.postgresql/issues/136).
- postgresql_info - Fix extension version handling when it has 0 value (https://github.com/ansible-collections/community.postgresql/issues/137).
- postgresql_set - Fix wrong numerical value conversion (https://github.com/ansible-collections/community.postgresql/issues/110).
- postgresql_slot - Correct the server_version check for PG 9.6 (https://github.com/ansible-collections/community.postgresql/issue/120)

v1.4.0
======

Release Summary
---------------

This is the minor release of the ``community.postgresql`` collection.
This changelog contains all changes to the modules in this collection that
have been added after the release of ``community.postgresql`` 1.3.0.

Minor Changes
-------------

- postgresql_db - add support for the ``directory`` format when the ``state`` option is ``dump`` or ``restore`` (https://github.com/ansible-collections/community.postgresql/pull/108).
- postgresql_db - add the ``rename`` value to the ``state`` option (https://github.com/ansible-collections/community.postgresql/pull/107).

v1.3.0
======

Release Summary
---------------

This is the minor release of the ``community.postgresql`` collection.
This changelog contains all changes to the modules in this collection that
have been added after the release of ``community.postgresql`` 1.2.0.

Major Changes
-------------

- postgresql_query - the default value of the ``as_single_query`` option will be changed to ``yes`` in community.postgresql 2.0.0 (https://github.com/ansible-collections/community.postgresql/issues/85).

Bugfixes
--------

- postgresql_privs - fix ``fail_on_role`` check (https://github.com/ansible-collections/community.postgresql/pull/82).

v1.2.0
======

Release Summary
---------------

This is the minor release of the ``community.postgresql`` collection.
This changelog contains all changes to the modules in this collection that
have been added after the release of ``community.postgresql`` 1.1.1.

Minor Changes
-------------

- postgresql_info - add the ``patch``, ``full``, and ``raw`` values of the ``version`` return value (https://github.com/ansible-collections/community.postgresql/pull/68).
- postgresql_ping - add the ``patch``, ``full``, and ``raw`` values of the ``server_version`` return value (https://github.com/ansible-collections/community.postgresql/pull/70).

v1.1.1
======

Release Summary
---------------

This is the patch release of the ``community.postgresql`` collection.
This changelog contains all changes to the modules in this collection that
have been added after the release of ``community.postgresql`` 1.1.0.

Bugfixes
--------

- postgresql_query - add a warning to set ``as_single_query`` option explicitly (https://github.com/ansible-collections/community.postgresql/pull/54).
- postgresql_query - fix datetime.timedelta type handling (https://github.com/ansible-collections/community.postgresql/issues/47).
- postgresql_query - fix decimal handling (https://github.com/ansible-collections/community.postgresql/issues/45).
- postgresql_set - fails in check_mode on non-numeric values containing `B` (https://github.com/ansible-collections/community.postgresql/issues/48).

v1.1.0
======

Release Summary
---------------

This is the minor release of the ``community.postgresql`` collection.
This changelog contains all changes to the modules in this collection that
have been added after the release of ``community.postgresql`` 1.0.0.

Minor Changes
-------------

- postgresql_query - add ``as_single_query`` option to execute a script content as a single query to avoid semicolon related errors (https://github.com/ansible-collections/community.postgresql/pull/37).

Bugfixes
--------

- postgresql_info - fix crash caused by wrong PgSQL version parsing (https://github.com/ansible-collections/community.postgresql/issues/40).
- postgresql_ping - fix crash caused by wrong PgSQL version parsing (https://github.com/ansible-collections/community.postgresql/issues/40).
- postgresql_set - return a message instead of traceback when a passed parameter has not been found (https://github.com/ansible-collections/community.postgresql/issues/41).

v1.0.0
======

Release Summary
---------------

This is the first proper release of the ``community.postgresql`` collection which is needed to include the collection in Ansible.
This changelog does not contain any changes because there are no changes made since release 0.1.0.


v0.1.0
======

Release Summary
---------------

The ``community.postgresql`` continues the work on the Ansible PostgreSQL
modules from their state in ``community.general`` 1.2.0.
The changes listed here are thus relative to the modules ``community.general.postgresql_*``.


Minor Changes
-------------

- postgresql_info - add ``in_recovery`` return value to show if a service in recovery mode or not (https://github.com/ansible-collections/community.general/issues/1068).
- postgresql_privs - add ``procedure`` type support (https://github.com/ansible-collections/community.general/issues/1002).
- postgresql_query - add ``query_list`` and ``query_all_results`` return values (https://github.com/ansible-collections/community.general/issues/838).

Bugfixes
--------

- postgresql_ext - fix the module crashes when available ext versions cannot be compared with current version (https://github.com/ansible-collections/community.general/issues/1095).
- postgresql_ext - fix version selection when ``version=latest`` (https://github.com/ansible-collections/community.general/pull/1078).
- postgresql_privs - fix module fails when ``type`` group and passing ``objs`` value containing hyphens (https://github.com/ansible-collections/community.general/issues/1058).
