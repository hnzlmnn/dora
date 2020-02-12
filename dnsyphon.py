#!/usr/bin/python3

import argparse
import logging
import signal
import sys
import time
import uuid
import binascii

from api import ApiThread
from db import Database, Entry
from dns import DnsThread

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("DNSyphon")


class ServiceExit(Exception):
    pass


def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit


def main():
    parser = argparse.ArgumentParser(
        prog="DNSyphon",
        description="Exfiltrate data via DNS",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-n", "--domain", dest="domain", type=str, default="dns.cybaer.ninja",
                        help="the domain for which queries should be logged")
    parser.add_argument("-d", "--database", dest="database", type=str, default="sqlite:///:memory:",
                        help="database connection string for sqlalchemy")
    parser.add_argument("-p", "--port", dest="port", type=int, default=3000,
                        help="port of the api")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--disable-dns", dest="dns_enabled", default=False, action="store_false",
                       help="if set, no DNS queries will be captured")
    group.add_argument("--disable-api", dest="api_enabled", default=False, action="store_false",
                       help="if set, the api server will not be started")

    args = parser.parse_args()

    try:
        db = Database(args.database)
    except ValueError:
        return 1

    if args.dns_enabled:
        try:
            domain: bytes = args.domain.encode("ascii")
        except UnicodeEncodeError:
            log.error(f"Invalid domain '{args.domain}'")
            return 2
        dns = DnsThread("lo", domain)
        dns.start()

    if args.api_enabled:
        api = ApiThread()
        api.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            log.info("Shutting down...")
            break
    return 0


if __name__ == "__main__":
    sys.exit(main())
