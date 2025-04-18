import os
import sys
import time
import textwrap
from pathlib import Path
import click
import yaml
from jinja2 import Environment, FileSystemLoader
from mako.template import Template
from incant.incus_cli import IncusCLI

# click output styles
CLICK_STYLE = {
    "success": {"fg": "green", "bold": True},
    "info": {"fg": "cyan"},
    "warning": {"fg": "yellow"},
    "error": {"fg": "red"},
}


class Incant:
    def __init__(self, **kwargs):
        self.verbose = kwargs.get("verbose", False)
        self.config = kwargs.get("config", None)
        self.quiet = kwargs.get("quiet", False)
        self.no_config = kwargs.get("no_config", False)
        if self.no_config:
            self.config_data = None
        else:
            self.config_data = self.load_config()

    def find_config_file(self):
        config_paths = [
            (
                Path(self.config) if self.config else None
            ),  # First, check if a config is passed directly
            *(
                Path(os.getcwd()) / f"incant{ext}"
                for ext in [
                    ".yaml",
                    ".yaml.j2",
                    ".yaml.mako",
                ]
            ),
            *(
                Path(os.getcwd()) / f".incant{ext}"
                for ext in [
                    ".yaml",
                    ".yaml.j2",
                    ".yaml.mako",
                ]
            ),
        ]
        for path in filter(None, config_paths):
            if path.is_file():
                if self.verbose:
                    click.secho(f"Config found at: {path}", **CLICK_STYLE["success"])
                return path
        # If no config is found, return None
        return None

    def load_config(self):
        try:
            # Find the config file first
            config_file = self.find_config_file()

            if config_file is None:
                if not self.quiet:
                    click.secho("No config file found to load.", **CLICK_STYLE["error"])
                return None

            # Read the config file content
            with open(config_file, "r", encoding="utf-8") as file:
                content = file.read()

            # If the config file ends with .yaml.j2, use Jinja2
            if config_file.suffix == ".j2":
                if self.verbose:
                    click.secho("Using Jinja2 template processing...", **CLICK_STYLE["info"])
                env = Environment(loader=FileSystemLoader(os.getcwd()))
                template = env.from_string(content)
                content = template.render()

            # If the config file ends with .yaml.mako, use Mako
            elif config_file.suffix == ".mako":
                if self.verbose:
                    click.secho("Using Mako template processing...", **CLICK_STYLE["info"])
                template = Template(content)
                content = template.render()

            # Load the YAML data from the processed content
            config_data = yaml.safe_load(content)

            if self.verbose:
                click.secho(
                    f"Config loaded successfully from {config_file}",
                    **CLICK_STYLE["success"],
                )
            return config_data
        except yaml.YAMLError as e:
            click.secho(f"Error parsing YAML file: {e}", **CLICK_STYLE["error"])
            return None
        except FileNotFoundError:
            click.secho(f"Config file not found: {config_file}", **CLICK_STYLE["error"])
            sys.exit(1)

    def dump_config(self):
        if not self.config_data:
            sys.exit(1)
        try:
            yaml.dump(self.config_data, sys.stdout, default_flow_style=False, sort_keys=False)
        except Exception as e:
            click.secho(f"Error dumping configuration: {e}", **CLICK_STYLE["error"])

    def check_config(self):
        if not self.config_data:
            sys.exit(1)
        if "instances" not in self.config_data:
            click.secho("No instances found in config.", **CLICK_STYLE["error"])
            sys.exit(1)

    def up(self, name=None):
        self.check_config()

        incus = IncusCLI()

        # If a name is provided, check if the instance exists in the config
        if name and name not in self.config_data["instances"]:
            click.secho(f"Instance '{name}' not found in config.", **CLICK_STYLE["error"])
            return

        # Step 1 -- Create instances (we do this for all instances so that they can boot in parallel)
        # Loop through all instances, but skip those that don't match the provided name (if any)
        for instance_name, instance_data in self.config_data["instances"].items():
            # If a name is provided, only process the matching instance
            if name and instance_name != name:
                continue

            # Process the instance
            image = instance_data.get("image")
            if not image:
                click.secho(f"Skipping {instance_name}: No image defined.", **CLICK_STYLE["error"])
                continue

            vm = instance_data.get("vm", False)
            profiles = instance_data.get("profiles", None)
            config = instance_data.get("config", None)
            devices = instance_data.get("devices", None)
            network = instance_data.get("network", None)
            instance_type = instance_data.get("type", None)

            click.secho(
                f"Creating instance {instance_name} with image {image}...",
                **CLICK_STYLE["success"],
            )
            incus.create_instance(
                instance_name,
                image,
                profiles=profiles,
                vm=vm,
                config=config,
                devices=devices,
                network=network,
                instance_type=instance_type,
            )

        # Step 2 -- Create shared folder and provision
        # Loop through all instances, but skip those that don't match the provided name (if any)
        for instance_name, instance_data in self.config_data["instances"].items():
            # If a name is provided, only process the matching instance
            if name and instance_name != name:
                continue

            # Wait for the agent to become ready before sharing the current directory
            while True:
                if incus.is_agent_running(instance_name) and incus.is_agent_usable(instance_name):
                    break
                time.sleep(0.3)
            click.secho(
                f"Sharing current directory to {instance_name}:/incant ...",
                **CLICK_STYLE["success"],
            )

            # Wait for the instance to become ready if specified in config, or
            # we want to perform provisioning, or the instance is a VM (for some
            # reason the VM needs to be running before creating the shared folder)
            if (
                instance_data.get("wait", False)
                or instance_data.get("provision", False)
                or instance_data.get("vm", False)
            ):
                click.secho(
                    f"Waiting for {instance_name} to become ready...",
                    **CLICK_STYLE["info"],
                )
                while True:
                    if incus.is_instance_ready(instance_name, True):
                        click.secho(
                            f"Instance {instance_name} is ready.",
                            **CLICK_STYLE["success"],
                        )
                        break
                    time.sleep(1)

            incus.create_shared_folder(instance_name)

            if instance_data.get("provision", False):
                # Automatically run provisioning after instance creation
                self.provision(instance_name)

    def provision(self, name: str = None):
        self.check_config()

        incus = IncusCLI()

        if name:
            # If a specific instance name is provided, check if it exists
            if name not in self.config_data["instances"]:
                click.echo(f"Instance '{name}' not found in config.")
                return
            instances_to_provision = {name: self.config_data["instances"][name]}
        else:
            # If no name is provided, provision all instances
            instances_to_provision = self.config_data["instances"]

        for instance_name, instance_data in instances_to_provision.items():
            provisions = instance_data.get("provision", [])

            if not provisions:
                click.secho(f"No provisioning found for {instance_name}.", **CLICK_STYLE["info"])
                continue

            click.secho(f"Provisioning instance {instance_name}...", **CLICK_STYLE["success"])

            # Handle provisioning steps
            if isinstance(provisions, str):
                incus.provision(instance_name, provisions)
            elif isinstance(provisions, list):
                for step in provisions:
                    click.secho("Running provisioning step ...", **CLICK_STYLE["info"])
                    incus.provision(instance_name, step)

    def destroy(self, name=None):
        self.check_config()

        incus = IncusCLI()

        # If a name is provided, check if the instance exists in the config
        if name and name not in self.config_data["instances"]:
            click.secho(f"Instance '{name}' not found in config.", **CLICK_STYLE["error"])
            return

        for instance_name, _instance_data in self.config_data["instances"].items():
            # If a name is provided, only process the matching instance
            if name and instance_name != name:
                continue

            # Check if the instance exists before deleting
            if not incus.is_instance(instance_name):
                click.secho(f"Instance '{instance_name}' does not exist.", **CLICK_STYLE["info"])
                continue

            click.secho(f"Destroying instance {instance_name} ...", **CLICK_STYLE["success"])
            incus.destroy_instance(instance_name)

    def list_instances(self):
        """List all instances defined in the configuration."""
        self.check_config()

        for instance_name in self.config_data["instances"]:
            click.echo(f"{instance_name}")

    def incant_init(self):
        example_config = textwrap.dedent(
            """\
            instances:
              client:
                image: images:ubuntu/24.04
                provision: |
                  #!/bin/bash
                  set -xe
                  apt-get update
                  apt-get -y install curl
              webserver:
                image: images:debian/13
                vm: true # KVM virtual machine, not container
                # Let's use a more complex provisionning here.
                devices:
                  root:
                    size: 20GB # set size of root device to 20GB
                config: # incus config options
                  limits.processes: 100
                type: c2-m2 # 2 CPUs, 2 GB of RAM
                provision:
                  # first, a single command
                  - apt-get update && apt-get -y install ruby
                  # then, a script. the path can be relative to the current dir,
                  # as incant will 'cd' to /incant
                  # - examples/provision/web_server.rb # disabled to provide a working example
                  # then a multi-line snippet that will be copied as a temporary file
                  - |
                    #!/bin/bash
                    set -xe
                    echo Done!
        """
        )

        config_path = "incant.yaml"

        if os.path.exists(config_path):
            print(f"{config_path} already exists. Aborting.")
            sys.exit(1)

        with open(config_path, "w") as f:
            f.write(example_config)

        print(f"Example configuration written to {config_path}")
