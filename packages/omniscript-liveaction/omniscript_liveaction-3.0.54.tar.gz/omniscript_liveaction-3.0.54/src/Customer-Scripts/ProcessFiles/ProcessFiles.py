"""ProcessFiles.py"""

import os
import sys
import argparse
import keyring
import paramiko
import time
import socket

from pathlib import PurePath

import omniscript
from omniscript.invariant import BYTES_PER_MEGABYTE

script_version = '1.0.0'
data_path = '/var/lib/omni/data'
sub_dir = 'ProcessFiles'
monitor_path = '/home/gary/mon'
capture_name = 'ProcessFiles Capture'
capture_comment = f'Capture and process packet in {monitor_path}.'
filter_name = ' ProcessFiles Filter'
filter_address = '192.168.7.200'

created_directory_list = []


def get_password(host, user, port=443):
    try:
        ip = [str(i[4][0]) for i in socket.getaddrinfo(host, port)][0]
    except Exception:
        ip = host
    return keyring.get_password(ip, user)


def get_token(host, user, port=443):
    try:
        ip = [str(i[4][0]) for i in socket.getaddrinfo(host, port)][0]
    except Exception:
        ip = host
    label = f'{user}:token'
    token = keyring.get_password(ip, label)
    return token.encode() if token else None


def set_token(host, user, token, port=443):
    try:
        ip = [str(i[4][0]) for i in socket.getaddrinfo(host, port)][0]
    except Exception:
        ip = host
    label = f'{user}:token'
    keyring.set_password(ip, label, token.decode() if token else None)


def read_token_file(path, host, port):
    token_file = os.path.join(path, 'f{host}-{port}.bin')
    if os.path.exists(token_file):
        with open(token_file, 'rb') as tf:
            token = tf.read()
            return token
    return None


def update_token_file(path, host, port, token):
    token_file = os.path.join(path, 'f{host}-{port}.bin')
    if os.path.exists(token_file):
        with open(token_file, 'wb') as tout:
            tout.write(token)


def write_token_file(path, host, port, token):
    if os.path.exists(path):
        os.create_path(path)
    token_file = os.path.join(path, 'f{host}-{port}.bin')
    with open(token_file, 'wb') as tout:
        tout.write(token)


class Options(object):
    """Class to parse command line options, then create and login
    to an OmniEngine.
    """

    def __init__(self, arg_list=None):
        self.file_list = []
        self.host = omniscript.DEFAULT_HOST
        self.port = omniscript.DEFAULT_PORT
        self.secure = True
        self.user = 'root'
        self.password = None
        self.otp = None
        self.tokens_directory = 'tokens/'
        self.keyring = True
        self.timeouts = None
        self.verbose = False
        self.help = False
        self._parser = Options._build_parser()
        if arg_list:
            self.parse_arguments(arg_list)

    @classmethod
    def _build_parser(cls):
        # Help will be added as the last argument so it's at the end of the help text.
        parser = argparse.ArgumentParser(prog='ProcessFiles.py', add_help=False)
        # Command line argument is 'files' but attribute is 'file_list', see parse_arguments().
        parser.add_argument(
            '-f', '--files', nargs='+', help='The file or list of files to process.')
        parser.add_argument(
            '-h', '--host', default='localhost',
            help='The IP Address or the name of the system hosting the OmniEngine. '
            '(Default: %(default)s)')
        parser.add_argument(
            '-p', '--port', default='443', type=int,
            help='The port number of the OmniEngine\'s web server. (Default: %(default)s)')
        parser.add_argument(
            '-s', '--secure', default=True, action='store_true',
            help='Enable using the Secure HTTP (HTTPS) protocol. (Default: %(default)s)')
        parser.add_argument(
            '--timeouts', default=f'({omniscript.DEFAULT_CONNECTION_TIMEOUT}, '
            f'{omniscript.DEFAULT_REQUEST_TIMEOUT})',
            help='Engines HTTP Connection and Request timeouts in seconds. (Default: %(default)s) '
            'To disable timeouts set TIMEOUTS to Off or None.')
        parser.add_argument(
            '-u', '--user', default='root', help='The user account name. (Default: %(default)s)')
        parser.add_argument(
            '--password', help='Password of the user account. If absent keyring will be tried '
            'if enabled (see --keyring).')
        parser.add_argument(
            '--otp', help='One Time Password for multi-factor authentication. (Optional)')
        parser.add_argument(
            '-t', '--tokens_dir', default='tokens/',
            help='The directory where token files are stored. The file '
            'TOKENS_DIR/<host>-<port>.bin will be read and updated if it exists. '
            '(Default: %(default)s)')
        parser.add_argument(
            '-k', '--keyring', default=True, action='store_true',
            help='Enable using keyring. If enabled the keyring will be checked for password if '
            'not supplied and for tokens if no token file is found (see --tokens_dir). '
            '(Default: %(default)s)')
        parser.add_argument(
            '-v', '--verbose', default=False, action="store_true",
            help='Enable verbose output. (Default: %(default)s)')
        parser.add_argument(
            '--help', default=False, action='store_true', help='Display this help text.')
        return parser

    def create_engine(self, omni):
        return omni.create_engine(self.host, self.port, self.secure, self.timeouts)

    def login(self, engine):
        if not engine:
            return False
        token = read_token_file(self.tokens_directory, self.host, self.port)
        if not token and self.keyring:
            token = get_token(self.host, self.user, self.port)
        try:
            if engine.login(self.user, self.password, self.otp, token, self.timeouts):
                new_token = engine.get_session_token()
                if new_token != token:
                    update_token_file(self.tokens_directory, self.host, self.port, new_token)
                    if self.keyring:
                        set_token(self.host, self.user, new_token, self.port)
                return True
        except Exception:
            # Token may be stale...
            pass

        password = self.password
        if not password and self.keyring:
            password = get_password(self.host, self.user, self.port)
        try:
            if engine.login(self.user, password, self.otp, None, self.timeouts):
                new_token = engine.get_session_token()
                if new_token:
                    update_token_file(self.tokens_directory, self.host, self.port, new_token)
                    if self.keyring:
                        set_token(self.host, self.user, new_token)
                return True
        except Exception:
            pass

        result = engine.login(self.user, self.password, self.otp, None, self.timeouts)
        if result and self.keyring:
            new_token = engine.get_session_token()
            set_token(self.host, self.user, new_token)

        return result

    def parse_arguments(self, arglist):
        settings = self._parser.parse_args(arglist)
        self.file_list = settings.files if isinstance(settings.files, list) else [settings.files]
        self.host = settings.host
        self.port = settings.port
        self.secure = settings.secure
        self.timeouts = settings.timeouts
        self.user = settings.user
        self.password = settings.password
        self.otp = settings.otp
        self.tokens_directory = settings.tokens_dir
        self.keyring = settings.keyring
        self.verbose = settings.verbose
        self.help = settings.help

    def print_help(self):
        self._parser.print_help()


def get_adapter(engine, plugin, folder):
    # Return the FolderAdapterOE adapter monitoring folder.
    adpt_list = engine.get_adapter_list()
    adpt = omniscript.find_adapter(adpt_list, folder)

    # Return the adapter if found, else create it.
    if isinstance(adpt, omniscript.Adapter):
        return adpt

    # Create a new FolderAdapter to monitor the folder.
    adapter_id = omniscript.OmniId(True)
    mask = '*.pcap'
    speed = -1
    save = ''

    create_adapter_msg = (
        '<CreateAdapter>'
        '<FolderAdapter>'
        f'<Id>{adapter_id}</Id>'
        f'<Monitor>{folder}</Monitor>'
        f'<Mask>{mask}</Mask>'
        f'<Speed>{speed}</Speed>'
        f'<Save>{save}</Save>'
        '</FolderAdapter>'
        '</CreateAdapter>'
    )
    engine.send_plugin_message(plugin, create_adapter_msg)

    adpt_list = engine.get_adapter_list()
    adpt = omniscript.find_adapter(adpt_list, folder)
    return adpt


def create_filter(engine, name, comment, plugin, address):
    # Create new Address and Plugin Filter.
    filter = omniscript.Filter(name)
    filter.comment = comment
    plugin_node = omniscript.PluginNode()
    plugin_node.ids = [plugin.id]
    addr_node = omniscript.AddressNode()
    addr_node.address_1 = omniscript.IPv4Address(address)
    addr_node.accept_1_to_2 = True
    addr_node.accept_2_to_1 = True
    addr_node.and_node = plugin_node
    filter.criteria = addr_node
    engine.add_filter(filter)
    fltr_list = engine.get_filter_list()
    fltr = omniscript.find_filter(fltr_list, name)
    return fltr


def create_capture(engine, name, comment, adpt, plugin, fltr):
    ct = omniscript.CaptureTemplate()
    ct.general.option_start_capture = False

    ct.set_adapter(adpt)

    ct.general.name = name
    ct.general.buffer_size = 10 * BYTES_PER_MEGABYTE
    ct.general.comment = comment
    ct.general.directory = name
    ct.general.file_pattern = f'{name} - '
    ct.general.file_size = 128 * BYTES_PER_MEGABYTE
    ct.general.option_capture_to_disk = True
    ct.general.option_continuous_capture = True
    ct.general.option_deduplicate = True
    ct.general.option_priority_ctd = True

    ct.analysis.option_analysis_modules = True
    ct.analysis.option_network = True
    ct.analysis.option_summary = True

    ct.filter.mode = omniscript.FILTER_MODE_ACCEPT_MATCHING_ANY
    ct.add_filter(fltr)

    ct.plugins.modules = [plugin]
    # Note this sets the configuration of the object in module_list.
    plugin.set_configuration(
        '<Case>Alpha</Case>'
        '<Case>Beta</Case>'
        '<Case>Delta</Case>'
        '<Notes>Quick Test</Notes>'
    )

    try:
        capt = engine.create_capture(ct)
        if capt is None:
            print('*** Failed to create capture.')
    except Exception:
        print('Failed to create capture.')
        sys.exit(2)
    return capt


def delete_directory(ssh, directory, password):
    _, _stdout, _ = ssh.exec_command(f'ls {directory}')
    dest_names = _stdout.read().decode('utf-8').splitlines()
    if dest_names:
        print(f'diretory is not empty: {directory}')
    else:
        channel = ssh.invoke_shell()
        channel.send(f'sudo -S -k -p "" rmdir {directory}')
        channel.send('\n')
        rec = ''
        while 'sudo' not in rec:
            if channel.recv_ready():
                rec = channel.recv(1024).decode('utf-8')
            else:
                time.sleep(1)
        channel.send(f'{password}\n')
        resp = ''
        while len(resp) == 0:
            if channel.recv_ready():
                resp = channel.recv(1024)
            else:
                time.sleep(1)


def delete_directory_list(host, user, directory_list):
    if not isinstance(directory_list, list):
        directory_list = [directory_list]

    password = get_password(host, user)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.RejectPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, 22, user, password)
    for directory in directory_list:
        delete_directory(ssh, directory, password)
    ssh.close()


def move_file(ssh, source_path, destination_path, file_name, password):
    _, _stdout, _ = ssh.exec_command(f'ls {destination_path}')
    dest_names = _stdout.read().decode('utf-8').splitlines()
    if file_name in dest_names:
        print(f'File already exists in {destination_path}')
    else:
        full_path = str(PurePath(source_path, file_name))
        channel = ssh.invoke_shell()
        channel.send(f'sudo -S -k -p "" mv {full_path} {destination_path}')
        channel.send('\n')
        rec = ''
        while 'sudo' not in rec:
            if channel.recv_ready():
                rec = channel.recv(1024).decode('utf-8')
            else:
                time.sleep(1)
        channel.send(f'{password}\n')
        resp = ''
        while len(resp) == 0:
            if channel.recv_ready():
                resp = channel.recv(1024)
            else:
                time.sleep(1)


def move_files(host, user, source_path, destination_path, file_list):
    password = get_password(host, user)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.RejectPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, 22, user, password)
    for file_name in file_list:
        move_file(ssh, source_path, destination_path, PurePath(file_name).name, password)
    ssh.close()


def process_file(engine, path):
    monitoring = engine.get_directory(path)
    return len(monitoring.file_list) > 0


def process_files(engine, capt, path):
    capt.start()
    while process_file(engine, path):
        time.sleep(1)
    capt.stop()


def upload_files(engine, file_list, destination=''):
    for file in file_list:
        engine.send_file(file, destination)


def main(arg_list):
    options = Options(arg_list)
    if options.verbose or options.help:
        print(f'Process Files v{script_version}')

    if options.help:
        options.print_help()
        sys.exit(0)

    if not options.host:
        print("A host is required.")
        options.print_help()
        sys.exit(2)

    if not options.file_list:
        print("A file or list of files is required.")
        options.print_help()
        sys.exit(2)

    omni = omniscript.OmniScript()
    engine = options.create_engine(omni)
    if not engine:
        print('Failed to create the engine.')
        sys.exit(2)

    if not options.login(engine):
        print('Failed to connect to the engine')
        sys.exit(2)

    status = engine.get_status()
    data_path = status.data_directory

    # Check for needed plugins: FolderAdapterOE, CefPrefsOE-1
    module_list = engine.get_analysis_module_list()
    folder_adapter = omniscript.find_analysis_module(module_list, 'FolderAdapterOE')
    if folder_adapter is None:
        print('Failed to find FolderAdapterOE plugin.')
        sys.exit(2)

    cef_prefs_1 = omniscript.find_analysis_module(module_list, 'CefPrefsOE-1')
    if cef_prefs_1 is None:
        print('Failed to find the CefPrefsOE-1 plugin.')
        sys.exit(2)

    # Delete all existing Captures and Filters.
    capt_list = engine.get_capture_list()
    captures = omniscript.find_all_captures(capt_list, capture_name)
    if captures:
        engine.delete_capture(captures)

    fltr_list = engine.get_filter_list()
    filters = omniscript.find_all_filters(fltr_list, filter_name)
    if filters:
        engine.delete_filter(filters)

    # Find or create the Folder Adapter monitoring monitor_path.
    adpt = get_adapter(engine, folder_adapter, monitor_path)
    if not isinstance(adpt, omniscript.Adapter):
        print(f'Failed to find or create FolderAdapter monitoring {monitor_path}')
        sys.exit(2)

    # Create the filter.
    filter_comment = f'Filter {filter_address} and {cef_prefs_1.name}'
    fltr = create_filter(engine, filter_name, filter_comment, cef_prefs_1, filter_address)
    if not fltr:
        print('Failed to create Address Filter.')
        sys.exit(2)

    # Create the capture.
    capt = create_capture(engine, capture_name, capture_comment, adpt, cef_prefs_1, fltr)
    if capt is None:
        sys.exit(2)

    # Create the destination path on the engine if needed.
    files_path = str(PurePath(data_path, sub_dir))
    if sub_dir:
        data_dir = engine.get_directory(data_path)
        if files_path not in data_dir.directory_list:
            engine.create_directory(files_path)
            created_directory_list.append(files_path)

    upload_files(engine, options.file_list, files_path)

    move_files(options.host, options.user, files_path, monitor_path, options.file_list)

    # Start the capture, monitor the monitor_path, when it's empty stop the capture.
    process_files(engine, capt, monitor_path)

    # Clean-up
    engine.delete_capture(capt)
    engine.delete_filter(fltr)
    engine.delete_adapter(adpt)

    if created_directory_list:
        delete_directory_list(options.host, options.user, created_directory_list)


if __name__ == '__main__':
    main(sys.argv[1:])
