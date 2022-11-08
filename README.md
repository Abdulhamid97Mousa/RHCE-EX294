# Linux Administration with Ansible Getting Started with Ansible Automation

## Managing growing linux systems

### Course Overview:
- Installing Ansible and run Ad-Hoc commands
   - 1.1 Installing Ansible-Across many systems
   - 1.2 Understanding Ansible Components
   - 1.3 Configuration of Ansible inventory
 
### Module Overview:
-  Managing systems
-  Scripting Solution
-  Building Lab System

## Lab Systems:
We're going to use the Virtual Systems:
- Red Hat Enterprise Linux 8.6
- Ubuntu 20.04
- CentOS Stream

> please take a look at the diagram below:

```mermaid
flowchart TD;
    A[Fire Up 3 VMs] --> B(#A RHEL 8.6 Controller Node);
    B -- Controlled By Node #A --> C[#B Ubuntu 20.04];
    B -- Controlled By Node #A --> D[#C CentOS Stream];
```

## SETTING UP OUR LAB:
<details><summary>SETTING UP OUR LAB</summary>

### Installing the necessary software
In order to be able to follow along you need to install the following software, remember software version is important. therefore, go to the following websites
and install the specified software only and in the same order.
   
> The **VirtualBox and Extension Pack** need to be downloaded with the same version, for example if you decided to install virtualbox 6.1 then the extension pack also need to be 6.1 version as well to avoid bugs or download failer.
   
1. Install the latest VirtualBox, Virtualization technology has many flavors, you can decide whether to use VMware Workstation, Oracle VirtualBox, and virtmanager.
   and for this course i recommend that you use VirtualBox, Please install VirtualBox and VirtualBox Extension Pack.
   
   - How to instal VirtualBox, please go to the following links to install VirtualBox and Extension Pack or you can follow the image links, starting by installing `Virtualbox graphical User Interface Version 6.1.36`, and if you're using windows make sure to choose Windows, or select MacOs if you're using MacOS, for windows users, please install [VirtualBox 6.1 (active maintenance)](https://download.virtualbox.org/virtualbox/6.1.40/VirtualBox-6.1.40-154048-Win.exe) or you can go to [https://www.virtualbox.org/wiki/Downloads](https://www.virtualbox.org/) and install newer versions at your peril.
   

   - How to instal VirtualBox Extension Pack, go to this link for installation [Oracle_VM_VirtualBox_Extension_Pack-6.1.36.vbox-extpack](https://download.virtualbox.org/virtualbox/6.1.36/Oracle_VM_VirtualBox_Extension_Pack-6.1.36-152435.vbox-extpack)
   
> After you've installed VirtualBox and Extension Pack Successfully, you need to add the Extension Pack to VirtualBox, and how to do it ? well, you need to follow the next bullet point, open it and follow along.

<details><summary>How to add the extension pack to VirtualBox</summary>

![image](https://user-images.githubusercontent.com/80536675/200651756-036369ef-0a33-401d-9c12-f401b2470522.png)

![image](https://user-images.githubusercontent.com/80536675/200651793-a756c55f-66ea-428d-b705-0f85b0cfef02.png)

![image](https://user-images.githubusercontent.com/80536675/200651827-9c41590b-e72a-4781-a33b-afd1e42af6ea.png)

![image](https://user-images.githubusercontent.com/80536675/200651872-032531a9-4744-47df-b480-82ef233f8c30.png)

![image](https://user-images.githubusercontent.com/80536675/200652048-b9e47e2c-e6ac-4c60-a9d0-a4aba0a5875a.png)

</details>


2. Install Latest version of Vagrant, Vagrant enables users to create and configure lightweight, reproducible, and portable development environments.
   - To install vagrant please go to this website https://www.vagrantup.com/downloads.html, select Windows and 64-bit or 32-bit depends on your OS
   
<details><summary>How to Install Vagrant</summary>

![image](https://user-images.githubusercontent.com/80536675/200653238-a6f6f187-9017-4b2b-b4b5-8c97daea58a5.png)

</details>


### Create the required directories in the Host OS
in order to create following directories, you need to create the following directories in the Path specified bellow.
1. Go to `C:/Users/user-name/vagrant` you need to create a directory called `vagrant` and Under the vagrant Directory create another sub-directory called `ansible`, your directory tree should be: `C:/Users/user-name/vagrant/ansible/`
2. Inside your `C:/Users/user-name/vagrant/ansible/` directory you need to install or write your own `Vagrantfile`
   - to install the Vagrantfile go to this link: [Vagrantfile](https://github.com/Abdulhamid97Mousa/RHCE_EX294_ExamPrep/blob/main/Linux%20Administration%20with%20Ansible%20Getting%20Started%20with%20Ansible%20Automation/Demo_1/Vagrantfile)

3. if you are facing trouble with these two bullet points, i've got images that could help you in creating these directories in the correct places.

<details><summary>How does Vagrantfile look like</summary>

![image](https://user-images.githubusercontent.com/80536675/200665970-9024fc15-f871-4c14-a468-74484e829035.png)

</details>

<details><summary>How to Install Vagrantfile</summary>

![image](https://user-images.githubusercontent.com/80536675/200666495-6293ef9b-182e-4739-8b69-0b864620a229.png)
![image](https://user-images.githubusercontent.com/80536675/200666520-a2d0961e-a9d1-460f-8f76-1a68ccfa991b.png)

</details>


4. After installing `Vagrantfile` please place it under the ansible directory.

<details><summary>Where to place the Vagrantfile</summary>

![image](https://user-images.githubusercontent.com/80536675/200659505-1f4ca412-efdf-4fd5-912c-26898ccd8a41.png)

</details>

</details>


## Running Vagrant and fire up our VMS:
<details><summary>Running Vagrant and fire up our VMS</summary>

In this section, we are going to use the `Powershell` or optionally use `SecureCRT 8.7` to run our script, our script is going to create VMs for us,
the VMs are being mentioned earlier in the diagram, and At this moment we don't have any VMs currently running.

</details>

<details><summary>Refer to these image for assistance:</summary>

![image](https://user-images.githubusercontent.com/80536675/200663239-1725be30-25d2-42b9-8624-9be6c1d5d118.png)
![image](https://user-images.githubusercontent.com/80536675/200661448-401aa05d-49e8-48db-9a4a-e07f6b81e6e3.png)
![image](https://user-images.githubusercontent.com/80536675/200661637-b97ea383-3402-4de1-bc59-408ececd4c82.png)

</details>

> Here we can see that we're being placed at the directory `C:\Users\pc` if you run `Powershell` as administrator, then you will be placed at this directory `C:\Windows\systems32`, being and administrator or not, it doesn't matter.

> Next, in order to run your script Vagrant file you need change your current directory `C:\Windows\systems32` to `C:\Users\user-name\vagrant\ansible\`, to do that you need to enter the following Command:
```
cd C:\Users\user-name\vagrant\ansible
```
<details><summary>Refer to this image:</summary>
 
![image](https://user-images.githubusercontent.com/80536675/200673183-437389d5-1b63-4b3a-9de2-c21d0815dbd5.png)


</details>

> to create and fire-up our VMs we just need enter the command:
```
vagrant up
```

<details><summary>Refer to this image:</summary> 

![image](https://user-images.githubusercontent.com/80536675/200664725-68905011-143e-4d05-ad13-00e948a1dc35.png)
![image](https://user-images.githubusercontent.com/80536675/200664930-b17a10c3-4765-4b2c-a9ad-81297140c56f.png)

</details>

## Registering our RedHat Enterprise Linux:

<details><summary>Registering our RedHat Enterprise Linux</summary>
In this section i'm going to use another software instead of `Powershell` called `SecureCRT`, Why would i do that?
well, working with Powershell is good but some commands won't be accessible to you and the interface is rigid in my opinion. therefore, i recommend that you install SecureCRT 8.7, to install SecureCRT 8.7 go to this link: [VanDyke_SecureCRT_and_SecureFX_8.7.2_Build_2214.rar](https://getintopc.com/softwares/file-sharing/vandyke-securecrt-and-securefx-free-download/)
> Working with Powershell or SecureCRT is almost the same.

</details>

<details><summary>After installing SecureCRT 8.7 version, open it and make sure you have an interface similar to mine</summary>

![image](https://user-images.githubusercontent.com/80536675/200668826-c367c8ea-3a0b-488b-a0f9-35143e8029e9.png)

</details>

- Next, you need to connect to your local shell.

<details><summary>Please refer to the following images for assistance</summary>

![image](https://user-images.githubusercontent.com/80536675/200668878-4c228deb-c689-4a56-a507-cddce932817e.png)
![image](https://user-images.githubusercontent.com/80536675/200669073-c7061f0c-69cf-4899-8cb4-ff8d97631c50.png)

</details>

- Go to `C:/Users/user-name/vagrant/ansible/` and enter the command: `vagrant ssh rhel8` to ssh to each of your VMs, remember VMs names are `rhel8`,`ubuntu` and `stream`, open another window and do the same for ubuntu and CentOS stream:
```
cd C:\Users\user-name\vagrant\ansible
vagrant ssh rhel8
```

<details><summary>Refer to the following images for assistance:</summary>

![image](https://user-images.githubusercontent.com/80536675/200670128-125e327b-83cc-4fc1-8e71-933031b65782.png)
![image](https://user-images.githubusercontent.com/80536675/200670681-a211ef91-1bd6-4b39-8bfd-ec0c9045808c.png)
![image](https://user-images.githubusercontent.com/80536675/200670882-0d42ffb5-af92-4441-9314-0930a8cb6701.png)

</details>



</details>
