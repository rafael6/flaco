__author__ = 'rafael'
__version__ = '1.0.0'

"""
This module is used to establish an SSH client session with a given host.
It includes methods for the handling of shell commands and its output, and for
SCP operations.

>>> from ssh import SSH
>>> username = 'an_username'
>>> password = 'a_password'
>>> device = '192.168.64.1'
>>> commands = ['pwd']
>>> file = '/Users/Rafael/Documents/test.py'
>>> destination = '/home/rafael'
>>> test = SSH(username, password)
>>> print(test.commander(device, commands))
{'DATE/TIME: 2015-11-12 19:40:35.389500 CLI: pwd': '/Users/Rafael\n'}
>>> scp_test = SSH(username, password)
>>> scp_test.get_scp(device, file, destination)

"""

import paramiko
import time
from datetime import datetime
from scp import SCPClient


class SSH:
    def __init__(self, username='rafael', password='default_pw_ro', port=22):
        """Initialize username, password, and port.

        :param username: string, username
        :param password: string, password
        :param port: integer, TCP port, default value = 22

        Instance attribute self.client is an SSH client object.
        """
        self.username = username
        self.password = password
        self.port = port
        self.client = None
        #self.output_list = []
        self.output_dict = dict()

    def get_client(self, node):
        """
        Create an SSH client object from a given node (IP address or hostname)
        and assigns it to object attribute self.client.

        This method also creates an SSH log file.

        :param node: string, IP address or hostname

        Example:
            self.get_client(node)
        """
        paramiko.util.log_to_file('paramiko.log')
        _client = paramiko.SSHClient()
        _client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            _client.connect(
                node, self.port, self.username, self.password)
        except ConnectionRefusedError:
            print('Connection refused on {}.'.format(node.strip()))
        except paramiko.AuthenticationException:
            print('Authentication failed on {}.'.format(node.strip()))
            exit()
        except KeyboardInterrupt:
            print('Goodbye')
            exit()
        else:
            self.client = _client

    def get_scp(self, node, source, destination_path):
        """Calls get_client with a given device (IP or hostname) to form an SSH
        self.client object.

        It then uses the self.client object to call get_transport() to build a
        SCP client object.

        The SCP client object uses the given source as the /path/to/source_file to
        and /destination/path execute a get method.

        :param node: string, IP or hostname.
        :param source: string, /directory/to/source_file
        :param destination_path: string, /destination/path

        Example:
            username = 'user'
            password = 'password'
            device = '192.168.64.1'
            source = '/Users/Rafael/Documents/test.py'
            destination_path = '/home/directory'
            scp_test = SSH(username, password)
            scp_test.get_scp(device, source)
        """
        self.get_client(node)
        with SCPClient(self.client.get_transport()) as scp:
            scp.get(source, destination_path)
        self.client.close()

    def commander(self, device, commands):
        """Calls get_client with a given device (IP or hostname) to form an SSH
        self.client object attribute. It then uses this object to issue an
        self.client.exec_command(command) method using a given command.

        Updates self.output_dict object attribute with a key/value pair where
        date/time and command are combined as a string for the key, and the
        output of self.client.exec_command(command) is used as value.

        :param device: str, IP address or hostname for the target node.
        :param commands: list, list of commands executed against node.
        :return: self.output_dict containing date/time and command as key, and the
        output for such command as value.

        Example:
            username = 'rafael'
            password = 'Levittown'
            device = '192.168.64.1'
            commands = ['whoami', 'pwd']
            test = SSH(username, password)
            print(test.commander(device, commands))
        """
        self.get_client(device)
        if self.client is not None:
            for command in commands:
                stdin, stdout, stderr = self.client.exec_command(command)
                command_output = stdout.read().decode("utf-8")
                key = 'DATE/TIME: {} CLI: {}'.format(datetime.now(), command)
                self.output_dict[key] = command_output
                time.sleep(2)
            self.client.close()  # Moved to the right
            return self.output_dict  # Moved to the right


def main():
    username = 'rafael'
    password = 'Levittown'

    device = '192.168.64.1'
    commands = ['whoami', 'pwd']

    file = '/Users/Rafael/Documents/test.py'
    destination = '/home/rafael'

    test = SSH(username, password)
    print(test.commander(device, commands))

    scp_test = SSH(username, password)
    scp_test.get_scp(device, file, destination)


if __name__ == "__main__":
    main()
