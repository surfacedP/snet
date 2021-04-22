#!/usr/bin/env python

import scapy.all as scapy


def scan(ip):
    # encode IP to string - scapy fails to scan unicode
    ip = ip.encode("utf-8")
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for x in answered_list:
        client_dict = {"ip": x[1].psrc, "mac": x[1].hwsrc}
        clients_list.append(client_dict)

    print_result(clients_list)


def print_result(results_list):
    print("IP\t\t\t      MAC Address\n-----------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])
