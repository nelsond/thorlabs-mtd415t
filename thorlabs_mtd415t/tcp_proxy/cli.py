"""
This module provides the command line interface for the tcp proxy server

---
Nelson Darkwah Oppong, March 2018
n@darkwahoppong.com
"""

import sys
import argparse
import logging

from .server import Server
from thorlabs_mtd415t import __version__


desc = ('Simple command line tool for starting a tcp server allowing to proxy'
        ' features of the Thorlabs MTD415T temperature controller via tcp.')

parser = argparse.ArgumentParser(prog='mtd415t-tcp-server', description=desc)

parser.add_argument('serialport', type=str, metavar='SERIALPORT',
                    help='serial port of Thorlabs MTD415T device'
                         ', example: /dev/ttyUSB0')

parser.add_argument('--version', action='version',
                    version='%(prog)s {}'.format(__version__),
                    help='show version number and exit')

parser.add_argument('--host', type=str, metavar='HOST',
                    default='localhost',
                    help='host for listening, default: localhost')

parser.add_argument('-p', '--port', type=int, metavar='PORT', default=3333,
                    help='port for listening, default: 3333')


def main():
    ns = parser.parse_args(sys.argv[1:])

    logging.basicConfig(level=logging.INFO, format='%(asctime)s'
                        ' [%(levelname)s] %(message)s')

    server = Server(ns.host, ns.port, ns.serialport)
    server.start()

    try:
        server.serve()
    except KeyboardInterrupt:
        logging.info('Exiting...')
        server.stop()
