# RHCE_EX294 Study Guide & Exam Prep
This repository is built to help you as beginner to Understand Ansible, And
walk you through RHCE_EX294 study Topics from setting up a lab to mastry in Ansible, and ensure that you're ready for the RHCE EX294 exam.
Please go to this link to set up your [Lab environment](https://github.com/Abdulhamid97Mousa/RHCE_EX294_Study_Guide/wiki/Linux-Administration-with-Ansible:-Getting-Started-with-Ansible-Automation#lab-systems)

Repository contains Study-Guide and exercises preparing for EX294 exam. the readers need to keep in mind that none of them was taken from the actual test. They were created based on the study point available at RedHat's website.

## Inspiration
Content present in the repository is inspierd by other people' sample exams, redhat training exercises and my own invention. Use links below to check them out
 - [Redhat Certified Engineer Exam Objectives](https://www.redhat.com/en/services/training/ex294-red-hat-certified-engineer-rhce-exam-red-hat-enterprise-linux-8?section=Objectives)
 - [Andrew Mallett Courses on Plural-Sight](https://app.pluralsight.com/paths/certificate/rhce-red-hat-certified-engineer-ex294)
 - [Sander van Vugt Detailed book and lab-exercises](https://www.amazon.com/RHCE-EX294-Cert-Guide-Certification/dp/0136872433)

# Part I: Introduction to Ansible

## Understanding Configuration Management

- [UNDERSTANDING AUTOMATION](#UNDERSTANDING AUTOMATION)
- [UNDERSTANDING ANSIBLE ESSENTIAL COMPONENTS](#UNDERSTANDING ANSIBLE ESSENTIAL COMPONENTS)
- [UNDERSTANDING ANSIBLE USE CASES](#UNDERSTANDING ANSIBLE USE CASES)
  


## Installing Ansible

- [UNDERSTANDING AN ANSIBLE ENVIRONMENT](#UNDERSTANDING AN ANSIBLE ENVIRONMENT)
- [UNDERSTANDING CONTROLLER HOST REQUIREMENTS](#UNDERSTANDING CONTROLLER HOST REQUIREMENTS)
- [UNDERSTANDING INSTALLATION METHODS](#UNDERSTANDING INSTALLATION METHODS)
- [CONFIGURING MANAGED HOSTS](#CONFIGURING MANAGED HOSTS)
- [CONFIGURE THE ANSIBLE USERS](#CONFIGURE THE ANSIBLE USERS)
  


### UNDERSTANDING AUTOMATION
Ansible is often referred to as a configuration
management solution. That description doesn't do
justice to all that Ansible can do. Ansible is more a
solution for automation, allowing system administrators
to take care of multiple systems in an efficient way. In
This section you learn about all that Ansible can do as an
automation tool. We also take a quick look at other
automation solutions.


<details><summary>What Is Automation?</summary>

In the years of the system administrator, companies used
servers. These servers performed a wide range of
different tasks, and to ensure that every server was doing
what it needed to be doing, a system administrator was
needed. System administrators typically had advanced
skills in managing different parts of the operating system
that ran on their servers.

Even though the years of the system administrator were
glorious, and many gurus worked in IT departments,
from a company perspective, this scenario was not ideal.
First, because system administrator skills are specific to
that person, if that person goes away, forgets about
brilliant solutions applied earlier, or just has a bad day,
things might go wrong.

Another part that was not ideal was that the system
administrator typically took care of individual servers,
and with the development of IT in recent years,
companies have gone from a handful of servers to data
centers and cloud environments with hundreds if not
thousands of servers. So a more efficient approach was
needed.

A first attempt in many sites was the use of shell scripts.
Based on the deep knowledge of many system
administrators, shell scripts can be used in a flexible way
to automate a wide range of tasks on many servers. Using
shell scripts, however, does come with some
disadvantages:
- **Shell scripts cannot be used on a wide range of
different devices that need management.**
- **It is difficult to write shell scripts in a way that will
always produce the same result in every situation.**

Because of these differences, and also because of changes
in the way companies consume IT, a new approach was
needed.

</details>

<details><summary>Understanding the DevOps Way of Working?</summary>

Throughout the years the way IT is consumed has
changed. In the past, IT was used to provide great
services to end users who just had to deal with them.
Now the landscape has changed to an environment in
which IT is everywhere, and multiple applications can provide a solution to the same IT problem. The years of
the system administrator slowly came to an end, and the
system administrator’s role needed to come closer to that
of the developers.

In this new way of working, the developers take care of
building applications, and system administrators take
care of implementing the code as a working application.
Because this change required a deep cooperation
between the developer and the system administrator, a
new role was created: the role of the DevOps. The term
DevOps is a contraction of developer and operator. In
this role, tasks performed by the developer and the
system administrator come together. A common
definition of DevOps is **“a set of practices intended to
reduce the time between committing a change to a
system and the change being placed into normal
production, while ensuring high quality”** (Len Bass, Ingo
Weber, and Liming Zhu, **DevOps: A Software Architect’s
Perspective**, Boston, MA: Addison-Wesley Professional,
2015).

With this new role, the “DevOps way of working” was
introduced. The exact definition is not always the same,
but in general, it comes down to managing the entire
application life cycle, which consists of the following
elements:
- **Coding:** Developing and reviewing application
source code
- **Building:** Using continuous integration to include
changes in the source code and convert to a working
application
- **Testing:** Using a toolchain that takes care of testing
the application and making sure that feedback is
provided on business risks, if there are any
- **Packaging:** Delivering the code to its end users by
bundling it into packages and offering these
packages in a repository
- **Releasing:** Approving, managing, and automating
new software releases
- **Configuring:** Managing the infrastructure to
support the new code
- **Monitoring:** Keeping an eye on application
performance and the way it is experienced by the
end users

To manage these different elements in the application
life cycle, new tools were introduced. Ansible is one of
these tools, with a strong focus on managing the
configuration of the managed environment according to
the infrastructure as code approach.

Some categories in the DevOps approach are more
important than others. The most important elements are
continuous integration, with solutions such as Jenkins
and GitLab, but also OpenShift and even Ansible. The
other main component is infrastructure as code, where
Ansible, Puppet, and Terraform are important solutions.
</details>

<details><summary>What is Infrastructure as Code?</summary>
  
The essence in infrastructure as code is that machinereadable
code (the automation language) is used to
describe the state the managed IT infrastructure needs to
be in. This is referred to as the desired state. This code is
next applied to the infrastructure to ensure that it
actually is in that state.

In this approach, the machine-readable code files, which
basically are simple text files, should be managed like
software code, using a version control system, or
Concurrent Version System (CVS). That means the tools
that are common to the developer are implemented to manage
the infrastructure as code. Commonly, Git
repositories are used for this purpose.

Putting these files in a CVS makes managing it easy. This
approach provides some benefits, such as easy
management of change history, upgrades, and rollback.
Infrastructure as code is the place where the developer
meets the operator in DevOps. Developers can easily
review changes, and operators can ensure that the
systems are in the state that developers expect.
</details>

<details><summary>Are there other Automation Solutions</summary>
To provide automation of configuration management,
Ansible is one of the most common solutions. Even if it
seems to be currently the most-used configuration
management solution, it’s not the only one. Other
common solutions include Puppet, Chef, and SaltStack.

Like Ansible, Puppet is one of the most important
automation solutions. There are a few reasons why
Ansible is taking over market share from Puppet though.
One of the reasons is YAML. Ansible configurations are
written in YAML, which is an easy-to-use and easy-tounderstand
language. Puppet uses its own language,
which is just not as easy. Another major difference is that
Ansible uses a push approach, where configurations are
sent from the controller node to the managed nodes.
Puppet uses a pull approach as its main strategy, where
managed nodes use an agent to connect to the Puppet
master to fetch their desired state.

Chef is built as a client/server solution, where the server
parts run on the master machine and the client parts are
implemented as an agent on the managed machines.
Chef provides its configuration in Ruby DSL, whereas
Ansible uses playbooks written in YAML. As a result,
Ansible is easier to learn because YAML is a much more
accessible data format.

SaltStack is another important alternative to Ansible.
The main difference between Ansible and SaltStack is the
performance. SaltStack uses the ZeroMQ message queue
to realize communication between the SaltStack minions
and the master, and that seems to be faster. SaltStack
uses configurations that are written in Jinja2 and use an
agent, which makes the learning curve to get started with
SaltStack also more complex.
</details>

### UNDERSTANDING ANSIBLE ESSENTIAL COMPONENTS
Now that you know a bit about Ansible and how it works,
let’s look at the different components used in Ansible. In
this section you learn about the role of Python, the
Ansible architecture, the Ansible Tower management
platform, and how to manage systems the Ansible way.
<br>

<details><summary>Ansible Is Python</summary>
There are many programming and scripting languages in
use in IT. In open source, the last few decades have seen
the rise of the Python scripting language. Python has
become the foundation of different solutions, such as
Ansible and OpenStack. The reason is that Python is
relatively easy to learn. The focus in Python is on
readability of code, while at the same time Python makes
it possible to do things in an easy way.

Ansible is written in Python, and most components that
are used in Ansible are written in Python as well. The
default Ansible version that is installed on Red Hat
Enterprise Linux 7 is based on Python 2.7; the Ansible
release that is used in RHEL 8 is based on Python 3.6.
There is no direct relation between an Ansible version
and a Python version. Recent versions of Ansible can call
either Python 2.x or Python 3.x scripts, but Python 3.x is
the better option nowadays because Python 2 is past its
end of support life.

The fact that Ansible is written in Python makes it easier
to integrate Ansible with custom scripts because Python
is a very common and widely known scripting language.
This doesn’t mean you have to know Python to work with
Ansible though. It’s true that if you understand the
workings of Python it’s easier to explain specific behavior
in Ansible, but it’s perfectly possible to be an expert in
Ansible without even knowing how to write a Hello
World script in Python.
</details>

<details><summary>Ansible Architecture</summary>
There are two main node roles in Ansible. The controller
node is the node that runs the Ansible software and from
which the operator issues Ansible commands. The
controller node can be a server running Linux, an
operator laptop, or a system running Ansible Tower. The
only requirement is that the controller node needs to be
Linux.

From the controller node, the managed nodes are
addressed. On the controller node, an inventory is
maintained to know which managed nodes are available.
Ansible doesn’t require the use of any agents. That
means it can reach out to managed nodes without a need
to install anything. To do so, Ansible uses native remote
access solutions that are provided by the managed node.
On Linux, remote access is realized by using SSH; on
Windows, it is realized by using Windows Remote
Management (WinRM); and on network devices, it can
be provided by using SSH or API access.

To configure the managed nodes, Ansible uses
playbooks. A playbook is written in YAML and contains
one or more plays. Each play consists of one or more
tasks that are executed on the managed nodes.

To implement the tasks, Ansible uses modules. Modules
are the pieces of code that do the actual work on the
managed nodes, and many modules are available—more than 3,000 already,
and the number is increasing.
Ansible also provides plug-ins. Ansible plug-ins are used
to extend Ansible functionality with additional features.

Ansible playbooks should be developed to be
idempotent. That means a playbook will always produce
the same results, even if it is started multiple times on
the same node. As a part of the idempotency, playbooks
should also be self-containing and not depend on any
other playbooks to be successful.
</details>
<details><summary>Understanding Ansible Tower</summary>
Ansible can be used in two different ways: Ansible
Engine or Ansible Tower. Ansible Engine is the
command-line version of Ansible, where modules and
plug-ins are used to offer Ansible functionality. Ansible
Engine is the solution of choice for people who like to
work from the command line in a medium- to mid-sized
environment.

Apart from Ansible Engine, there is Ansible Tower,
which is based on the AWX open-source solution. It
provides a web-based interface to manage Ansible.
Ansible Tower adds different features to Ansible Engine,
such as

- **Web management interface**
- **Role-based access control**
- **Job scheduling**
- **Enhanced security**
- **Centralized logging**

Because the RHCE EX294 exam is about Ansible Engine,
you won’t find much information about Ansible Tower in
this book.
</details>

<details><summary> Understanding the Ansible Way </summary>
While working with Ansible, you need to make choices
on how to approach specific tasks. In many cases, many
solutions are available. If, however, you choose to work
the Ansible way, making the right solution becomes a lot
easier. The Ansible way is focused around the following
rules:

- **Keep it simple:** At its launch, Ansible was
positioned as a solution that is simpler than the
others. That goes for the playbooks and other
solutions you’ll develop as well. Keep it simple, and
it will be easier for others to understand what you
had in mind.
- **Make it readable:** As with anything in IT, you can
make it very complex and use compact structures to
ensure that nobody understands what you were
trying to do. That approach doesn’t make sense. You
should keep it readable, and that starts with your
development of Ansible playbooks.
- **Use a declarative approach:** In Ansible, it’s all
about the desired state. The purpose of Ansible is to
bring managed assets in the desired state,
regardless of the current state, and make only the
modifications that are necessary. The desired state
is implemented in playbooks, and using playbooks
to make the current state match the desired state is
what is known as the declarative approach.
- **Use specific solutions:** On many occasions, you’ll
find that multiple solutions are available to reach a
specific desired state. For instance, you can use the
command module to run arbitrary commands,
making it possible to accomplish almost anything.
You shouldn’t, though. To make sure that you get
the desired result, use the most specific solution. So
if, for instance, a user module allows you to create
users, use that module and don’t use the Linux
useradd command with the command module.
</details>

### UNDERSTANDING ANSIBLE USE CASES
The core of Ansible is configuration management. The
Ansible modules and plug-ins cover a wide range of
functions, which means that Ansible can be used for
configuration management and beyond. Here are some
common use cases.

<details><summary>Using Ansible for Configuration
Management</summary>
Many people know Ansible only as a configuration
management solution, and there’s a reason for that.
Ansible started as a solution for configuration
management, and that is what it still is used for in most
cases. In configuration management, Ansible is used to
manage configuration files, install software, create users,
and perform similar tasks to guarantee that the managed
systems all are in the desired state.
</details>

<details><summary>Using Ansible for Provisioning</summary>
Another common scenario for use of Ansible is for
deploying and installing systems (provisioning).
Provisioning is particularly common in virtual and cloud
environments, where in the end a new machine is just a
configuration file that needs to be pushed to the
managed machine and started from there. Ansible does
not offer the functionality to PXE-boot and kickstart a
bare-metal server but is used in combination with
solutions that can take care of that as well. While
exploring the different modules that are available, you’ll
notice that a wide range of modules is provided to work
with Ansible in different cloud environments.
</details>
<details><summary>Using Ansible for Provisioning</summary>
Another common scenario for use of Ansible is for
deploying and installing systems (provisioning).
Provisioning is particularly common in virtual and cloud
environments, where in the end a new machine is just a
configuration file that needs to be pushed to the
managed machine and started from there. Ansible does
not offer the functionality to PXE-boot and kickstart a
bare-metal server but is used in combination with
solutions that can take care of that as well. While
exploring the different modules that are available, you’ll
notice that a wide range of modules is provided to work
with Ansible in different cloud environments.
</details>

<details><summary>Using Ansible for Continuous Delivery</summary>
Continuous integration/continuous delivery (CI/CD)
makes sure that source code can easily be developed and
updated, and the results are easily provisioned as a new
version of an application. Ansible cannot take care of the
entire CI/CD procedure itself, but Ansible playbooks can
play an important role in the CD part of the CI/CD
pipeline.
</details>

