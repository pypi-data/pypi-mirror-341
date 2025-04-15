import subprocess
import time
from pathlib import Path

import paramiko
import requests

from .utils import get_device_id


def manage_ssh_config(action, host=None, config_data=None, config_path=None):
    """Manage SSH config file."""
    config_path = Path(config_path or Path.home() / ".ssh" / "config")
    config_backup_path = config_path.with_suffix(".backup")
    if not config_backup_path.exists():
        config_backup_path.write_text(config_path.read_text())

    ssh_config = paramiko.SSHConfig()
    if config_path.exists():
        ssh_config.parse(config_path.open())

    if action == "add" and host and config_data:
        ssh_config._config = [
            e for e in ssh_config._config if host not in e.get("host", [])
        ]
        entry = {"host": [host], "config": {}}
        for k, v in config_data.items():
            entry["config"][k] = [v]
        ssh_config._config.append(entry)
    elif action == "delete" and host:
        ssh_config._config = [
            e for e in ssh_config._config if host not in e.get("host", [])
        ]

    if action in ["add", "delete"]:
        lines = []
        seen_hosts = set()

        for entry in ssh_config._config:
            hosts = " ".join(entry.get("host", []))

            if any(h in seen_hosts for h in entry.get("host", [])):
                continue

            lines.append(f"Host {hosts}")
            for h in entry.get("host", []):
                seen_hosts.add(h)

            for k, v in entry["config"].items():
                if k != "host" and v:
                    value = v[0] if isinstance(v, list) and v else v
                    lines.append(f"    {k} {value}")
            lines.append("")

        config_path.write_text("\n".join(lines))
    return ssh_config


def run_remote_python(host, ssh_key_path, script, username="root"):
    """Run a Python script on a remote server using a temporary file.

    Args:
        host: Remote hostname or IP
        ssh_key_path: Path to private key file
        script: Python code to execute (multi-line string)
        username: Remote username (default: "root")

    Returns:
        stdout and stderr as strings
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(
        hostname=host,
        username=username,
        key_filename=str(ssh_key_path),
    )

    sftp = client.open_sftp()

    try:
        remote_path = "/tmp/remote_script_temp.py"
        with sftp.open(remote_path, "w") as f:
            f.write(script)

        _, stdout, stderr = client.exec_command(f"python3 {remote_path}")

        print(stdout.read().decode())
        print(stderr.read().decode())
        client.exec_command(f"rm {remote_path}")
    finally:
        sftp.close()
        client.close()


class DigitalOcean:
    """DigitalOcean API client."""

    def __init__(self, api_key=None):
        """Initialize the DigitalOcean API client."""
        from nates import env

        api_key = api_key or env.DIGITAL_OCEAN_API_KEY
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self.base_url = "https://api.digitalocean.com/v2"

    def get(self, endpoint):
        """Send a GET request to the DigitalOcean API."""
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def post(self, endpoint, data):
        """Send a POST request to the DigitalOcean API."""
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def put(self, endpoint, data):
        """Send a PUT request to the DigitalOcean API."""
        url = f"{self.base_url}/{endpoint}"
        response = requests.put(url, headers=self.headers, json=data)
        return response.json()

    @property
    def projects(self):
        """Get all projects."""
        return {p["name"]: p for p in self.get("projects")["projects"]}

    @property
    def droplets(self):
        """Get all droplets."""
        return {d["name"]: d for d in self.get("droplets")["droplets"]}

    @property
    def ssh_keys(self):
        """Get all SSH keys."""
        return {k["name"]: k for k in self.get("account/keys")["ssh_keys"]}

    @property
    def firewalls(self):
        """Get all firewalls."""
        return {f["name"]: f for f in self.get("firewalls")["firewalls"]}

    @property
    def device_ssh_key_path(self):
        """Get the path to the device's SSH key."""
        do_ssh_name = f"do-{get_device_id()}"
        do_ssh_path = Path.home() / ".ssh" / do_ssh_name
        if not do_ssh_path.exists():
            subprocess.run(
                [
                    "ssh-keygen",
                    "-C",
                    f"do-{get_device_id()}",
                    "-f",
                    do_ssh_path,
                    "-N",
                    "",
                ]
            )
        return do_ssh_path

    def get_device_ssh_key(self):
        """Get the device's SSH key on DigitalOcean."""
        ssh_key = self.ssh_keys.get(self.device_ssh_key_path.name)
        if not ssh_key:
            public_key = self.device_ssh_key_path.with_suffix(".pub").read_text()
            self.post(
                "account/keys",
                {
                    "name": self.device_ssh_key_path.name,
                    "public_key": public_key,
                },
            )
            time.sleep(10)
            ssh_key = self.ssh_keys.get(self.device_ssh_key_path.name)
        return ssh_key

    def assign_droplet_to_project(self, droplet_name, project_name):
        """Assign a droplet to a specific project."""
        project_id = self.projects[project_name]["id"]
        droplet_id = self.droplets[droplet_name]["id"]

        self.post(
            f"projects/{project_id}/resources",
            {"resources": [f"do:droplet:{droplet_id}"]},
        )

    def create_droplet(
        self,
        name,
        project_name,
        region="nyc3",
        size="s-4vcpu-8gb",
        image="ubuntu-24-10-x64",
        ipv6=True,
        ssh_keys=None,
    ):
        """Create a new droplet."""
        if self.droplets.get(name):
            print(f"droplet {name} already exists")
            return
        payload = {
            "name": name,
            "region": region,
            "size": size,
            "image": image,
            "ipv6": ipv6,
            "with_droplet_agent": True,
            "monitoring": True,
        }
        if ssh_keys:
            payload["ssh_keys"] = [self.ssh_keys[k]["id"] for k in ssh_keys]

        self.post("droplets", payload)

        while 1:
            print("waiting for droplet to be active")
            droplet = self.droplets.get(name)
            if droplet and droplet["status"] == "active":
                break
            time.sleep(3)

        self.assign_droplet_to_project(name, project_name)
        print(f"droplet {name} created and assigned to project {project_name}")

    def get_reserved_ip(self, droplet_name):
        """Get or create a reserved IP for a droplet."""
        droplet = self.droplets[droplet_name]
        if len(droplet["networks"]["v4"]) < 3:
            self.post(
                "reserved_ips",
                {
                    "droplet_id": droplet["id"],
                },
            )["reserved_ip"]["ip"]
            time.sleep(15)
            droplet = self.droplets[droplet_name]
        return droplet["networks"]["v4"][-1]["ip_address"]

    def get_firewall(self, name, droplet_name=None, whitelisted_ips=None, update=False):
        """Get or create/update a firewall."""
        firewall = self.firewalls.get(name)
        droplet_name = droplet_name or name

        if not firewall or update:

            def create_firewall_rule(
                ports, droplet_ids=None, ips=None, protocol="tcp", inbound=True
            ):
                location = "sources" if inbound else "destinations"
                rule = {"protocol": protocol, "ports": str(ports), location: {}}
                if droplet_ids:
                    rule[location]["droplet_ids"] = droplet_ids
                if ips:
                    rule[location]["addresses"] = ips
                return rule

            droplet_id = self.droplets[droplet_name]["id"]

            inbound_rules = [
                create_firewall_rule("22", ips=whitelisted_ips),
                create_firewall_rule("80", ips=["0.0.0.0/0", "::/0"]),
                create_firewall_rule("443", ips=["0.0.0.0/0", "::/0"]),
                create_firewall_rule(
                    "5432", ips=whitelisted_ips, droplet_ids=[droplet_id]
                ),
                create_firewall_rule(
                    "6379", ips=whitelisted_ips, droplet_ids=[droplet_id]
                ),
                create_firewall_rule(
                    "9200", ips=whitelisted_ips, droplet_ids=[droplet_id]
                ),
            ]

            outbound_rules = [
                create_firewall_rule(
                    "0", ips=["0.0.0.0/0", "::/0"], protocol="icmp", inbound=False
                ),
                create_firewall_rule(
                    "0", ips=["0.0.0.0/0", "::/0"], protocol="tcp", inbound=False
                ),
                create_firewall_rule(
                    "0", ips=["0.0.0.0/0", "::/0"], protocol="udp", inbound=False
                ),
            ]

            payload = {
                "name": name,
                "droplet_ids": [droplet_id],
                "inbound_rules": inbound_rules,
                "outbound_rules": outbound_rules,
            }

            if update and firewall:
                firewall = self.put(f"firewalls/{firewall['id']}", payload)
            else:
                firewall = self.post("firewalls", payload)
        return firewall

    def run_python(self, droplet_name, script):
        """Run a Python script on a droplet via SSH."""
        host = self.get_reserved_ip(droplet_name)
        run_remote_python(host, self.device_ssh_key_path, script)

    def setup(
        self,
        droplet_name,
        project_name,
        ssh_keys=None,
        whitelisted_ips=None,
        droplet_args=None,
    ):
        """Setup a new droplet."""
        from nates import env

        print("Setting up device SSH key for DigitalOcean")
        self.get_device_ssh_key()

        if ssh_keys is None:
            ssh_keys = [x["name"] for x in self.ssh_keys.values()]

        if whitelisted_ips is None:
            whitelisted_ips = [ip.strip() for ip in env.WHITELISTED_IPS.split(",")]

        print("Creating droplet")
        droplet_args = droplet_args or {}
        self.create_droplet(
            droplet_name,
            project_name,
            ssh_keys=ssh_keys,
            **droplet_args,
        )

        print("Assigning reserved IP")
        reserved_ip = self.get_reserved_ip(droplet_name)

        print("Creating firewall")
        self.get_firewall(droplet_name, whitelisted_ips=whitelisted_ips, update=True)

        print("Adding local SSH config")
        manage_ssh_config("delete", droplet_name)
        manage_ssh_config(
            "add",
            droplet_name,
            {
                "hostname": reserved_ip,
                "user": "root",
                "identityfile": str(self.device_ssh_key_path.absolute()),
                "ForwardAgent": "yes",
            },
        )

        print("Running initial install script")
        script = """
import os
import getpass

os.system("sudo apt update")
os.system("sudo apt install unattended-upgrades")
os.system("sudo systemctl status unattended-upgrades.service")

username = getpass.getuser()

os.system("sudo apt install apt-transport-https ca-certificates curl software-properties-common -y")
os.system("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -")
os.system('echo "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null')
os.system("sudo apt update -y")
os.system("sudo apt install docker-ce docker-ce-cli containerd.io -y")
os.system("sudo docker --version")
os.system(f"sudo usermod -aG docker {username}")

print("Installation complete. Log out and log back in for docker group membership to take effect.")
        """  # noqa: E501
        self.run_python(droplet_name, script)
