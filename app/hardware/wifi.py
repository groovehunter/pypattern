import sys
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio
from app.core.logger import log
# Mock für Desktop-Environment, ansonsten echtes 'network' (MicroPython)
try:
    import network
except ImportError:
    class DummyWLAN:
        def __init__(self, *args): pass
        def active(self, *args): return True
        def connect(self, *args): pass
        def isconnected(self): return True
        def ifconfig(self, *args): return ("127.0.0.1", "255.255.255.0", "1.1.1.1", "8.8.8.8")
        def config(self, **kwargs): pass
    class network:
        STA_IF = 0
        AP_IF = 1
        WLAN = DummyWLAN
class WifiManager:
    def __init__(self, config):
        self.config = config.get("wifi", {})
        self.sta_if = network.WLAN(network.STA_IF)
        self.ap_if = network.WLAN(network.AP_IF)
    async def connect(self):
        self.ap_if.active(False)
        self.sta_if.active(True)

        # Hardware etwas Zeit geben, das RF-Modul zu starten (verhindert oft 0x0102)
        await asyncio.sleep(0.5)

        ssid = self.config.get("ssid", "")
        pwd = self.config.get("pwd", "")
        timeout = self.config.get("timeout_sec", 15)

        # Statische IP setzen, falls in config.json gewünscht
        ip = self.config.get("ip", "")
        if ip:
            netmask = self.config.get("netmask", "255.255.255.0")
            gateway = self.config.get("gateway", "192.168.43.1")
            dns = self.config.get("dns", "8.8.8.8")
            try:
                self.sta_if.ifconfig((ip, netmask, gateway, dns))
                log.info(f"Static IP configured: {ip}")
            except Exception as e:
                log.warn(f"Failed to set static IP: {e}")

        # Leere SSID -> direkt in den AP Modus
        if not ssid:
            log.warn("No SSID configured, jumping directly to AP mode.")
            await self.start_ap()
            return

        log.info(f"Connecting to WiFi '{ssid}'...")
        try:
            self.sta_if.connect(ssid, pwd)
        except Exception as e:
            log.error(f"Hardware-Fehler beim WLAN-Connect: {e}")
            self.sta_if.active(False)
            await self.start_ap()
            return

        elapsed = 0
        # Non-blocking Wait Loop!
        while not self.sta_if.isconnected() and elapsed < timeout:
            await asyncio.sleep(1)
            elapsed += 1
        if self.sta_if.isconnected():
            log.info(f"WLAN Connected! IP: {self.sta_if.ifconfig()[0]}")
        else:
            log.error("WiFi connect failed or timeout. Starting AP Fallback.")
            self.sta_if.active(False)
            await self.start_ap()
    async def start_ap(self):
        ap_ssid = self.config.get("ap_fallback_ssid", "PyPattern-AP")
        ap_pwd = self.config.get("ap_fallback_pwd", "password123")
        self.ap_if.active(True)
        try:
            self.ap_if.config(essid=ap_ssid, password=ap_pwd, authmode=3) # 3 = WPA2
        except Exception:
            # Fallback for some older MicroPython ports oder Mock
            self.ap_if.config(essid=ap_ssid)
        log.info(f"AP Mode started on SSID '{ap_ssid}' / IP: {self.ap_if.ifconfig()[0]}")
    async def keepalive(self):
        """ Background task checking connection every ~15 seconds """
        while True:
            await asyncio.sleep(15)
            # Wenn STA eigentlich aktiv ist, aber die Verbindung abbrach:
            if self.sta_if.active() and not self.sta_if.isconnected():
                log.warn("WiFi connection lost! Attempting background reconnect...")
                # Kein Blockieren! Wiederholt intern Non-Blocking connects.
                await self.connect()
