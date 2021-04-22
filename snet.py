#!/usr/bin/env python

import click
import modules.mac_changer as changer
import modules.network_scanner as netscan
import modules.arp_spoof as arp


@click.command()
@click.option("--mac", nargs=2)
@click.option("--net")
@click.option(
    "-t",
    "--target",
    prompt="Input target IP",
    help="IP address of the target",
)
@click.option(
    "-g",
    "--gateway",
    prompt="Input gateway IP",
    help="Gateway IP",
)
def x(mac, net, target, gateway):
    if mac:
        changer.show_mac(mac[0], mac[1])

    if net:
        netscan.scan(net)

    arp.arp_spoof(target, gateway)


if __name__ == "__main__":
    x()
