import io
import itertools
import os
import re
import subprocess
import sys
import typing
import logging
import functools
import copy
from pathlib import Path

import click

from SuperHelper.Core import Config
from SuperHelper.Core.Config import pass_config

PATH_HOST = str(Path("/etc") / "hosts")
MODULE_NAME: str = "FocusEnabler"
pass_config_no_lock = functools.partial(pass_config, module_name=MODULE_NAME, lock=False)
pass_config_with_lock = functools.partial(pass_config, module_name=MODULE_NAME, lock=True)
__name__ = f"SuperHelper.Modules.{MODULE_NAME}"
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

__all__ = [
    "main",
]


def is_domain_valid(domain) -> bool:
    """Checks if the domain is valid.

    This function matches the domain with a regex pattern of the domain specification. It does not check for domain
    availability or connectivity.

    Args:
        domain (str): The domain to check.

    Returns:
        True if the domain is valid, otherwise False.
    """
    return True if re.match(
        r"^(([a-zA-Z])|([a-zA-Z][a-zA-Z])|([a-zA-Z][0-9])|([0-9][a-zA-Z])"
        r"|([a-zA-Z0-9][a-zA-Z0-9-_]{1,61}[a-zA-Z0-9]))\.([a-zA-Z]{2,6}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z]{2,3})$",
        domain
    ) else False


@pass_config()
def patch_config(config: Config) -> None:
    """Initialise a new config dictionary.

    This function can also be used to patch the existing config.

    Returns:
        None
    """
    cfg = {
        "BL_SECTION_START": "# Added by FocusEnabler, do not modify!",
        "BL_SECTION_END": "# End of section FocusEnabler",
        "BL_DOMAINS": [],
        "PATH_HOST": PATH_HOST,
    }
    config.apply_module_patch(MODULE_NAME, cfg)


def is_root() -> bool:
    """Checks if the user is root.

    This function checks for the effective uid of the user.

    Returns:
        True if the user is root, otherwise False.
    """
    return os.getuid() == 0


@click.group("focus")
def main() -> None:
    """Enables your focus by blocking websites."""
    # Apply patch to module config (or initialise)
    patch_config()


@main.command("add")
@click.option("-c", "--clear", is_flag=True, help="(Optionally) Remove all blacklisted domains (same as 'remove')")
@click.argument("domains", nargs=-1, required=True)
def add_domain(clear, domains) -> None:
    """Add DOMAINS to blacklist."""
    if is_root():
        logger.warning("Please do not run this command as 'root'")
        sys.exit(1)
    if clear:
        with io.StringIO() as sio:
            remove_domain_internal(False, ".", sio)
    sys.exit(add_domain_internal(domains))


@main.command("list")
@pass_config_no_lock()
def list_domain(config: dict[str, ...]) -> None:
    """List blacklisted domains"""
    if is_root():
        logger.warning("Please do not run this command as 'root'")
        sys.exit(1)
    if len(config["BL_DOMAINS"]) == 0:
        click.echo("No blacklisted domains found")
        sys.exit(0)
    click.echo("All blacklisted domains:")
    for domain, count in zip(config["BL_DOMAINS"], itertools.count()):
        click.echo(f"({count + 1}) {domain}")
    sys.exit(0)


@main.command("remove")
@click.option("-c", "--confirm", is_flag=True, help="Ask before removing each domain")
@click.argument("domains", nargs=-1, required=True)
def remove_domain(confirm, domains) -> None:
    """Remove DOMAINS from blacklist"""
    if is_root():
        logger.warning("Please do not run this command as 'root'")
        sys.exit(1)
    sys.exit(remove_domain_internal(confirm, domains, sys.stdout))


@main.command("activate")
@pass_config_no_lock()
def activate_app(config: dict[str, ...]) -> None:
    """Activate FocusEnabler."""
    if not is_root():
        logger.warning("Please run this command as 'root'")
        sys.exit(1)
    if not os.access(config["PATH_HOST"], os.W_OK):
        logger.warning("Hosts file is inaccessible!")
        sys.exit(1)
    with open(config["PATH_HOST"]) as fp:
        if config["BL_SECTION_START"] in fp.read():
            logger.warning("FocusEnabler is already activated! Deactivate first.")
            sys.exit(1)
    entries: typing.List[str] = [config["BL_SECTION_START"]]
    for domain in config["BL_DOMAINS"]:
        logger.info(f"Adding entry {domain} -> Done")
        entries.append(f"127.0.0.1   {domain}")
        entries.append(f"127.0.0.1   www.{domain}")
    entries.append(config["BL_SECTION_END"])
    try:
        with open(config["PATH_HOST"], "a") as fp:
            fp.write("\n".join(entries))
        click.echo("Written to host file!")
        flush_dns()
        click.echo("FocusEnabler is enabled!")
    except OSError:
        logger.exception("Writing to host file -> Failed")
        sys.exit(1)
    sys.exit(0)


@main.command("deactivate")
@pass_config_no_lock()
def deactivate_app(config: dict[str, ...]) -> None:
    """Deactivate FocusEnabler"""
    if not is_root():
        logger.warning("Please run this command as 'root'")
        sys.exit(1)
    if not os.access(config["PATH_HOST"], os.W_OK):
        logger.warning("Hosts file is inaccessible!")
        sys.exit(1)
    try:
        with open(config["PATH_HOST"]) as fp:
            content = fp.read()
            original_content_len = len(content)
        content = re.sub(rf"{config['BL_SECTION_START']}(.|[\n\r\t])*{config['BL_SECTION_END']}", "", content)
        if len(content) == original_content_len:
            logger.warning("FocusEnabler is not activated! Activate first")
            sys.exit(1)
    except OSError:
        logger.exception("Unable to read host file")
        sys.exit(1)
    try:
        with open(config["PATH_HOST"], "w") as fp:
            fp.write(content)
        click.echo("FocusEnabler is disabled!")
    except OSError:
        logger.exception("Writing to host file -> Failed")
        sys.exit(1)
    sys.exit(0)


def flush_dns() -> None:
    """Flushes DNS cache on machine.

    Returns:
        None
    """

    def flush_dns_linux():
        """Flush DNS on Linux."""
        subprocess.Popen(["sudo", "/etc/init.d/nscd", "restart"])
        subprocess.Popen(["sudo", "/etc/init.d/dnsmasq", "restart"])
        subprocess.Popen(["sudo", "/etc/init.d/named", "restart"])

    def flush_dns_darwin():
        """Flush DNS on MacOS."""
        subprocess.Popen(["sudo", "killall", "-HUP", "mDNSResponder"])
        subprocess.Popen(["sudo", "dscacheutil", "-flushcache"])

    if sys.platform == "darwin":
        flush_dns_darwin()
    else:
        flush_dns_linux()


@pass_config_with_lock()
def add_domain_internal(domains: list[str], config: dict[str, ...]) -> int:
    """Adds domains to module config.

    Args:
        domains (list[str]): A list of domain name strings to be added.
        config (dict[str, ...]): The module config.

    Returns:
        0 if the operation succeeds, otherwise 1.
    """
    all_domains = copy.deepcopy(config["BL_DOMAINS"])
    for dm in domains:
        if is_domain_valid(dm):
            if dm not in all_domains:
                all_domains.append(dm)
                click.echo(f"Blacklisted: {dm}")
            elif dm not in config["BL_DOMAINS"]:
                continue
            else:
                click.echo(f"Already blacklisted: {dm}")
        else:
            click.echo(f"Invalid domain: {dm}")
            break
    else:
        config["BL_DOMAINS"] = all_domains
        return 0
    return 1


@pass_config_with_lock()
def remove_domain_internal(confirm: bool, domains: list[str], fp: io.IOBase, config: dict[str, ...]) -> int:
    """Removes domains from module config.

    Args:
        confirm (bool): Whether not to ask for confirmation.
        domains (list[str]): A list of domain name strings to be added.
        fp (io.IOBase): The target output buffer (in place of `sys.stdout`)
        config (dict[str, ...]): The module config.

    Returns:
        0 if the operation succeeds, otherwise 1.
    """
    if domains == (".",):
        if len(config["BL_DOMAINS"]) == 0:
            click.echo("No blacklisted domains found", fp)
            exit(0)
        domains = config["BL_DOMAINS"]
    all_domains = copy.deepcopy(config["BL_DOMAINS"])
    for dm in domains:
        if dm in all_domains:
            if not confirm:
                if not click.confirm(f"Un-blacklist '{dm}'?"):
                    continue
            all_domains.remove(dm)
            click.echo(f"Un-blacklisted: {dm}", fp)
        elif dm in config["BL_DOMAINS"]:
            continue
        else:
            click.echo(f"Domain not found: {dm}", fp)
            break
    else:
        config["BL_DOMAINS"] = all_domains
        return 0
    return 1
