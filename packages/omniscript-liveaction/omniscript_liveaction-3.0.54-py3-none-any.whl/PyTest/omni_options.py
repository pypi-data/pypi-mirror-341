"""omni_options.py"""

import os
import argparse
import keyring
import socket

import omniscript


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

    def __init__(self, script_name, arg_list=None):
        self.file_list = []
        self.host = omniscript.DEFAULT_HOST
        self.port = omniscript.DEFAULT_PORT
        self.secure = True
        self.user = 'root'
        self.password = None
        self.otp = None
        self.tokens_directory = 'tokens/'
        self.keyring = True
        self.timeout = None
        self.verbose = False
        self.help = False
        self._parser = Options._build_parser()
        if arg_list:
            self.parse_arguments(arg_list)

    @classmethod
    def _build_parser(cls):
        # Help will be added as the last argument so it's at the end of the help text.
        parser = argparse.ArgumentParser(prog='script_name', add_help=False)
        # Command line argument is 'files' but attribute is 'file_list', see parse_arguments().
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
            '--timeout', default=f'({omniscript.DEFAULT_CONNECTION_TIMEOUT}, '
            f'{omniscript.DEFAULT_REQUEST_TIMEOUT})',
            help='Engines HTTP Connection and Request timeout in seconds. (Default: %(default)s) '
            'To disable timeout set TIMEOUT to Off or None.')
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
            '--help', default=False, action='help', help='Display this help text.')
        return parser

    def create_engine(self, omni):
        return omni.create_engine(self.host, self.port, self.secure, self.timeout)

    def login(self, engine):
        if not engine:
            return False
        token = read_token_file(self.tokens_directory, self.host, self.port)
        if not token and self.keyring:
            token = get_token(self.host, self.user, self.port)
        try:
            if engine.login(self.user, self.password, self.otp, token, self.timeout):
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
            if engine.login(self.user, password, self.otp, None, self.timeout):
                new_token = engine.get_session_token()
                if new_token:
                    update_token_file(self.tokens_directory, self.host, self.port, new_token)
                    if self.keyring:
                        set_token(self.host, self.user, new_token)
                return True
        except Exception:
            pass

        result = engine.login(self.user, self.password, self.otp, None, self.timeout)
        if result and self.keyring:
            new_token = engine.get_session_token()
            set_token(self.host, self.user, new_token)

        return result

    def parse_arguments(self, arglist):
        settings = self._parser.parse_args(arglist)
        self.host = settings.host
        self.port = settings.port
        self.secure = settings.secure
        self.timeout = settings.timeout
        self.user = settings.user
        self.password = settings.password
        self.otp = settings.otp
        self.tokens_directory = settings.tokens_dir
        self.keyring = settings.keyring
        self.verbose = settings.verbose
        self.help = settings.help

    def print_help(self):
        self._parser.print_help()
