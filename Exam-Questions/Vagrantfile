VAGRANTFILE_API_VERSION = "2"
VAGRANT_DISABLE_VBOXSYMLINKCREATE = "1"
file_to_disk1 = './disk-0-1.vdi'
file_to_disk2 = './disk-0-2.vdi'
file_to_disk3 = './disk-0-3.vdi'
file_to_disk4 = './disk-0-4.vdi'
file_to_disk5 = './disk-1-3.vdi'
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
# Use same SSH key for each machine
config.ssh.insert_key = false
config.vm.box_check_update = false

# Repo
config.vm.define "repo" do |repo|

  repo.vm.box = "rdbreak/rhel8repo"    
  repo.vm.provider "virtualbox" do |repo|
    repo.memory = "1024"
    unless File.exist?(file_to_disk5)
      repo.customize ['createhd', '--filename', file_to_disk5, '--variant', 'Standard', '--size', 2 * 1024]
      repo.customize ['storagectl', :id, '--name', 'SATA Controller', '--add', 'sata', '--portcount', 1]
      repo.customize ['storageattach', :id,  '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', file_to_disk5]       
    end      
  end
  repo.vm.provision :shell, :inline => "pvs | grep '/dev/sdb' && echo 'The disk was already expanded!' || (pvcreate /dev/sdb; vgextend rhel_rhel8 /dev/sdb; lvextend -l +100%FREE /dev/rhel_rhel8/root; xfs_growfs /dev/rhel_rhel8/root)"

  repo.vm.provision :shell, :inline => "sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config; sudo systemctl restart sshd;", run: "always"
  repo.vm.provision :shell, :inline => "yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm -y; sudo yum install -y sshpass python3-pip python3-devel httpd sshpass vsftpd createrepo", run: "always"
  repo.vm.provision :shell, :inline => " python3 -m pip install -U pip ; python3 -m pip install pexpect; python3 -m pip install ansible", run: "always"
  repo.vm.synced_folder ".", "/vagrant", type: "rsync", rsync__exclude: ".git/"
  repo.vm.network "private_network", ip: "192.168.55.199"
end

# Node 1
config.vm.define "node1" do |node1|
  node1.vm.box = "rdbreak/rhel8node"
#  node1.vm.hostname = "node1.ansi.example.com"
  node1.vm.network "private_network", ip: "192.168.55.201"
  node1.vm.synced_folder ".", "/vagrant", type: "rsync", rsync__exclude: [".git/", "*.vdi"]
  node1.vm.provider "virtualbox" do |node1|
    node1.memory = "1024"

    unless File.exist?(file_to_disk1)
      node1.customize ['createhd', '--filename', file_to_disk1, '--variant', 'Fixed', '--size', 2 * 1024]
      node1.customize ['storagectl', :id, '--name', 'SATA Controller', '--add', 'sata', '--portcount', 2]
      node1.customize ['storageattach', :id,  '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', file_to_disk1]
      end
  end
  
    node1.vm.provision "shell", inline: <<-SHELL
    yes| sudo mkfs.ext4 /dev/sdb
    SHELL
    node1.vm.synced_folder ".", "/vagrant"
 end

# Node 2
config.vm.define "node2" do |node2|
  node2.vm.box = "rdbreak/rhel8node"
#  node2.vm.hostname = "node2.ansi.example.com"
  node2.vm.network "private_network", ip: "192.168.55.202"
  node2.vm.synced_folder ".", "/vagrant", type: "rsync", rsync__exclude: [".git/", "*.vdi"]
  node2.vm.provider "virtualbox" do |node2|
    node2.memory = "1024"

    unless File.exist?(file_to_disk2)
      node2.customize ['createhd', '--filename', file_to_disk2, '--variant', 'Fixed', '--size', 2 * 1024]
      node2.customize ['storagectl', :id, '--name', 'SATA Controller', '--add', 'sata', '--portcount', 2]
      node2.customize ['storageattach', :id,  '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', file_to_disk2]
      end
 end
 
    node2.vm.provision "shell", inline: <<-SHELL
    yes| sudo mkfs.ext4 /dev/sdb
    SHELL
    node2.vm.synced_folder ".", "/vagrant"
end

# Node 3
config.vm.define "node3" do |node3|
  node3.vm.box = "rdbreak/rhel8node"
#  node3.vm.hostname = "node3.ansi.example.com"
  node3.vm.network "private_network", ip: "192.168.55.203"
  node3.vm.synced_folder ".", "/vagrant", type: "rsync", rsync__exclude: [".git/", "*.vdi"]
  node3.vm.provider "virtualbox" do |node3|
    node3.memory = "512"

   unless File.exist?(file_to_disk3)
      node3.customize ['createhd', '--filename', file_to_disk3, '--variant', 'Fixed', '--size', 2 * 1024]
      node3.customize ['storagectl', :id, '--name', 'SATA Controller', '--add', 'sata', '--portcount', 2]
      node3.customize ['storageattach', :id,  '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', file_to_disk3]
      end
  end
  
    node3.vm.provision "shell", inline: <<-SHELL
    yes| sudo mkfs.ext4 /dev/sdb
    SHELL
    node3.vm.synced_folder ".", "/vagrant"
end

# Node 4
config.vm.define "node4" do |node4|
  node4.vm.box = "rdbreak/rhel8node"
#  node4.vm.hostname = "node4.ansi.example.com"
  node4.vm.network "private_network", ip: "192.168.55.204"
  node4.vm.synced_folder ".", "/vagrant", type: "rsync", rsync__exclude: [".git/", "*.vdi"]
  node4.vm.provider "virtualbox" do |node4|
    node4.memory = "512"

    unless File.exist?(file_to_disk4)
      node4.customize ['createhd', '--filename', file_to_disk4, '--variant', 'Fixed', '--size', 2 * 1024]
      node4.customize ['storagectl', :id, '--name', 'SATA Controller', '--add', 'sata', '--portcount', 2]
      node4.customize ['storageattach', :id,  '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', file_to_disk4]
      end
  end
  
    node4.vm.provision "shell", inline: <<-SHELL
    yes| sudo mkfs.ext4 /dev/sdb
    SHELL
    node4.vm.synced_folder ".", "/vagrant"
end

# Control Node
config.vm.define "control" do |control|
  control.vm.box = "rdbreak/rhel8node"
#  control.vm.hostname = "control.ansi.example.com"
  control.vm.network "private_network", ip: "192.168.55.200"
  control.vm.provider :virtualbox do |control|
    control.customize ['modifyvm', :id,'--memory', '2048']
    end
  control.vm.synced_folder ".", "/vagrant", type: "rsync", rsync__exclude: [".git/", "*.vdi"]
  control.vm.provision :ansible_local do |ansible|
  ansible.playbook = "/vagrant/playbooks/master.yml"
  ansible.install = false
  ansible.compatibility_mode = "2.0"
  ansible.inventory_path = "/vagrant/inventory"
  ansible.config_file = "/vagrant/ansible.cfg"
  ansible.limit = "all"
 end
end
end
