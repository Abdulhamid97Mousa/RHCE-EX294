#!/bin/bash
file='/etc/os-release'
id=$(grep '^ID=' $file | cut -f2 -d'=' )
if [ $id = 'ubuntu' ] ; then
	echo "Installing vim on Ubuntu"
	sudo apt-get install -y vim
else
	echo "Installing vim on RHEL Platforms"
	sudo yum install -y vim-enhanced
fi