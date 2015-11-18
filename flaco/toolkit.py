#!/usr/bin/env python3
__author__ = 'rafael'
__version__ = '3.1.0'

"""
This modules provides methods for checking: ICMP/DNS, sockets, and URL status.

>>> from toolkit import Toolkit
>>> element = Toolkit(node='yahoo.com')
>>> print(element.check_dns(['8.8.8.8'], 'A'))
98.139.183.24, 206.190.36.45, 98.138.253.109
>>> print(element.check_host('3'))
--- yahoo.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 401ms
rtt min/avg/max/mdev = 78.102/78.205/78.328/0.336 ms
>>> print(element.check_socket(80, 'TCP'))
open
>>> print(element.check_url('https://yahoo.com'))
200

"""

import dns.resolver
import socket
import subprocess
import urllib.request


class Toolkit:
    """Container class for the following network related methods: check_dns(),
    check_host(), check_socket(), and check_url().

    Example:
        element = Toolkit(node)
    """
    def __init__(self, node=None):
        """Initializes instance variable node.

        Use: element = Toolkit(node)

        :param node: string, name or IP address of an IP element.
        """
        self.node = node

    def check_dns(self, nservers, qtype):
        """Process name resolution (DNS) queries on instance variable node
        using a name server from a given list of name servers (nservers), and a
        query type (qtype). Returns DNS data otherwise an exception.

        Example:
            element = Toolkit(node)
            print(element.check_dns([nservers], qtype))

        :param nservers: list of strings, DNS servers.
        :param qtype: string, one of the these query types: A, CNAME, MX, PTR.
        :return: string, name resolution data otherwise an exception.
        """
        try:
            _data = []
            _resolver = dns.resolver.Resolver()
            _resolver.nameservers = nservers

            if qtype == 'MX' or qtype == 'mx':
                _answer = _resolver.query(self.node, qtype)
                #for rdata in _answer:
                    #_data.append('Host{} preferance {}'.format(
                        #rdata.exchange, rdata.preference))
                _data = ['Host {} preferance {}'.format(
                    rdata.exchange, rdata.preference) for rdata in _answer]
            elif qtype == 'PTR' or qtype == 'ptr':
                _answer = _resolver.query(dns.reversename.from_address(
                    self.node), qtype)
                #for record in _answer:
                    #_data.append(str(record))
                _data = [str(record) for record in _answer]
            else:
                # Handles both A and CNAME records
                _answer = _resolver.query(self.node, qtype)
                #for address in _answer:
                    #_data.append(str(address))
                _data = [str(address) for address in _answer] # NEW
        except dns.exception.SyntaxError:
            return 'Error; check IP address.'
        except dns.rdatatype.UnknownRdatatype:
            return 'Error; check query type.'
        except dns.resolver.NoAnswer:
            return 'Error; check query type.'
        except dns.resolver.NXDOMAIN:
            return 'Error; check hostname.'
        except dns.exception.Timeout:
            return 'Timeout; check connection and DNS server.'
        else:
            return ', '.join(_data)

    def check_host(self, count='9'):
        """Pings the instance variable node with a load of 1378 bytes a given
        number of times (9 by default) at a 200ms interval. Returns a ping
        statistics as a string otherwise an exception.

        Example:
            element = Toolkit(node)
            print(element.check_host(count))

        :param count: string, number of echo requests.
        :return: string, containing ping related information or an exception.
        """
        _interval = '.2'  # 200ms
        _size = '1350'    # bytes
        _command = 'ping -c {} -i {} -s {} {} | grep -1 loss'.format(
            count, _interval, _size, self.node)
        try:
            self.output = subprocess.check_output(_command, shell=True)\
                .decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            return str(e)
        else:
            return self.output

    def check_socket(self, port, kind='TCP'):
        """Check the status of a given socket (self.node, port, kind) as arguments.
        Returns 'open' is the socket is open otherwise an exception.

        Example:
            element = Toolkit(node)
            print(element.check_socket(port, kind))

        :param port: integer, TCP/UDP port number.
        :param kind: string, port type TCP or UDP.
        :return: string, open otherwise and exception.
        """
        if kind == 'udp' or kind == 'UDP':
            _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            _sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            _sock.connect((self.node, port))
            _sock.close()
        except socket.error as e:
            return str(e)
        except OverflowError as e:
            return str(e)
        else:
            return 'open'

    def check_url(self, url):
        """Check the status of a given URL and returns the HTTP code as a
        string. Returns the HTTP status code otherwise an exception.

        Example:
            element = Toolkit(node)
            print(element.check_url(url))

        :param url: string, URL/URI to check.
        :return: string, HTTP code otherwise and exception.
        """
        try:
            _connection = urllib.request.urlopen(url)
        except urllib.error.URLError as e:
            return str(e)
        except ValueError as e:
            return str(e)
        else:
            return str(_connection.getcode())


def main():
    element = Toolkit(node='yahoo.com')
    print(element.check_dns(['8.8.8.8'], 'A'))
    print()
    print(element.check_host('3'))
    print()
    print(element.check_socket(80, 'TCP'))
    print()
    print(element.check_url('https://yahoo.com'))

if __name__ == "__main__":
    main()
