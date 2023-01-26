# AI&P Final project [Create M6 2022-2023]
# controller_hardware/server.py
#
# Copyright 2022-2023 Jakub Stachurski
# Copyright 2022-2023 Natalia Bueno Donadeu
#
# Imports
from network import WLAN, STA_IF
import socket
from micropython import const
from time import sleep_ms

from hardware import Hardware
from data import ControllerData, readpacket


WIFI_NAME = "machine"
WIFI_KEY = "sussypassword"
DESIRED_IP = 69


def wlan_connect(wlan):
    wlan.connect(WIFI_NAME, WIFI_KEY)
    while not wlan.isconnected():
        pass


def init_wlan():
    # WLAN
    wlan = WLAN(STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        wlan_connect(wlan)

    ip, mask, gateway, dns = wlan.ifconfig()

    ip_parts = ip.split('.')

    if int(ip[-1]) != DESIRED_IP:
        wlan.disconnect()
        new_ip = '.'.join(ip_parts[:3]+[str(DESIRED_IP)])
        wlan.ifconfig((new_ip, mask, gateway, dns))
        wlan_connect(wlan)

    ip, _, _, _ = wlan.ifconfig()
    print(ip)
    return ip


def init_server(ip):
    # Server
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = socket.getaddrinfo(ip, 420)[0][-1]
        print(addr)
        sock.bind(addr)
        sock.listen(2)

        while True:
            loop(*sock.accept())
    except OSError as e:
        print(e)
    finally:
        sock.close()


def init():
    ip = init_wlan()
    Hardware.init()
    init_server(ip)


def loop(sock, addr):
    data = ControllerData()
    while True:
        Hardware.writeData(data)
        sleep_ms(12)
        sock.write(data.writeMESSAGE())
        try:
            s_packet = readpacket(sock).decode('utf-8')
            i_packet = int(s_packet)

            if i_packet == 0:
                freq = 100
                Hardware.setBuzzer(const(1), 0)
            else:
                Hardware.setBuzzer(i_packet, 50)
        except:
            pass


if __name__ == "__main__":
    init()
