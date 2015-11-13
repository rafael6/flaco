__author__ = 'rafael'
from element import Element

def main():
    # Varible definition here:
    resolvers = ['8.8.8.8']
    query_type = 'A'
    ports = (80, 443)
    port_type = 'TCP'
    urls = ('https://yahoo.com', 'http://yahoo.com')

    # App title
    print('Checking application my.app.com; please wait')

    # Element construct
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