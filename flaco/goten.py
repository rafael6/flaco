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
                try:
                    device_formatted = '\nDevice [{}]:\n'.format(device.strip())
                    print(device_formatted, end='')
                    for k, v in SSH().commander(device, commands).items():
                        cmd_output = '{}\n{}'.format(k, v)
                        print(cmd_output.strip())
                        create_record(job_name, device_formatted, cmd_output)
                except OSError as e:
                    print(e)
                    cmd_output = str(e)
                    create_record(job_name, device_formatted, cmd_output+'\n')

    except FileNotFoundError as e:
        print(e)


def main():
    record = input('Do you want an output file? [yes] > ')
    if record == 'yes' or record == '':
        record = 'Yes'
        job_name = input('Enter a name for the output file > ')
    device_file = input('Enter the name of the device file > ')
    commands = input('Enter commands using comma separation > ').split(',')

    print('Review job settings; '
          'enter 1 to proceed or any key to edit the job.')
    print('\tOutput file: {}'.format(record))
    print('\tJob name: {}'.format(job_name))
    print('\tDevice file name: {}'.format(device_file))
    print('\tCommands to execute: {}'.format(commands))
    commit = input()
    if commit == '1':
        dispatcher(device_file, commands, job_name+'.txt')
    else:
        main()


if __name__ == "__main__":
    main()