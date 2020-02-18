import datetime

from scapy.all import Packet
from scapy.layers.inet import IP
from scapy.layers.inet6 import IPv6
from scapy.layers.dns import DNS
from scapy.sendrecv import sniff
import threading
import logging

from db import Entry, Meta
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
            log.debug("not matching host")
            return
        log.debug(match.groups())
        try:
            context = match.group(4).decode('ascii')
        except UnicodeDecodeError:
            log.debug("bogus data")
            return
        if not match.group(2):
            line = 0
            try:
                data = int(match.group(3))
            except ValueError:
                log.debug("invalid line count")
                return
        else:
            try:
                line = int(match.group(2))
            except ValueError:
                log.debug("not matching line")
                return
            data = match.group(1)
        if line == 0:
            Meta.insert(
                context=context,
                source=ip_src,
                v6=v6,
                updated_at=datetime.datetime.now(),
                lines=data
            ).on_conflict_ignore().execute()
            return
        entry = Entry.create(
            source=ip_src,
            v6=v6,
            received_at=datetime.datetime.now(),
            context=context,
            line=line,
            data=data
        )
        log.debug(entry.summary())

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
