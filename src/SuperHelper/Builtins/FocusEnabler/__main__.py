import ctypes
import io
import itertools
import os
import re
import subprocess
import sys
import typing
import logging
from pathlib import Path

import click

from SuperHelper.Core.Config import load_module_config, save_module_config

__name__ = "SuperHelper.Builtins.FocusEnabler"
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.NullHandler())

config: typing.Dict


def get_input_prompt(title):
    """Get prompt for input() function"""
    return f"{title} \u2192 "


def is_domain_valid(domain):
    """Check if the domain contains valid syntax."""
    return True if re.match(
        r"^(([a-zA-Z])|([a-zA-Z][a-zA-Z])|([a-zA-Z][0-9])|([0-9][a-zA-Z])"
        r"|([a-zA-Z0-9][a-zA-Z0-9-_]{1,61}[a-zA-Z0-9]))\.([a-zA-Z]{2,6}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z]{2,3})$",
        domain
    ) else False


def get_host_path() -> str:
    if sys.platform == "win32":
        return Path(os.getenv("WINDIR")) / "System32" / "Driver" / "etc" / "hosts"
    else:
        return Path("/etc") / "hosts"


def initialise_config_dict() -> None:
    """Initialise a new config dictionary and write to file."""
    global config
    config = {
        "BL_SECTION_START": "# Added by FocusEnabler, do not modify!",
        "BL_SECTION_END": "# End of section FocusEnabler",
        "BL_DOMAINS": [],
        "PATH_HOST": str(get_host_path()),
    }


def is_root():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin()


@click.group("focus")
def main():
    """FocusEnabler is a program that enables your focus by blocking websites."""
    # Load config for this module
    global config
    config = load_module_config(__name__)
    if len(config.keys()) == 0:
        initialise_config_dict()
        save_module_config(__name__, config)


@main.command("add")
@click.option("-c", "--clear", is_flag=True, help="(Optionally) Remove all blacklisted domains (same as 'remove')")
@click.argument("domains", nargs=-1, required=True)
def add_domain(clear, domains):
    """Add DOMAINS to blacklist."""
    if is_root():
        logging.warning("Please do not run this command as 'root'")
        sys.exit(1)
    if clear:
        with io.StringIO() as sio:
            remove_domain_internal(False, ".", sio)
    add_domain_internal(domains)
    save_module_config(__name__, config)


@main.command("list")
def list_domain():
    """List blacklisted domains"""
    if is_root():
        logging.warning("Please do not run this command as 'root'")
        sys.exit(1)
    if len(config["BL_DOMAINS"]) == 0:
        click.echo("No blacklisted domains found")
        exit(0)
    click.echo("All blacklisted domains:")
    for domain, count in zip(config["BL_DOMAINS"], itertools.count()):
        click.echo(f"({count + 1}) {domain}")
    save_module_config(__name__, config)


@main.command("remove")
@click.option("-c", "--confirm", is_flag=True, help="Ask before removing each domain")
@click.argument("domains", nargs=-1, required=True)
def remove_domain(confirm, domains):
    """Remove DOMAINS from blacklist"""
    if is_root():
        logging.warning("Please do not run this command as 'root'")
        sys.exit(1)
    remove_domain_internal(confirm, domains, sys.stdout)
    save_module_config(__name__, config)


@main.command("activate")
def activate_app():
    """Activate FocusEnabler."""
    if not is_root():
        logging.warning("Please run this command as 'root'")
        sys.exit(1)
    if not os.access(config["PATH_HOST"], os.W_OK):
        logging.warning("Hosts file is inaccessible!")
        sys.exit(1)
    with open(config["PATH_HOST"]) as fp:
        if config["BL_SECTION_START"] in fp.read():
            logging.warning("FocusEnabler is already activated! Deactivate first.")
            exit(1)
    entries: typing.List[str] = [config["BL_SECTION_START"]]
    for domain in config["BL_DOMAINS"]:
        logging.info(f"Adding entry {domain}", "Done")
        entries.append(f"127.0.0.1   {domain}")
        entries.append(f"127.0.0.1   www.{domain}")
    entries.append(config["BL_SECTION_END"])
    try:
        with open(config["PATH_HOST"], "a") as fp:
            fp.write("\n".join(entries))
        click.echo("Written to host file!")
        flush_dns()
        click.echo("FocusEnabler is enabled!")
        exit(0)
    except OSError:
        logger.exception("Unable to write to host file")
        exit(1)
    save_module_config(__name__, config)


@main.command("deactivate")
def deactivate_app():
    """Deactivate FocusEnabler"""
    if not is_root():
        logging.warning("Please run this command as 'root'")
        sys.exit(1)
    if not os.access(config["PATH_HOST"], os.W_OK):
        logging.warning("Hosts file is inaccessible!")
        sys.exit(1)
    content = None
    try:
        with open(config["PATH_HOST"]) as fp:
            content = fp.read()
            original_content_len = len(content)
        content = re.sub(rf"{config['BL_SECTION_START']}(.|[\n\r\t])*{config['BL_SECTION_END']}", "", content)
        if len(content) == original_content_len:
            logging.warning("FocusEnabler is not activated! Activate first")
            save_module_config(__name__, config)
            exit(1)
    except OSError:
        logging.exception("Unable to read host file")
        save_module_config(__name__, config)
        exit(1)
    try:
        with open(config["PATH_HOST"], "w") as fp:
            fp.write(content)
        click.echo("FocusEnabler is disabled!")
    except OSError:
        logger.exception("Writing to host file", "Failed", content_colour="red", fp=sys.stderr)
    save_module_config(__name__, config)


def flush_dns():
    """Flush DNS cache on machine."""
    def flush_dns_win32():
        """Flush DNS on Windows."""
        subprocess.Popen(["ipconfig", "/flushdns"])

    def flush_dns_linux():
        """Flush DNS on Linux."""
        subprocess.Popen(["sudo", "/etc/init.d/nscd", "restart"])
        subprocess.Popen(["sudo", "/etc/init.d/dnsmasq", "restart"])
        subprocess.Popen(["sudo", "/etc/init.d/named", "restart"])

    def flush_dns_darwin():
        """Flush DNS on MacOS."""
        subprocess.Popen(["sudo", "killall", "-HUP", "mDNSResponder"])
        subprocess.Popen(["sudo", "dscacheutil", "-flushcache"])

    if sys.platform == "win32":
        flush_dns_win32()
    elif sys.platform == "darwin":
        flush_dns_darwin()
    else:
        flush_dns_linux()


def add_domain_internal(domains):
    """(Internal) Add domain to config."""
    for dm in domains:
        if is_domain_valid(dm):
            if dm not in config["BL_DOMAINS"]:
                config["BL_DOMAINS"].append(dm)
                click.echo(f"Blacklisted: {dm}")
            else:
                click.echo(f"Already blacklisted: {dm}")
        else:
            click.echo(f"Invalid domain: {dm}")


def remove_domain_internal(confirm, domains, fp):
    """(Internal) Remove domain from config."""
    if domains == (".",):
        if len(config["BL_DOMAINS"]) == 0:
            click.echo("No blacklisted domains found", fp)
            exit(0)
        domains = config["BL_DOMAINS"]
    for dm in domains:
        if dm in config["BL_DOMAINS"]:
            option = None
            while confirm and option not in ("y", "n"):
                option = input(get_input_prompt(f"Un-blacklist '{dm}'? [Y/N]"))
            if option == "n":
                continue
            config["BL_DOMAINS"].remove(dm)
            click.echo(f"Un-blacklisted: {dm}", fp)
        else:
            click.echo(f"Domain not found: {dm}", fp)
