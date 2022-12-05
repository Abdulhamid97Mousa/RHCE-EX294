# PostgreSQL collection for Ansible
| | | | |
|--|--|--|--|
|[![Build Status](https://dev.azure.com/ansible/community.postgres/_apis/build/status/CI?branchName=main)](https://dev.azure.com/ansible/community.postgres/_build?definitionId=28)|[![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/community.postgresql)](https://codecov.io/gh/ansible-collections/community.postgresql)| |![](https://img.shields.io/matrix/postgresql:ansible.com.svg?server_fqdn=ansible-accounts.ems.host&label=Discuss%20at%20%23postgresql:ansible.com&logo=matrix)|

This collection is a part of the Ansible package.

## Code of Conduct

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior violating the [Ansible Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html), please refer to the [policy violations](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html#policy-violations) section of the Code of Conduct for information on how to raise a complaint.

## Contributing to this collection

The content of this collection is made by [people](https://github.com/ansible-collections/community.postgresql/blob/main/CONTRIBUTORS) just like you, a community of individuals collaborating on making the world better through developing automation software.

We are actively accepting new contributors.

All types of contributions are very welcome.

You don't know how to start? Refer to our [contribution guide](https://github.com/ansible-collections/community.postgresql/blob/main/CONTRIBUTING.md)!

We use the following guidelines:

* [CONTRIBUTING.md](https://github.com/ansible-collections/community.postgresql/blob/main/CONTRIBUTING.md)
* [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html)
* [Ansible Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
* [Ansible Collection Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections)

## Collection maintenance

The current maintainers (contributors with `write` or higher access) are listed in the [MAINTAINERS](https://github.com/ansible-collections/community.postgresql/blob/main/MAINTAINERS) file. If you have questions or need help, feel free to mention them in the proposals.

To learn how to maintain / become a maintainer of this collection, refer to the [Maintainer guidelines](https://github.com/ansible-collections/community.postgresql/blob/main/MAINTAINING.md).

It is necessary for maintainers of this collection to be subscribed to:

* The collection itself (the `Watch` button -> `All Activity` in the upper right corner of the repository's homepage).
* The "Changes Impacting Collection Contributors and Maintainers" [issue](https://github.com/ansible-collections/overview/issues/45).

They also should be subscribed to Ansible's [The Bullhorn newsletter](https://docs.ansible.com/ansible/devel/community/communication.html#the-bullhorn).

## Communication

We announce important development changes and releases through Ansible's [The Bullhorn newsletter](https://docs.ansible.com/ansible/devel/community/communication.html#the-bullhorn). If you are a collection developer, be sure you are subscribed.

Join us on Matrix in:

* `#postgresql:ansible.com` [room](https://matrix.to/#/#postgresql:ansible.com): questions on how to contribute and use this collection.
* `#users:ansible.com` [room](https://matrix.to/#/#users:ansible.com): general use questions and support.
* `#ansible-community:ansible.com` [room](https://matrix.to/#/#community:ansible.com): community and collection development questions.
* other Matrix rooms or corresponding bridged Libera.Chat channels. See the [Ansible Communication Guide](https://docs.ansible.com/ansible/devel/community/communication.html) for details.

We take part in the global quarterly [Ansible Contributor Summit](https://github.com/ansible/community/wiki/Contributor-Summit) virtually or in-person. Track [The Bullhorn newsletter](https://docs.ansible.com/ansible/devel/community/communication.html#the-bullhorn) and join us.

For more information about communication, refer to the [Ansible Communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).

## Governance

We, [the PostgreSQL working group](https://github.com/ansible-collections/community.postgresql/wiki/PostgreSQL-Working-Group), use [the community pinboard](https://github.com/ansible-collections/community.postgresql/issues/30) for general announcements and discussions.

The process of decision making in this collection is based on discussing and finding consensus among participants.

Every voice is important and every idea is valuable. If you have something on your mind, create an issue or dedicated discussion and let's discuss it!

## External requirements

The PostgreSQL modules rely on the [Psycopg2](https://www.psycopg.org/docs/) PostgreSQL database adapter.

## Tested with ansible-core

Tested with the following `ansible-core` releases:
- 2.12
- 2.13
- 2.14
- current development version

Ansible-core versions before 2.12.0 are not supported.
Our AZP CI includes testing with the following docker images / PostgreSQL versions:

- CentOS 7: 9.2
- RHEL 8.3 / 8.4: 10
- Fedora 34: 13
- Ubuntu 20.04: 14

## Included content

- **Info modules**:
  - [postgresql_info](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_info_module.html)
  - [postgresql_ping](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_ping_module.html)
  - [postgresql_user_obj_stat_info](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_user_obj_stat_info_module.html)

- **Basic modules**:
  - [postgresql_db](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_db_module.html)
  - [postgresql_ext](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_ext_module.html)
  - [postgresql_lang](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_lang_module.html)
  - [postgresql_pg_hba](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_pg_hba_module.html)
  - [postgresql_privs](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_privs_module.html)
  - [postgresql_set](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_set_module.html)
  - [postgresql_schema](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_schema_module.html)
  - [postgresql_tablespace](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_tablespace_module.html)
  - [postgresql_query](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_query_module.html)
  - [postgresql_user](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_user_module.html)

- **Other modules**:
  - [postgresql_copy](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_copy_module.html)
  - [postgresql_idx](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_idx_module.html)
  - [postgresql_membership](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_membership_module.html)
  - [postgresql_owner](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_owner_module.html)
  - [postgresql_publication](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_publication_module.html)
  - [postgresql_sequence](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_sequence_module.html)
  - [postgresql_slot](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_slot_module.html)
  - [postgresql_subscription](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_subscription_module.html)
  - [postgresql_table](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_table_module.html)

## Using this collection

### Installing the Collection from Ansible Galaxy

Before using the PostgreSQL collection, you need to install it with the Ansible Galaxy command-line tool:

```bash
ansible-galaxy collection install community.postgresql
```

You can include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: community.postgresql
```

You can also download the tarball from [Ansible Galaxy](https://galaxy.ansible.com/community/postgresql) and install the collection manually wherever you need.

Note that if you install the collection from Ansible Galaxy with the command-line tool or tarball, it will not be upgraded automatically when you upgrade the Ansible package. To upgrade the collection to the latest available version, run the following command:

```bash
ansible-galaxy collection install community.postgresql --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax:

```bash
ansible-galaxy collection install community.postgresql:==X.Y.Z
```

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Release notes

See the [changelog](https://github.com/ansible-collections/community.postgresql/blob/main/CHANGELOG.rst).

## Roadmap

See the [release plan](https://github.com/ansible-collections/community.postgresql/issues/13).

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
