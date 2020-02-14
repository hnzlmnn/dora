import datetime

from scapy.all import Packet
from scapy.layers.inet import IP
from scapy.layers.inet6 import IPv6
from scapy.layers.dns import DNS
from scapy.sendrecv import sniff
import threading
import logging

from db.models import Entry
from swiper import Swiper

log = logging.getLogger(__name__)


class DnsThread(threading.Thread):

    def __init__(self, swiper: Swiper, interface: str):
        threading.Thread.__init__(self)
        self.swiper = swiper
        self.interface = interface
        self.setDaemon(True)

    def _disect_dns(self, dns: DNS, ip_src, v6=False):
        host: bytes = dns.qd.qname
        log.debug(host)
        if not host:
            return
        match = self.swiper.dns_match(host)
        if not match:
            return
        try:
            line = int(match.group(2))
        except ValueError:
            return
        try:
            context = match.group(3).decode('ascii')
        except UnicodeDecodeError:
            return
        entry = Entry(
            source=ip_src,
            v6=v6,
            received_at=datetime.datetime.now(),
            context=context,
            line=line,
            data=match.group(1)
        )
        log.info(entry.summary())
        entry.save()

    def _callback(self, pkt: Packet) -> None:
        log.debug(pkt.summary())
        if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 0:
            if IP in pkt:
                return self._disect_dns(pkt.getlayer(DNS), pkt[IP].src)
            elif IPv6 in pkt:
                return self._disect_dns(pkt.getlayer(DNS), pkt[IPv6].src, True)

    def run(self) -> None:
        log.info(f"Starting dns capture on interface '{self.interface}'")
        try:
            sniff(iface=self.interface, filter="port 53", prn=self._callback, store=0)
        except KeyboardInterrupt:
            pass
