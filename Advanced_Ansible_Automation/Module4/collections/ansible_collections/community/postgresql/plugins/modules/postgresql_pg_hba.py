#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Sebastiaan Mannem (@sebasmannem) <sebastiaan.mannem@enterprisedb.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

'''
This module is used to manage postgres pg_hba files with Ansible.
'''

__metaclass__ = type

DOCUMENTATION = r'''
---
module: postgresql_pg_hba
short_description: Add, remove or modify a rule in a pg_hba file
description:
   - The fundamental function of the module is to create, or delete lines in pg_hba files.
   - The lines in the file should be in a typical pg_hba form and lines should be unique per key (type, databases, users, source).
     If they are not unique and the SID is 'the one to change', only one for I(state=present) or
     none for I(state=absent) of the SID's will remain.
extends_documentation_fragment: files
options:
  address:
    description:
      - The source address/net where the connections could come from.
      - Will not be used for entries of I(type)=C(local).
      - You can also use keywords C(all), C(samehost), and C(samenet).
    default: samehost
    type: str
    aliases: [ source, src ]
  backup:
    description:
      - If set, create a backup of the C(pg_hba) file before it is modified.
        The location of the backup is returned in the (backup) variable by this module.
    default: false
    type: bool
  backup_file:
    description:
      - Write backup to a specific backupfile rather than a temp file.
    type: str
  create:
    description:
      - Create an C(pg_hba) file if none exists.
      - When set to false, an error is raised when the C(pg_hba) file doesn't exist.
    default: false
    type: bool
  contype:
    description:
      - Type of the rule. If not set, C(postgresql_pg_hba) will only return contents.
    type: str
    choices: [ local, host, hostnossl, hostssl, hostgssenc, hostnogssenc ]
  comment:
    description:
      - A comment that will be placed in the same line behind the rule. See also the I(keep_comments_at_rules) parameter.
    type: str
    version_added: '1.5.0'
  databases:
    description:
      - Databases this line applies to.
    default: all
    type: str
  dest:
    description:
      - Path to C(pg_hba) file to modify.
    type: path
    required: true
  method:
    description:
      - Authentication method to be used.
    type: str
    choices: [ cert, gss, ident, krb5, ldap, md5, pam, password, peer, radius, reject, scram-sha-256 , sspi, trust ]
    default: md5
  netmask:
    description:
      - The netmask of the source address.
    type: str
  options:
    description:
      - Additional options for the authentication I(method).
    type: str
  order:
    description:
      - The entries will be written out in a specific order.
        With this option you can control by which field they are ordered first, second and last.
        s=source, d=databases, u=users.
        This option is deprecated since 2.9 and will be removed in community.postgresql 3.0.0.
        Sortorder is now hardcoded to sdu.
    type: str
    default: sdu
    choices: [ sdu, sud, dsu, dus, usd, uds ]
  overwrite:
    description:
      - Remove all existing rules before adding rules. (Like I(state=absent) for all pre-existing rules.)
    type: bool
    default: false
  keep_comments_at_rules:
    description:
      - If C(true), comments that stand together with a rule in one line are kept behind that line.
      - If C(false), such comments are moved to the beginning of the file, like all other comments.
    type: bool
    default: false
    version_added: '1.5.0'
  rules:
    description:
      - A list of objects, specifying rules for the pg_hba.conf. Use this to manage multiple rules at once.
      - "Each object can have the following keys (the 'rule-specific arguments'), which are treated the same as if they were arguments of this module:"
      - C(address), C(comment), C(contype), C(databases), C(method), C(netmask), C(options), C(state), C(users)
      - See also C(rules_behavior).
    type: list
    elements: dict
  rules_behavior:
    description:
      - "Configure how the I(rules) argument works together with the rule-specific arguments outside the I(rules) argument."
      - See I(rules) for the complete list of rule-specific arguments.
      - When set to C(conflict), fail if I(rules) and, for example, I(address) are set.
      - If C(combine), the normal rule-specific arguments are not defining a rule, but are used as defaults for the arguments in the I(rules) argument.
      - Is used only when I(rules) is specified, ignored otherwise.
    type: str
    choices: [ conflict, combine ]
    default: conflict
  state:
    description:
      - The lines will be added/modified when C(state=present) and removed when C(state=absent).
    type: str
    default: present
    choices: [ absent, present ]
  users:
    description:
      - Users this line applies to.
    type: str
    default: all

notes:
   - The default authentication assumes that on the host, you are either logging in as or
     sudo'ing to an account with appropriate permissions to read and modify the file.
   - This module also returns the pg_hba info. You can use this module to only retrieve it by only specifying I(dest).
     The info can be found in the returned data under key pg_hba, being a list, containing a dict per rule.
   - This module will sort resulting C(pg_hba) files if a rule change is required.
     This could give unexpected results with manual created hba files, if it was improperly sorted.
     For example a rule was created for a net first and for a ip in that net range next.
     In that situation, the 'ip specific rule' will never hit, it is in the C(pg_hba) file obsolete.
     After the C(pg_hba) file is rewritten by the M(community.postgresql.postgresql_pg_hba) module, the ip specific rule will be sorted above the range rule.
     And then it will hit, which will give unexpected results.
   - With the 'order' parameter you can control which field is used to sort first, next and last.
   - The module supports a check mode and a diff mode.

seealso:
- name: PostgreSQL pg_hba.conf file reference
  description: Complete reference of the PostgreSQL pg_hba.conf file documentation.
  link: https://www.postgresql.org/docs/current/auth-pg-hba-conf.html

requirements:
    - ipaddress

author:
- Sebastiaan Mannem (@sebasmannem)
- Felix Hamme (@betanummeric)
'''

EXAMPLES = '''
- name: Grant users joe and simon access to databases sales and logistics from ipv6 localhost ::1/128 using peer authentication
  community.postgresql.postgresql_pg_hba:
    dest: /var/lib/postgres/data/pg_hba.conf
    contype: host
    users: joe,simon
    source: ::1
    databases: sales,logistics
    method: peer
    create: true

- name: Grant user replication from network 192.168.0.100/24 access for replication with client cert authentication
  community.postgresql.postgresql_pg_hba:
    dest: /var/lib/postgres/data/pg_hba.conf
    contype: host
    users: replication
    source: 192.168.0.100/24
    databases: replication
    method: cert

- name: Revoke access from local user mary on database mydb
  community.postgresql.postgresql_pg_hba:
    dest: /var/lib/postgres/data/pg_hba.conf
    contype: local
    users: mary
    databases: mydb
    state: absent

- name: Grant some_user access to some_db, comment that and keep other rule-specific comments attached to their rules
  community.postgresql.postgresql_pg_hba:
    dest: /var/lib/postgres/data/pg_hba.conf
    contype: host
    users: some_user
    databases: some_db
    method: md5
    source: ::/0
    keep_comments_at_rules: true
    comment: "this rule is an example"

- name: Replace everything with a new set of rules
  community.postgresql.postgresql_pg_hba:
    dest: /var/lib/postgres/data/pg_hba.conf
    overwrite: true # remove preexisting rules

    # custom defaults
    rules_behavior: combine
    contype: hostssl
    address: 2001:db8::/64
    comment: added in bulk

    rules:
    - users: user1
      databases: db1
      # contype, address and comment come from custom default
    - users: user2
      databases: db2
      comment: added with love # overwrite custom default for this rule
      # contype and address come from custom default
    - users: user3
      databases: db3
      # contype, address and comment come from custom default
'''

RETURN = r'''
msgs:
    description: List of textual messages what was done.
    returned: always
    type: list
    sample:
       "msgs": [
          "Removing",
          "Changed",
          "Writing"
        ]
backup_file:
    description: File that the original pg_hba file was backed up to.
    returned: changed
    type: str
    sample: /tmp/pg_hba_jxobj_p
pg_hba:
    description: List of the pg_hba rules as they are configured in the specified hba file.
    returned: always
    type: list
    sample:
      "pg_hba": [
         {
            "db": "all",
            "method": "md5",
            "src": "samehost",
            "type": "host",
            "usr": "all"
         }
      ]
'''

import os
import re
import traceback

IPADDRESS_IMP_ERR = None
try:
    import ipaddress
except ImportError:
    IPADDRESS_IMP_ERR = traceback.format_exc()

import tempfile
import shutil
from ansible.module_utils.basic import AnsibleModule, missing_required_lib

# from ansible.module_utils.postgres import postgres_common_argument_spec

PG_HBA_METHODS = ["trust", "reject", "md5", "password", "gss", "sspi", "krb5", "ident", "peer",
                  "ldap", "radius", "cert", "pam", "scram-sha-256"]
PG_HBA_TYPES = ["local", "host", "hostssl", "hostnossl", "hostgssenc", "hostnogssenc"]
PG_HBA_ORDERS = ["sdu", "sud", "dsu", "dus", "usd", "uds"]
PG_HBA_HDR = ['type', 'db', 'usr', 'src', 'mask', 'method', 'options']

WHITESPACES_RE = re.compile(r'\s+')


class PgHbaError(Exception):
    '''
    This exception is raised when parsing the pg_hba file ends in an error.
    '''


class PgHbaRuleError(PgHbaError):
    '''
    This exception is raised when parsing the pg_hba file ends in an error.
    '''


class PgHbaRuleChanged(PgHbaRuleError):
    '''
    This exception is raised when a new parsed rule is a changed version of an existing rule.
    '''


class PgHbaValueError(PgHbaError):
    '''
    This exception is raised when a new parsed rule is a changed version of an existing rule.
    '''


class PgHbaRuleValueError(PgHbaRuleError):
    '''
    This exception is raised when a new parsed rule is a changed version of an existing rule.
    '''


class PgHba(object):
    """
    PgHba object to read/write entries to/from.
    pg_hba_file - the pg_hba file almost always /etc/pg_hba
    """

    def __init__(self, pg_hba_file=None, order="sdu", backup=False, create=False, keep_comments_at_rules=False):
        if order not in PG_HBA_ORDERS:
            msg = "invalid order setting {0} (should be one of '{1}')."
            raise PgHbaError(msg.format(order, "', '".join(PG_HBA_ORDERS)))
        self.pg_hba_file = pg_hba_file
        self.rules = None
        self.comment = None
        self.order = order
        self.backup = backup
        self.last_backup = None
        self.create = create
        self.keep_comments_at_rules = keep_comments_at_rules
        self.unchanged()
        # self.databases will be update by add_rule and gives some idea of the number of databases
        # (at least that are handled by this pg_hba)
        self.databases = set(['postgres', 'template0', 'template1'])

        # self.databases will be update by add_rule and gives some idea of the number of users
        # (at least that are handled by this pg_hba) since this might also be groups with multiple
        # users, this might be totally off, but at least it is some info...
        self.users = set(['postgres'])

        self.read()

    def clear_rules(self):
        self.rules = {}

    def unchanged(self):
        '''
        This method resets self.diff to a empty default
        '''
        self.diff = {'before': {'file': self.pg_hba_file, 'pg_hba': []},
                     'after': {'file': self.pg_hba_file, 'pg_hba': []}}

    def read(self):
        '''
        Read in the pg_hba from the system
        '''
        self.rules = {}
        self.comment = []
        # read the pg_hbafile
        try:
            with open(self.pg_hba_file, 'r') as file:
                for line in file:
                    # split into line and comment
                    line = line.strip()
                    comment = None
                    if '#' in line:
                        line, comment = line.split('#', 1)
                        if comment == '':
                            comment = None

                    # if there is just a comment, save it
                    if line == '':
                        if comment is not None:
                            self.comment.append('#' + comment)
                    else:
                        if comment is not None and not self.keep_comments_at_rules:
                            # save the comment independent of the line
                            self.comment.append('#' + comment)
                            comment = None
                        try:
                            self.add_rule(PgHbaRule(line=line, comment=comment))
                        except PgHbaRuleError:
                            pass
            self.unchanged()
        except IOError:
            pass

    def write(self, backup_file=''):
        '''
        This method writes the PgHba rules (back) to a file.
        '''
        if not self.changed():
            return False

        contents = self.render()
        if self.pg_hba_file:
            if not (os.path.isfile(self.pg_hba_file) or self.create):
                raise PgHbaError("pg_hba file '{0}' doesn't exist. "
                                 "Use create option to autocreate.".format(self.pg_hba_file))
            if self.backup and os.path.isfile(self.pg_hba_file):
                if backup_file:
                    self.last_backup = backup_file
                else:
                    _backup_file_h, self.last_backup = tempfile.mkstemp(prefix='pg_hba')
                shutil.copy(self.pg_hba_file, self.last_backup)
            fileh = open(self.pg_hba_file, 'w')
        else:
            filed, _path = tempfile.mkstemp(prefix='pg_hba')
            fileh = os.fdopen(filed, 'w')

        fileh.write(contents)
        self.unchanged()
        fileh.close()
        return True

    def add_rule(self, rule):
        '''
        This method can be used to add a rule to the list of rules in this PgHba object
        '''
        key = rule.key()
        try:
            try:
                oldrule = self.rules[key]
            except KeyError:
                raise PgHbaRuleChanged
            ekeys = set(list(oldrule.keys()) + list(rule.keys()))
            ekeys.remove('line')
            for k in ekeys:
                if oldrule.get(k) != rule.get(k):
                    raise PgHbaRuleChanged('{0} changes {1}'.format(rule, oldrule))
        except PgHbaRuleChanged:
            self.rules[key] = rule
            self.diff['after']['pg_hba'].append(rule.line())
            if rule['db'] not in ['all', 'samerole', 'samegroup', 'replication']:
                databases = set(rule['db'].split(','))
                self.databases.update(databases)
            if rule['usr'] != 'all':
                user = rule['usr']
                if user[0] == '+':
                    user = user[1:]
                self.users.add(user)

    def remove_rule(self, rule):
        '''
        This method can be used to find and remove a rule. It doesn't look for the exact rule, only
        the rule with the same key.
        '''
        keys = rule.key()
        try:
            del self.rules[keys]
            self.diff['before']['pg_hba'].append(rule.line())
        except KeyError:
            pass

    def get_rules(self, with_lines=False):
        '''
        This method returns all the rules of the PgHba object
        '''
        rules = sorted(self.rules.values())
        for rule in rules:
            ret = {}
            for key, value in rule.items():
                ret[key] = value
            if not with_lines:
                if 'line' in ret:
                    del ret['line']
            else:
                ret['line'] = rule.line()

            yield ret

    def render(self):
        '''
        This method renders the content of the PgHba rules and comments.
        The returning value can be used directly to write to a new file.
        '''
        comment = '\n'.join(self.comment)
        rule_lines = []
        for rule in self.get_rules(with_lines=True):
            if 'comment' in rule:
                rule_lines.append(rule['line'] + '\t#' + rule['comment'])
            else:
                rule_lines.append(rule['line'])
        result = comment + '\n' + '\n'.join(rule_lines)
        # End it properly with a linefeed (if not already).
        if result and result[-1] not in ['\n', '\r']:
            result += '\n'
        return result

    def changed(self):
        '''
        This method can be called to detect if the PgHba file has been changed.
        '''
        return bool(self.diff['before']['pg_hba'] or self.diff['after']['pg_hba'])


class PgHbaRule(dict):
    '''
    This class represents one rule as defined in a line in a PgHbaFile.
    '''

    def __init__(self, contype=None, databases=None, users=None, source=None, netmask=None,
                 method=None, options=None, line=None, comment=None):
        '''
        This function can be called with a comma seperated list of databases and a comma seperated
        list of users and it will act as a generator that returns a expanded list of rules one by
        one.
        '''

        super(PgHbaRule, self).__init__()

        if line:
            # Read values from line if parsed
            self.fromline(line)

        if comment:
            self['comment'] = comment

        # read rule cols from parsed items
        rule = dict(zip(PG_HBA_HDR, [contype, databases, users, source, netmask, method, options]))
        for key, value in rule.items():
            if value:
                self[key] = value

        # Some sanity checks
        for key in ['method', 'type']:
            if key not in self:
                raise PgHbaRuleError('Missing {0} in rule {1}'.format(key, self))

        if self['method'] not in PG_HBA_METHODS:
            msg = "invalid method {0} (should be one of '{1}')."
            raise PgHbaRuleValueError(msg.format(self['method'], "', '".join(PG_HBA_METHODS)))

        if self['type'] not in PG_HBA_TYPES:
            msg = "invalid connection type {0} (should be one of '{1}')."
            raise PgHbaRuleValueError(msg.format(self['type'], "', '".join(PG_HBA_TYPES)))

        if self['type'] == 'local':
            self.unset('src')
            self.unset('mask')
        elif 'src' not in self:
            raise PgHbaRuleError('Missing src in rule {1}'.format(self))
        elif '/' in self['src']:
            self.unset('mask')
        else:
            self['src'] = str(self.source())
            self.unset('mask')

    def unset(self, key):
        '''
        This method is used to unset certain columns if they exist
        '''
        if key in self:
            del self[key]

    def line(self):
        '''
        This method can be used to return (or generate) the line
        '''
        try:
            return self['line']
        except KeyError:
            self['line'] = "\t".join([self[k] for k in PG_HBA_HDR if k in self.keys()])
            return self['line']

    def fromline(self, line):
        '''
        split into 'type', 'db', 'usr', 'src', 'mask', 'method', 'options' cols
        '''
        if WHITESPACES_RE.sub('', line) == '':
            # empty line. skip this one...
            return
        cols = WHITESPACES_RE.split(line)
        if len(cols) < 4:
            msg = "Rule {0} has too few columns."
            raise PgHbaValueError(msg.format(line))
        if cols[0] not in PG_HBA_TYPES:
            msg = "Rule {0} has unknown type: {1}."
            raise PgHbaValueError(msg.format(line, cols[0]))
        if cols[0] == 'local':
            cols.insert(3, None)  # No address
            cols.insert(3, None)  # No IP-mask
        if len(cols) < 6:
            cols.insert(4, None)  # No IP-mask
        elif cols[5] not in PG_HBA_METHODS:
            cols.insert(4, None)  # No IP-mask
        if cols[5] not in PG_HBA_METHODS:
            raise PgHbaValueError("Rule {0} of '{1}' type has invalid auth-method '{2}'".format(line, cols[0], cols[5]))

        if len(cols) < 7:
            cols.insert(6, None)  # No auth-options
        else:
            cols[6] = " ".join(cols[6:])  # combine all auth-options
        rule = dict(zip(PG_HBA_HDR, cols[:7]))
        for key, value in rule.items():
            if value:
                self[key] = value

    def key(self):
        '''
        This method can be used to get the key from a rule.
        '''
        if self['type'] == 'local':
            source = 'local'
        else:
            source = str(self.source())
        return (source, self['db'], self['usr'])

    def source(self):
        '''
        This method is used to get the source of a rule as an ipaddress object if possible.
        '''
        if 'mask' in self.keys():
            try:
                ipaddress.ip_address(u'{0}'.format(self['src']))
            except ValueError:
                raise PgHbaValueError('Mask was specified, but source "{0}" '
                                      'is not valid ip'.format(self['src']))
            # ipaddress module cannot work with ipv6 netmask, so lets convert it to prefixlen
            # furthermore ipv4 with bad netmask throws 'Rule {} doesn't seem to be an ip, but has a
            # mask error that doesn't seem to describe what is going on.
            try:
                mask_as_ip = ipaddress.ip_address(u'{0}'.format(self['mask']))
            except ValueError:
                raise PgHbaValueError('Mask {0} seems to be invalid'.format(self['mask']))
            binvalue = "{0:b}".format(int(mask_as_ip))
            if '01' in binvalue:
                raise PgHbaValueError('IP mask {0} seems invalid '
                                      '(binary value has 1 after 0)'.format(self['mask']))
            prefixlen = binvalue.count('1')
            sourcenw = '{0}/{1}'.format(self['src'], prefixlen)
            try:
                return ipaddress.ip_network(u'{0}'.format(sourcenw), strict=False)
            except ValueError:
                raise PgHbaValueError('{0} is not valid address range'.format(sourcenw))

        try:
            return ipaddress.ip_network(u'{0}'.format(self['src']), strict=False)
        except ValueError:
            return self['src']

    def __lt__(self, other):
        """This function helps sorted to decide how to sort.

        It just checks itself against the other and decides on some key values
        if it should be sorted higher or lower in the list.
        The way it works:
        For networks, every 1 in 'netmask in binary' makes the subnet more specific.
        Therefore I chose to use prefix as the weight.
        So a single IP (/32) should have twice the weight of a /16 network.
        To keep everything in the same weight scale,
        - for ipv6, we use a weight scale of 0 (all possible ipv6 addresses) to 128 (single ip)
        - for ipv4, we use a weight scale of 0 (all possible ipv4 addresses) to 128 (single ip)
        Therefore for ipv4, we use prefixlen (0-32) * 4 for weight,
        which corresponds to ipv6 (0-128).
        """
        myweight = self.source_weight()
        hisweight = other.source_weight()
        if myweight != hisweight:
            return myweight > hisweight

        myweight = self.db_weight()
        hisweight = other.db_weight()
        if myweight != hisweight:
            return myweight < hisweight

        myweight = self.user_weight()
        hisweight = other.user_weight()
        if myweight != hisweight:
            return myweight < hisweight
        try:
            return self['src'] < other['src']
        except TypeError:
            return self.source_type_weight() < other.source_type_weight()
        except Exception:
            # When all else fails, just compare the exact line.
            return self.line() < other.line()

    def source_weight(self):
        """Report the weight of this source net.

        Basically this is the netmask, where IPv4 is normalized to IPv6
        (IPv4/32 has the same weight as IPv6/128).
        """
        if self['type'] == 'local':
            return 130

        sourceobj = self.source()
        if isinstance(sourceobj, ipaddress.IPv4Network):
            return sourceobj.prefixlen * 4
        if isinstance(sourceobj, ipaddress.IPv6Network):
            return sourceobj.prefixlen
        if isinstance(sourceobj, str):
            # You can also write all to match any IP address,
            # samehost to match any of the server's own IP addresses,
            # or samenet to match any address in any subnet that the server is connected to.
            if sourceobj == 'all':
                # (all is considered the full range of all ips, which has a weight of 0)
                return 0
            if sourceobj == 'samehost':
                # (sort samehost second after local)
                return 129
            if sourceobj == 'samenet':
                # Might write some fancy code to determine all prefix's
                # from all interfaces and find a sane value for this one.
                # For now, let's assume IPv4/24 or IPv6/96 (both have weight 96).
                return 96
            if sourceobj[0] == '.':
                # suffix matching (domain name), let's assume a very large scale
                # and therefore a very low weight IPv4/16 or IPv6/64 (both have weight 64).
                return 64
            # hostname, let's assume only one host matches, which is
            # IPv4/32 or IPv6/128 (both have weight 128)
            return 128
        raise PgHbaValueError('Cannot deduct the source weight of this source {1}'.format(sourceobj))

    def source_type_weight(self):
        """Give a weight on the type of this source.

        Basically make sure that IPv6Networks are sorted higher than IPv4Networks.
        This is a 'when all else fails' solution in __lt__.
        """
        if self['type'] == 'local':
            return 3

        sourceobj = self.source()
        if isinstance(sourceobj, ipaddress.IPv4Network):
            return 2
        if isinstance(sourceobj, ipaddress.IPv6Network):
            return 1
        if isinstance(sourceobj, str):
            return 0
        raise PgHbaValueError('This source {0} is of an unknown type...'.format(sourceobj))

    def db_weight(self):
        """Report the weight of the database.

        Normally, just 1, but for replication this is 0, and for 'all', this is more than 2.
        """
        if self['db'] == 'all':
            return 100000
        if self['db'] == 'replication':
            return 0
        if self['db'] in ['samerole', 'samegroup']:
            return 1
        return 1 + self['db'].count(',')

    def user_weight(self):
        """Report weight when comparing users."""
        if self['usr'] == 'all':
            return 1000000
        return 1


def main():
    '''
    This function is the main function of this module
    '''
    # argument_spec = postgres_common_argument_spec()
    argument_spec = dict()
    argument_spec.update(
        address=dict(type='str', default='samehost', aliases=['source', 'src']),
        backup=dict(type='bool', default=False),
        backup_file=dict(type='str'),
        contype=dict(type='str', default=None, choices=PG_HBA_TYPES),
        comment=dict(type='str', default=None),
        create=dict(type='bool', default=False),
        databases=dict(type='str', default='all'),
        dest=dict(type='path', required=True),
        method=dict(type='str', default='md5', choices=PG_HBA_METHODS),
        netmask=dict(type='str'),
        options=dict(type='str'),
        order=dict(type='str', default="sdu", choices=PG_HBA_ORDERS,
                   removed_in_version='3.0.0', removed_from_collection='community.postgresql'),
        keep_comments_at_rules=dict(type='bool', default=False),
        state=dict(type='str', default="present", choices=["absent", "present"]),
        users=dict(type='str', default='all'),
        rules=dict(type='list', elements='dict'),
        rules_behavior=dict(type='str', default='conflict', choices=['combine', 'conflict']),
        overwrite=dict(type='bool', default=False),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        add_file_common_args=True,
        supports_check_mode=True
    )
    if IPADDRESS_IMP_ERR is not None:
        module.fail_json(msg=missing_required_lib('ipaddress'), exception=IPADDRESS_IMP_ERR)

    create = bool(module.params["create"] or module.check_mode)
    if module.check_mode:
        backup = False
    else:
        backup = module.params['backup']
        backup_file = module.params['backup_file']
    dest = module.params["dest"]
    order = module.params["order"]
    keep_comments_at_rules = module.params["keep_comments_at_rules"]
    rules = module.params["rules"]
    rules_behavior = module.params["rules_behavior"]
    overwrite = module.params["overwrite"]

    ret = {'msgs': []}
    try:
        pg_hba = PgHba(dest, order, backup=backup, create=create, keep_comments_at_rules=keep_comments_at_rules)
    except PgHbaError as error:
        module.fail_json(msg='Error reading file:\n{0}'.format(error))

    if overwrite:
        pg_hba.clear_rules()

    rule_keys = [
        'address',
        'comment',
        'contype',
        'databases',
        'method',
        'netmask',
        'options',
        'state',
        'users'
    ]
    if rules is None:
        single_rule = dict()
        for key in rule_keys:
            single_rule[key] = module.params[key]
        rules = [single_rule]
    else:
        if rules_behavior == 'conflict':
            # it's ok if the module default is set
            used_rule_keys = [key for key in rule_keys if module.params[key] != argument_spec[key].get('default', None)]
            if len(used_rule_keys) > 0:
                module.fail_json(msg='conflict: either argument "rules_behavior" needs to be changed or "rules" must'
                                     ' not be set or {0} must not be set'.format(used_rule_keys))

        new_rules = []
        for index, rule in enumerate(rules):
            # alias handling
            address_keys = [key for key in rule.keys() if key in ('address', 'source', 'src')]
            if len(address_keys) > 1:
                module.fail_json(msg='rule number {0} of the "rules" argument ({1}) uses ambiguous settings: '
                                     '{2} are aliases, only one is allowed'.format(index, address_keys, rule))
            if len(address_keys) == 1:
                address = rule[address_keys[0]]
                del rule[address_keys[0]]
                rule['address'] = address

            for key in rule_keys:
                if key not in rule:
                    if rules_behavior == 'combine':
                        # use user-supplied defaults or module defaults
                        rule[key] = module.params[key]
                    else:
                        # use module defaults
                        rule[key] = argument_spec[key].get('default', None)
            new_rules.append(rule)
        rules = new_rules

    for rule in rules:
        if rule.get('contype', None) is None:
            continue

        try:
            for database in rule['databases'].split(','):
                for user in rule['users'].split(','):
                    pg_hba_rule = PgHbaRule(rule['contype'], database, user, rule['address'], rule['netmask'],
                                            rule['method'], rule['options'], comment=rule['comment'])
                    if rule['state'] == "present":
                        ret['msgs'].append('Adding rule {0}'.format(pg_hba_rule))
                        pg_hba.add_rule(pg_hba_rule)
                    else:
                        ret['msgs'].append('Removing rule {0}'.format(pg_hba_rule))
                        pg_hba.remove_rule(pg_hba_rule)
        except PgHbaError as error:
            module.fail_json(msg='Error modifying rules:\n{0}'.format(error))
    file_args = module.load_file_common_arguments(module.params)
    ret['changed'] = changed = pg_hba.changed()
    if changed:
        ret['msgs'].append('Changed')
        ret['diff'] = pg_hba.diff

        if not module.check_mode:
            ret['msgs'].append('Writing')
            try:
                if pg_hba.write(backup_file):
                    module.set_fs_attributes_if_different(file_args, True, pg_hba.diff,
                                                          expand=False)
            except PgHbaError as error:
                module.fail_json(msg='Error writing file:\n{0}'.format(error))
            if pg_hba.last_backup:
                ret['backup_file'] = pg_hba.last_backup

    ret['pg_hba'] = list(pg_hba.get_rules())
    module.exit_json(**ret)


if __name__ == '__main__':
    main()
