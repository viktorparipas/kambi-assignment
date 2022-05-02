import re
import time

from subprocess import CalledProcessError, check_output, Popen, PIPE


def list_files(folder_name='', name=None, params=None):
    if not name and not params:
        return run_ls(folder_name)
    else:
        return run_find(folder_name, name, params)


def run_ls(folder_name):
    # time.sleep(5)
    command = f"ls -p {folder_name}"
    command_as_list = command.split()
    process_1 = Popen(command_as_list, stdout=PIPE, stderr=PIPE)
    try:
        check_output(command_as_list)
    except CalledProcessError:
        # Only communicate output if the command failed
        output, error = process_1.communicate()
    else:
        # Remove directories from result
        process_2 = Popen(['grep', '-v', '/'], stdin=process_1.stdout, stdout=PIPE, stderr=PIPE)
        # Allow p1 to receive a SIGPIPE if p2 exits.
        process_1.stdout.close()

        output, error = process_2.communicate()

    finally:
        return output, error


def run_find(folder_name, name, params):
    folder_name = folder_name or '.'
    # Use -- at the end of command to prevent injection attacks
    command = f"find {folder_name} -maxdepth 1 -type f--"
    if name:
        # If name is specified, remove any name filter from params
        if params is not None:
            params = re.sub(r"-name \S+ *", '', params)
        command += f" -name {name}"

    if params:
        params = re.sub(r"-maxdepth \S+ *", '', params)
        params = re.sub(r"-type \S+ *", '', params)
        command += f" {params}"

    command_as_list = command.split()
    process_1 = Popen(command_as_list, stdout=PIPE, stderr=PIPE)
    output, error = process_1.communicate()
    process_1.stdout.close()
    return output, error
