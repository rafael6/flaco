#!/usr/bin/env python3

__author__ = 'rafael'
__version__ = '3.1.0'

from toolkit import Toolkit


def get_dns(node, nservers='8.8.8.8', qtype='A'):
    """Calls Toolkit.check_dns([nservers], qtype) and format the
    returned value.
    """
    dns = Toolkit(node=node)
    result = dns.check_dns([nservers], qtype)
    print('Record=[{}] Resolution=[{}]'.format(node, result))


def get_ping(node, count='25'):
    """Calls Toolkit.check_host(count) and format the returned value.
    """
    ping = Toolkit(node=node)
    try:
        print(ping.check_host(count=count))
    except AttributeError:
        print('Unable to ping {}; check its syntax'.format(node))


def get_socket(node, prt, prt_kind='TCP'):
    """Calls Toolkit.check_socket(port, kind) and format the returned value.
    """
    socket = Toolkit(node=node)
    result = socket.check_socket(port=prt, kind=prt_kind)
    print('Type=[{}] Socket=[{}]:[{}] Status=[{}]'.format(
        prt_kind, node, prt, result))


def get_url(site):
    """Calls Toolkit.check_socket(url) and format the returned value.
    """
    http = Toolkit()
    status = http.check_url(url=site)
    print('URI=[{}] Status=[{}]'.format(site, status))


def input_handler(selection):
    if selection == '1':
        hostname = input('Hostname > ')
        resolver = input('Enter DNS server [int] or ext > ')
        if resolver == '' or resolver == 'int':
            resolver = '8.8.8.8'  # Internal DNS server
        elif resolver == 'ext' or resolver == 'EXT':
            resolver = '8.8.8.8'  # External DNS server
        else:
            print('Enter internal [int] or ext.')
            input_handler('1')
        query_type = input('Enter query type [A-Record], CNAME, MX, PTR > ')
        if query_type == '':
            query_type = 'A'
        get_dns(hostname, resolver, query_type)
    elif selection == '2':
        hostname = input('Hostname > ')
        echos = input('Enter number of echo requests [25] > ')
        if echos == '':
            echos = '25'
        get_ping(hostname, echos)
    elif selection == '3':
        hostname = input('Hostname > ')
        port = input('Enter a port number > ')
        kind = input('TCP or UDP? [TCP]')
        if kind == '':
            kind = 'tcp'
        get_socket(hostname, int(port), kind)
    elif selection == '4':
        url = input('URL > ')
        get_url(url)
    else:
        print('\nInvalid selection; try again or Ctrl-C to exit.')


def main():

    while True:
        print('''\033[1m\033[91m
                                 (((Gohan)))\033[0m
               \033[1mEnter a number for selection or Ctrl-C to exit.

    [1] - DNS
    [2] - PING
    [3] - SOCKET
    [4] - URI
    \033[0m''')
        try:
            option = input('Enter selection number > ')
            if option == '1':
                input_handler(option)
            elif option == '2':
                input_handler(option)
            elif option == '3':
                input_handler(option)
            elif option == '4':
                input_handler(option)
            else:
                print('\nInvalid selection; try again or Ctrl-C to exit.')

        except KeyboardInterrupt:
            print('\nGoodbye')
            exit()

if __name__ == "__main__":
    main()