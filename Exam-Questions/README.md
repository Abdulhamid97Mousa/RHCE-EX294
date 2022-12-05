# Ansible Sample Exam for RHCE EX294

This is a sample Ansible exam that I’ve created to prepare for the new RHCE exam EX294. As with the real exam, no answers to the sample exam questions will be provided.

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
vim /home/automation/plays/inventory
```

> Create the inventory with following contents

```
[proxy]
managed1.example.com

[webservers]
managed2.example.com
managed3.example.com

[database]
managed3.example.com
managed4.example.com

[public:children]
webservers
proxy
```

> Save it to /home/automation/plays/inventory

- **step5:** Create the config file with following content
  > Create the ansible.cfg `ansible configuration file` with following contents

```
[defaults]
inventory = ./inventory
forks = 8
log_path = /var/log/ansible/execution.log
roles_path = ~/.ansible/roles:/usr/share/ansible/roles:/etc/ansible/roles:/home/automation/plays/roles

[privilege_escalation]
become = false
become_ask_pass = false
become_method = sudo
```

> Save it to /home/automation/plays/ansible.cfg

General thoughts

Ensure that you have proper ownership, to restore it call

```
chown -R automation:automation /home/automation
```

> Do the same for /var/log/ansible directory
