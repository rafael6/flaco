__author__ = 'rafael'

from ssh import SSH


def create_record(job_name, device_formatted, cmd_output):
    with open(job_name, 'a') as output_file:
        output_file.write(device_formatted)
        output_file.write(cmd_output)


def dispatcher(device_file, commands, job_name):
    try:
        with open(device_file, 'r') as devices:
            for device in devices:
                device_formatted = '\nDevice [{}]:\n'.format(device.strip())
                print(device_formatted, end='')
                for k, v in SSH().commander(device, commands).items():
                    cmd_output = '{}\n{}'.format(k, v)
                    print(cmd_output.strip())
                create_record(job_name, device_formatted, cmd_output)
    except FileNotFoundError as e:
        return str(e)


def main():
    record = input('Do you want an output file? [yes] > ')
    if record == 'yes' or record == '':
        job_name = input('Enter a name for the output file > ')
    device_file = input('Enter the name of the device file > ')
    commands = input('Enter commands using comma separation > ').split(',')
    dispatcher(device_file, commands, job_name)


if __name__ == "__main__":
    main()