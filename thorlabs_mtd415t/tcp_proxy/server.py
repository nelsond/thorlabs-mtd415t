# -*- coding: utf-8 -*-
"""
This module provides the Server class.

Example:
    from thorlabs_mtd415t import tcp_proxy

    server = tcp_proxy.Server('127.0.0.1', 3333, '/dev/ttyUSB0')
    server.start()

    try:
        server.serve()
    except KeyboardInterrupt:
        print('Exiting...')
        server.stop()
---
Nelson Darkwah Oppong, March 2018
n@darkwahoppong.com
"""

import socket
import logging
from thorlabs_mtd415t import MTD415TDevice


class Server(object):
    def __init__(self, host, port, device_port):
        self._host = host
        self._port = port

        self._device_port = device_port

        self.is_running = False

    def start(self):
        """
        Starts server
        """
        if self.is_running:
            self.stop()

        self._connect_device()

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((self._host, self._port))
        self._socket.listen(1)
        logging.info('Starting server on port {:d}'.format(self._port))

        self.is_running = True

        return True

    def stop(self):
        """
        Stops server
        """
        if self.is_running is False:
            return False

        self._disconnect_device()
        self._socket.close()

        return True

    def serve(self):
        """
        Enables accepting and handling connections to the server
        """
        conn, addr = self._socket.accept()
        logging.info('Connected to {}:{}'.format(*addr))

        while True:
            try:
                self._handle_request(conn)
            except ConnectionError:
                logging.warning('Disconnected from {}:{}'.format(*addr))
                conn, addr = self._socket.accept()
                logging.info('Connected to {}:{}'.format(*addr))

        conn.close()

    def _connect_device(self):
        logging.info('Connecting to device at {}'.format(self._device_port))
        self._device = MTD415TDevice(self._device_port, auto_save=True)

    def _disconnect_device(self):
        logging.info('Disconnecting device at {}'.format(self._device_port))
        self._device.close()

    def _handle_request(self, conn):
        data = conn.recv(1024).strip().decode('ascii')
        command, arg = self._parse_request(data)

        if command == 'invalid':
            logging.warning('Invalid request "{}"'.format(data))

        elif command == 'set_temp_setpoint':
            result = self._set_temp_setpoint(arg)
            if result is not False:
                conn.send('OK\n'.encode('ascii'))
            else:
                conn.send('ERROR\n'.encode('ascii'))

        else:
            logging.warning('Invalid command "{}"'.format(command))

    def _set_temp_setpoint(self, arg):
        try:
            arg = float(arg)
        except:
            logging.warning('Invalid argument for set_temp_setpoint command'
                            ' "{}"'.format(arg))
            return False

        if arg > 45 or arg < 5:
            logging.warning('Argument for set_temp_setpoint command out of'
                            ' range (>=5, <= 45)')
            return False

        try:
            self._device.temp_setpoint = arg
            logging.info('Set temperature setpoint to {:.3f}°C'.format(arg))
            return True

        except Exception as e:
            logging.info('Error: {}'.format(e))
            return False

    @staticmethod
    def _parse_request(message):
        try:
            command, arg = str(message).split(':')
        except:
            return 'invalid', None

        return command, arg
