import network
import time
import machine

WIFI_SSID = "SSID-NAME"
WIFI_PASS = "PSK-Passwort"

IP_ADDR   = "192.168.2.162"
NETMASK   = "255.255.255.0"
GATEWAY   = "192.168.2.1"
DNS       = "192.168.2.1"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def connect():
    if wlan.isconnected():
        return True

    # saubere Re-Initialisierung
    wlan.active(False)
    time.sleep(1)
    wlan.active(True)

    # statische IP setzen
    wlan.ifconfig((IP_ADDR, NETMASK, GATEWAY, DNS))

    print("Verbinde mit WLAN:", WIFI_SSID)
    wlan.connect(WIFI_SSID, WIFI_PASS)

    timeout = 20
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1
        print(".", end="")

    if wlan.isconnected():
        print("\nWLAN verbunden:", wlan.ifconfig())
        return True
    else:
        print("\nWLAN fehlgeschlagen – Neustart")
        time.sleep(3)
        machine.reset()

