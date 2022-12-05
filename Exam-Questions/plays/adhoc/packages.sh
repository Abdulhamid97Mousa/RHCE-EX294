#!/usr/bin/bash

# Create the directory for ssh keys
ansible localhost -m file -a 'path=/home/automation/.ssh state=directory'
# Generate the keypair
ansible localhost -m openssh_keypair -a "path=/home/automation/.ssh/id_rsa owner=automation group=automation type=rsa"
# Create the user, calling it with sudo will avoid host key checking
ansible all -b -m user -a "name=automation password={{ 'devops' | password_hash('sha512') }}"
# Share public key with rest of the nodes, inventory is taken from the previous exercise
ansible all -b -m authorized_key -a "key={{ lookup('file', '/home/automation/.ssh/id_rsa.pub') }} user=automation state=present"
# Allow passwordless sudo
ansible all -b -m copy -a 'content="automation ALL=(ALL) NOPASSWD:ALL" dest=/etc/sudoers.d/automation'
