#!/usr/bin/python3

import argparse
import logging
import sys
import time

from api import ApiThread
from db import Database
from dns import DnsThread
from swiper import Swiper

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("Dora")


class ServiceExit(Exception):
    pass


def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit


def main():
    parser = argparse.ArgumentParser(
        prog="Dora",
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
    group.add_argument("--disable-dns", dest="dns_enabled", action="store_false",
                       help="if set, no DNS queries will be captured")
    group.add_argument("--disable-api", dest="api_enabled", action="store_false",
                       help="if set, the api server will not be started")

    args = parser.parse_args()

    try:
        swiper = Swiper.instance(args.domain)
    except UnicodeEncodeError:
        log.error(f"Invalid domain '{args.domain}'")
        return 1

    try:
        db = Database.instance(args.database, False)
    except ValueError:
        return 2
    db.init()

    if args.dns_enabled:
        dns = DnsThread(swiper, "lo")
        dns.start()

    if args.api_enabled:
        api = ApiThread(swiper)
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
