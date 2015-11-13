#!/usr/bin/env python3

__author__ = 'rafael'
__version__ = '3.1.0'

"""
Dispatch and format output.

>>> from toolkit import Toolkit
>>> from element import Element
>>> yahoo = Element('yahoo.com', 'CAS')
>>> print(yahoo.get_element())
        Element: yahoo.com
>>> print(yahoo.get_etype())
                Type CAS
>>> print(yahoo.check_dns(['8.8.8.8'], 'A'))
                DNS A records: 98.139.183.24, 206.190.36.45, 98.138.253.109
>>> print(yahoo.check_host())
                Ping: 0% packet loss
>>> yahoo.check_socket((80, 443), 'TCP')
['\t\tTCP port 80: open', '\t\tTCP port 443: open']
>>> yahoo.check_url(('https://yahoo.com', 'http://yahoo.com'))
['\t\tURL https://yahoo.com: 200', '\t\tURL http://yahoo.com: 200']
"""

__author__ = 'rafael'

from toolkit import Toolkit


class Element(Toolkit):
    """This is an interface class for the application. Inherits class
    toolkit.Toolkit(). This class' methods overrides each of its parent
    methods, but each of its methods calls the corresponding parent methods.
    Formats the return values from toolkit.Toolkit() methods for display.

    Example:
        yahoo = Element(node, etype)
    """
    def __init__(self, node, etype):
        """
        Initialize class. Use: element = Element(node, etype)
        :param node: string, name or IP address of the element.
        :param etype: str, element type such as F5 VIP, server, etc.
        """
        self.etype = etype
        super().__init__(node)

    def check_dns(self, nservers, qtype):
        """Calls Toolkit.check_dns(nservers, qtype) and formats its ouput for
        display.

        :param nservers:  list of strings, list of DNS servers.
        :param qtype: string, type of record such as A, CNAME, or MX.
        :return: string, formatted Toolkit.check_dns() output.

        Example:
            element = Element(node, etype)
            print(element.check_dns(nservers, qtype))
        """
        return '\t\tDNS {} records: {}'.format(
            qtype, super().check_dns(nservers, qtype))

    def check_host(self):
        """Calls Toolkit.check_host() and filter the returned value to capture
        just the packet loss portion. Returns the packet loss counter.

        :return: string, packet-loss counter.

        Example:
            element = Element(node, etype)
            print(element.check_host())
        """
        _output = super().check_host()
        try:
            _filter = _output.split('received, ')[1]  # filter
            _refined = _filter[0:16].strip(', ')      # 0% packet loss
            return '\t\tPing: {}'.format(_refined)
        except IndexError:
            return 'connection error'

    def check_socket(self, ports, kind):
        """Calls Toolkit.check_socket() for each element (port) in the tuple.
        Formats the returned value as such: 'TCP port 80: open'. Inserts each
        returned value into _port_list. Returns _port_list.

        :param ports: tuple, tuple containing integers (TCP/UDP ports).
        :param kind: string, port type TCP or UDP.
        :return: list, list of formatted strings as:'\t\tTCP port 80: open'

        Example:
            element = Element(node, etype)
            element.check_socket(ports, kind)
        """
        _port_list = []
        for port in ports:
            _result = super().check_socket(port)
            _port_stat = '{} port {}: {}'.format(kind, port, _result)
            _port_list.append('\t\t{}'.format(_port_stat))
        return _port_list

    def check_url(self, urls):
        """Calls Toolkit.check_socket() for each URL in tuple urls.
        Format the returned value as such: 'URL http://yahoo.com: open'.
        Insert each returned value into _url_list. Returns _url_list.

        :param urls: tuple, tuple containing formatted strings for each URL/URI
        :return: list, list of strings in the form of url: result.

        Example:
            element = Element(node, etype)
            element.check_url(urls)
        """
        _url_list = []
        for url in urls:
            _result = super().check_url(url)
            _url_stat = 'URL {}: {}'.format(url, _result)
            _url_list.append('\t\t{}'.format(_url_stat))
        return _url_list

    def get_element(self):
        """Format self.node for display.

        :return: string, formatted string output.

        Example:
            element = Element(node, etype)
            element.get_element()
        """
        return '\tElement: {}'.format(self.node)

    def get_etype(self):
        """Format instance variable etype for display.

        :return: string, formatted string output.

        Example:
            element = Element(node, etype)
            element.get_etype()
        """
        return '\t\tType: {}'.format(self.etype)


def main():
    resolvers = ['8.8.8.8']
    query_type = 'A'
    ports = (80, 443)
    port_type = 'TCP'
    urls = ('https://yahoo.com', 'http://yahoo.com')

    print('Checking application my.app.com; please wait...')

    yahoo = Element('yahoo.com', 'Web Server')
    print(yahoo.get_element())
    print(yahoo.get_etype())
    print(yahoo.check_dns(resolvers, query_type))
    print(yahoo.check_host())
    for port in yahoo.check_socket(ports, port_type):
        print(port)
    for url in yahoo.check_url(urls):
        print(url)

if __name__ == '__main__':
    main()