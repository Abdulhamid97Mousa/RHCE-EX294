# RHCE_EX294

# FOUNDATION TOPICS
## UNDERSTANDING AUTOMATION
Ansible is often referred to as a configuration
management solution. That description doesn't do
justice to all that Ansible can do. Ansible is more a
solution for automation, allowing system administrators
to take care of multiple systems in an efficient way. In
This section you learn about all that Ansible can do as an
automation tool. We also take a quick look at other
automation solutions.


<details><summary>What Is Automation?</summary>

## What Is Automation?
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


## Understanding the DevOps Way of Working?
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

