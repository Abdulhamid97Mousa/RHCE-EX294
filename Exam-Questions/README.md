# Ansible Sample Exam for RHCE EX294

This is a sample Ansible exam that I’ve created to prepare for the new RHCE exam EX294. As with the real exam, no perfect answers to the sample exam questions will be provided, but more or less correct and accurate.

## Requirements

There are 18 questions in total could be more or less.
You will need five RHEL 8 virtual machines to be able to successfully complete all questions.

One VM will be configured as an Ansible control node. Other four VMs will be used to apply playbooks to solve the sample exam questions. The following FQDNs will be used throughout the sample exam.

| FQDN                      | Description                            |
| ------------------------- | -------------------------------------- |
| repo.ansi.example.com     | install packages from                  |
|                           | http://repo.ansi.example.com/BaseOS    |
|                           | http://repo.ansi.example.com/AppStream |
| control.ansi.example.com  | Ansible control node                   |
| managed1.ansi.example.com | managed host                           |
| managed2.ansi.example.com | managed host                           |
| managed3.ansi.example.com | managed host                           |
| managed4.ansi.example.com | managed host                           |

```mermaid
flowchart TD;
    A[Fire Up 6 VMs] --> B(#A Controller Node);
    B -- Repo to pull packages from it --> Z[repository];
    B -- Controlled By Node #A --> C[Managed Node1];
    B -- Controlled By Node #A --> D[Managed Node2];
    B -- Controlled By Node #A --> E[Managed Node3];
    B -- Controlled By Node #A --> F[Managed Node4];
```

## Lab Setup

> you can create the lab setup manually, but instead i've `Vagrantfile` which you can use inorder to create this setup, please go to this website for more information regarding lab setup https://github.com/rdbreak/rhce8env

## Q1. Ansible Installation and Configuration

- Install the ansible package on the control node
- Create automation user with devops password
- the user should be allowed to execute any command without providing password to the prompt "Add the automation user to sudoers group"
- Create inventory on the control node at /home/automation/plays/inventory. Meet following requirements:

  - managed1.example.com should be a member of the proxy host group
  - managed1.example.com should be a member of the proxy host group
  - managed2.example.com should be a member of the webservers host group
  - managed3.example.com should be a member of the webservers and database host group
  - managed4.example.com should be a member of the database host group
  - proxy and webservers belong to group named public

- Create a config file at /home/automation/plays/ansible.cfg with following requirements:
  - priviledged escalation is disabled by default
  - ansible should manage 8 hosts at a single time
  - use previously defined inventory file by default
  - uses /var/log/ansible/execution.log to save information related to playbook execution
  - roles path should include /home/automation/plays/roles
  - ensure that priviledge escalation method is set to sudo
  - do not allow ansible to ask for password when elevating privileges

## A1. Ansible Installation and Configuration

- **step1:** Installing the ansible

```
yum install -y ansible
```

- **step2:** Configuring the user account

> Create an account

```
useradd automation
```

> Set password

```
echo devops | passwd --stdin automation
```

- **step3:** Allow access to privileged commands

```
echo "automation ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/automation
```

- **step4:** Creating inventory

> Create directory for the inventory

```
mkdir -p /home/automation/plays
mkdir -p /home/automation/plays/roles
sudo mkdir -p /var/log/ansible/
sudo touch /var/log/ansible/execution.log
vim /home/automation/plays/inventory
```

> Manage your /etc/hosts file to resolve host ip address to FQDNs

```
192.168.55.199 repo.ansi.example.com     repo
192.168.55.200 control.ansi.example.com  control
192.168.55.201 node1.ansi.example.com    managed1
192.168.55.202 node2.ansi.example.com    managed2
192.168.55.203 node3.ansi.example.com    managed3
192.168.55.204 node4.ansi.example.com    managed4
```

> Create the inventory with following contents

```
[proxy]
managed1 ansible_hostname=managed1 ansible_host=192.168.55.201 ansible_user=vagrant ansible_ssh_pass=vagrant ansible_python_interpreter=/usr/bin/python3

[webservers]
managed2 ansible_hostname=managed2 ansible_host=192.168.55.202 ansible_user=vagrant ansible_ssh_pass=vagrant ansible_python_interpreter=/usr/bin/python3
managed3 ansible_hostname=managed3 ansible_host=192.168.55.203 ansible_user=vagrant ansible_ssh_pass=vagrant ansible_python_interpreter=/usr/bin/python3

[database]
managed3 ansible_hostname=managed3 ansible_host=192.168.55.203 ansible_user=vagrant ansible_ssh_pass=vagrant ansible_python_interpreter=/usr/bin/python3
managed4 ansible_hostname=managed4 ansible_host=192.168.55.204 ansible_user=vagrant ansible_ssh_pass=vagrant ansible_python_interpreter=/usr/bin/python3

[public:children]
webservers
proxy
```

> Save it to /home/automation/plays/inventory

- **step5:** Create the config file with following content

> Create the ansible.cfg `ansible configuration file` with following contents

```
[defaults]
remote_user=automation
inventory=./inventory
forks=8
log_path=/var/log/ansible/execution.log
roles_path=~/.ansible/roles:/usr/share/ansible/roles:/etc/ansible/roles:/home/automation/plays/roles

[privilege_escalation]
become=false
become_ask_pass=false
become_method=sudo
become_user=root
```

> Save it to /home/automation/plays/ansible.cfg

General thoughts

Ensure that you have proper ownership, to restore it call

```
chown -R automation:automation /home/automation
```

> Do the same for /var/log/ansible directory

```
sudo chown -R automation:automation /var/log/ansible
```

## A2. Ad-Hoc Commands

Generate an SSH keypair on the control node. You can perform this step manually.

- Write a script `/home/automation/plays/adhoc` that uses Ansible ad-hoc commands to achieve the following:
  - User automation is created on all inventory hosts (not the control node).
  - SSH key (that you generated) is copied to all inventory hosts for the automation user and stored in `/home/automation/.ssh/authorized_keys`.
  - The automation user is allowed to elevate privileges on all inventory hosts without having to provide a password.

> **After running the adhoc script on the control node as the automation user, you should be able to SSH into all inventory hosts using the automation user without password, as well as a run all privileged commands.**

## Q2. Ad-Hoc Commands

- **step1:** you should test ansible adhoc commands before writing the bash script, the command `ansible localhost -m ping` is usefull, use it few times against target hosts to verify connectivity

- **step2:** you should read and understand the inventory file, if you haven't wrote your inventory by yourself, then you can check the inventory file in this repository.

```
#!/bin/bash
# Create the directory for ssh keys.
ansible localhost -m file -a "path=/home/automation/.ssh state=directory"
# Generate the ssh keys.
ansible localhost -m openssh_keypair -a "path=/home/automation/.ssh/id_rsa owner=automation group=automation type=rsa"
# Create automation user on managed nodes.
ansible all -m user -a "name=automation password={{ 'devops' | password_hash('sha512') }}"
# share public key to managed nodes, remember to check your ansible.cfg configuration because this command needs sudo privileges.
ansible all -m authorized_key -a "key={{ lookup('file', '/home/automation/.ssh/id_rsa.pub') }} user=automation state=present"
# Add the automation user in each managed node to sudoers group for privilege escalation.
ansible all -m copy -a "content='automation ALL=(root) NOPASSWD:ALL' dest=/etc/sudoers.d/automation"
```

## Q3. Archiving

- Create a playbook that meets following requirements:
  - Creates a gzip archive containing `/etc` and stores it at `/backup/configuration.gz` on the managed hosts.
  - Is placed at `/home/automation/plays/archive.yml`
  - Runs against `all` host group
  - Retrieves archives from the managed nodes and stores them at `/backup/<hostname>-configuration.gz` on the control node
  - User automation should be owner of /backup and everything underneath. Both on the managed hosts and the control node. Only owner and members of his group should be able to read and manage files inside. Anyone should be allowed to list contents of `/backup`.

## A3. Archiving

```
- name: Archiving
  hosts: localhost
  become: true
  gather_facts: false
  tasks:
    - name: Create a backup folder
      file:
        path: '/backup'
        state: 'directory'
        owner: automation
        group: automation
        mode: 0755

- name: Archive config files
  hosts: all
  become: true
  gather_facts: false
  tasks:
    - name: Create a folder for archive
      file:
        path: /backup
        owner: automation
        group: automation
        state: directory
        mode: 0755

- name: create the archive
  hosts: all
  become: true
  gather_facts: false
  tasks:
    - name: create the archive
      archive:
        path: /etc
        dest: /backup/configuration.gz
        format: gz
        owner: automation
        group: automation
        mode: 0660

- name: fetch the archive
  hosts: all
  become: true
  gather_facts: false
  tasks:
    - name: Retrieves archives from managed nodes
      fetch:
        src: /backup/configuration.gz
        dest: /backup/{{ ansible_hostname }}-configuration.gz
        owner: automation
        group: automation
        mode: 0660
```

## Q4. Group differentiation "File Content"

- Create a playbook `/home/automation/plays/motd.yml` that runs on all inventory hosts and does the following:
  - Populates /etc/motd with text, its content depends on the group, The
  - proxy group should use `Welcome to HAProxy server` as the motd.
  - database group should use `Welcome to MySQL database` as the motd
  - webservers should use `Welcome to Apache server` as the motd.
  - Is placed at `/home/automation/plays/motd.yml`

## A4. Group differentiation "File Content"

- **step1: **Create directories for groups

```
mkdir -p /home/automation/plays/group_vars
mkdir -p /home/automation/plays/group_vars/{proxy,database,webservers}
```

- **step2: **Populate yml for each group group

```
echo "motd: Welcome to HAProxy server" > /home/automation/plays/group_vars/proxy/motd.yml
echo "motd: Welcome to MySQL database" > /home/automation/plays/group_vars/database/motd.yml
echo "motd: Welcome to Apache server" > /home/automation/plays/group_vars/webservers/motd.yml
```

- **step3: **Create the `motd.yml` playbook

```
- name: file content distributed on managed hosts
  hosts: all
  become: true
  gather_facts: false
  tasks:
    - name: populate the /etc/motd file
      copy:
        content: "{{ motd }}"
        dest: /etc/motd
        owner: root
        group: root
        mode: 644
```

> Another way of solving the problem:

- name: Changing MOTD
  hosts: all
  become: yes
  tasks:
  - name: Copy the content to HAProxy
    copy:
    content: "Welcome to HAProxy server\n"
    dest: /etc/motd
    when: "'proxy' in group_names"
  - name: Copy the content to Apache
    copy:
    content: "Welcome to Apache server\n"
    dest: /etc/motd
    when: "'webservers' in group_names"
  - name: Copy the content to MySQL
    copy:
    content: "Welcome to MySQL server\n"
    dest: /etc/motd
    when: "'database' in group_names"

## Q5. Ansible Facts

- Create a playbook that meets following requirements:
  - Is placed at `/home/automation/plays/ansible_facts.yml`
  - Runs against proxy group
  - Results in possiblity of getting a pair `name=haproxy` from ansible facts path `ansible_local.environment.application` after calling setup module

## A5. Ansible Facts

```
---
- name: Work with Ansible Facts
  hosts: database
  become: yes
  tasks:
  - name: Ensure directory is exist
    file:
    path: /etc/ansible/facts.d
    state: directory
    recurse: yes
  - name: Copy the content to the file
    copy:
    content: "[application]\nname=haproxy\n"
    dest: /etc/ansible/facts.d/environment.fact
```

## Q6: Work with Ansible Facts

Create a playbook `/home/automation/plays/facts.yml` that runs on hosts in the `database host group` and does the following:

A custom Ansible fact `server_role=mysql` is created that can be retrieved from `ansible_local.custom.sample_exam` when using Ansible setup module.

## A6: Work with Ansible Facts

---

- name: Work with Ansible Facts
  hosts: database
  become: yes
  tasks:
  - name: Ensure directory is exist
    file:
    path: /etc/ansible/facts.d
    state: directory
    recurse: yes
  - name: Copy the content to the file
    copy:
    content: "[sample_exam]\nserver_role=mysql\n"
    dest: /etc/ansible/facts.d/custom.fact
