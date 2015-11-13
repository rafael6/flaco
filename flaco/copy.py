import subprocess

def check_transaction(username, host):
    source_file = '/Users/Rafael/Documents/test.py'
    destination_dir = '/home/rafael/PycharmProjects/flaco/flaco/'
    _command = 'scp -v {}@{}:{} {}'.format(
        username, host, source_file, destination_dir)

    try:
        output = subprocess.check_output(_command, shell=True)\
            .decode('utf-8').strip()
        return output
    except subprocess.CalledProcessError as e:
        return str(e)


def main():

    print(check_transaction('rafael', '192.168.64.1'))


if __name__ == "__main__":
    main()