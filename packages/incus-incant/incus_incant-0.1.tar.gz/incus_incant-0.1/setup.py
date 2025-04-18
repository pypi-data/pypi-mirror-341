# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['incant']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'mako>=1.1.3,<2.0.0',
 'pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['incant = incant.cli:cli']}

setup_kwargs = {
    'name': 'incus-incant',
    'version': '0.1',
    'description': '',
    'long_description': '# Incant\n\n[![PyPI version](https://img.shields.io/pypi/v/incus-incant.svg)](https://pypi.org/project/incus-incant/)\n\nIncant is a frontend for [Incus](https://linuxcontainers.org/incus/) that provides a declarative way to define and manage development environments. It simplifies the creation, configuration, and provisioning of Incus instances using YAML-based configuration files.\n\n## Features\n\n- **Declarative Configuration**: Define your development environments using simple YAML files.\n- **Provisioning Support**: Declare and run provisioning scripts automatically.\n- **Shared Folder Support**: Mount the current working directory into the instance.\n\n## Installation\n\nEnsure you have Python installed and `incus` available on your system.\n\nYou can install Incant from PyPI:\n\n```sh\npipx install incus-incant\n```\n\nOr install directly from Git:\n\n```sh\npipx install git+https://github.com/lnussbaum/incant.git\n```\n\n## Usage\n\n## Configure Incant\n\nIncant looks for a configuration file named `incant.yaml`, `incant.yaml.j2`, or `incant.yaml.mako` in the current directory. Here is an example:\n\n```yaml\ninstances:\n  my-instance:\n    image: images:debian/12\n    vm: false # use a container, not a KVM virtual machine\n    provision:\n      - echo "Hello, World!"\n      - apt-get update && apt-get install -y curl\n```\n\nYou can also ask Incant to create an example in the current directory:\n\n```sh\n$ incant init\n```\n\n### Initialize and Start an Instance\n\n```sh\n$ incant up\n```\n\nor for a specific instance:\n\n```sh\n$ incant up my-instance\n```\n\n### Provision again an Instance that was already started previously\n\n```sh\n$ incant provision\n```\n\nor for a specific instance:\n\n```sh\n$ incant provision my-instance\n```\n\n### Use your Instances\n\nUse [Incus commands](https://linuxcontainers.org/incus/docs/main/instances/) to interact with your instances:\n\n```sh\n$ incus exec ubuntu-container -- apt-get update\n$ incus shell my-instance\n$ incus console my-instance\n$ incus file edit my-container/etc/hosts\n$ incus file delete <instance_name>/<path_to_file>\n```\n\nYour instance\'s services are directly reachable on the network. They should be discoverable in DNS if the instance supports [LLMNR](https://en.wikipedia.org/wiki/Link-Local_Multicast_Name_Resolution) or [mDNS](https://en.wikipedia.org/wiki/Multicast_DNS).\n\n### Destroy an Instance\n\n```sh\n$ incant destroy\n```\n\nor for a specific instance:\n\n```sh\n$ incant destroy my-instance\n```\n\n### View Configuration (especially useful if you use Mako or Jinja2 templates)\n\n```sh\n$ incant dump\n```\n\n## Incant compared to Vagrant\n\nIncant is inspired by Vagrant, and intended as an Incus-based replacement for Vagrant.\n\nThe main differences between Incant and Vagrant are:\n\n* Incant is Free Software (licensed under the Apache 2.0 license). Vagrant is licensed under the non-Open-Source Business Source License.\n* Incant is only a frontend for [Incus](https://linuxcontainers.org/incus/), which supports containers (LXC-based) and virtual machines (KVM-based) on Linux. It will not attempt to be a more generic frontend for other virtualization providers. Thus, Incant only works on Linux.\n\nSome technical differences are useful to keep in mind when migrating from Vagrant to Incant.\n\n* Incant is intended as a thin layer on top of Incus, and focuses on provisioning. Once the provisioning has been performed by Incant, you need to use Incus commands such as `incus shell` to work with your instances.\n* Incant shares the current directory as `/incant` inside the instance (compared to Vagrant\'s sharing of `/vagrant`). Incant tries to share the current directory read-write (using Incus\' `shift=true`) but this fails in some cases, such as restricted containers. So there are chances that the directory will only be shared read-only.\n* Incant does not create a user account inside the instance -- you need to use the root account, or create a user account during provisioning (for example, with `adduser --disabled-password --gecos "" incant`)\n* Incant uses a YAML-based description format for instances. [Mako](https://www.makotemplates.org/) or [Jinja2](https://jinja.palletsprojects.com/) templates can be used to those YAML configuration files if you need more complex processing, similar to what is available in *Vagrantfiles* (see the examples/ directory).\n\n## Incant compared to other projects\n\nThere are several other projects addressing similar problem spaces. They are shortly described here so that you can determine if Incant is the right tool for you.\n\n* [lxops](https://github.com/melato/lxops) and [blincus](https://blincus.dev/) manage the provisioning of Incus instances using a declarative configuration format, but the provisioning actions are described using  [cloud-init](https://cloud-init.io/) configuration files. [lxops](https://github.com/melato/lxops) uses [cloudconfig](https://github.com/melato/cloudconfig) to apply them, while [blincus](https://blincus.dev/) requires *cloud* instances that include cloud-init. In contrast, using Incant does not require knowing about cloud-init or fitting into cloud-init\'s formalism.\n* [terraform-provider-incus](https://github.com/lxc/terraform-provider-incus) is a [Terraform](https://www.terraform.io/) or [OpenTofu](https://opentofu.org/) provider for Incus. Incant uses a more basic scheme for provisioning, and does not require knowing about Terraform or fitting into Terraform\'s formalism.\n* [cluster-api-provider-lxc (CAPL)](https://github.com/neoaggelos/cluster-api-provider-lxc) is an infrastructure provider for Kubernetes\' Cluster API, which enables deploying Kubernetes clusters on Incus. Incant focuses on the more general use case of provisioning system containers or virtual machines outside of the Kubernetes world.\n* [devenv](https://devenv.sh/) is a [Nix](https://nixos.org/)-based development environment manager. It also uses a declarative file format. It goes further than Incant by including the definition of development tasks. It also covers defining services that run inside the environment, and generating OCI containers to deploy the environment to production. Incant focuses on providing the environment based on classical Linux distributions and tools.\n\n## License\n\nThis project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.\n\n',
    'author': 'Lucas Nussbaum',
    'author_email': 'lucas@debian.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
