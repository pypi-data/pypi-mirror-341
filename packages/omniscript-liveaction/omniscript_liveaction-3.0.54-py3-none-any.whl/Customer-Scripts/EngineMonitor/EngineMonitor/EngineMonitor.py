"""EngineMonitor.py"""

import os
import sys
import getopt
import json
import socket
import keyring
import omniscript

from omniscript import ID_FLAG_NO_BRACES


script_version = '1.4.0'
token_dir = 'tokens'


def print_help():
    print("EngineMonitor")
    print('  -h : host IP Address or Name.')
    print('  -p : port. Default is 443.')
    print('  -u : user/account name')
    print('  -w : password')
    print('  -t : tokens directory. Default is "tokens/"')
    print('  -k : use keyring')
    print()
    print('Host, User Name and Password are required.')


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


def create_report(engine):
    status = engine.get_status()
    report = {
        'IP': status.address,
        'Port': status.port,
        'Version': status.file_version
    }
    lst = []
    captures = engine.get_capture_list()
    for c in captures:
        last_write = None
        el = engine.get_event_log(capture=c, query="Saved file:")
        el.get_next(-1)
        if len(el.entries) > 0:
            last_write = el.entries[-1].timestamp.iso_time()
        cr = {
            'IsCapturing': c.is_capturing(),
            'CaptureName': c.name,
            'Comment': c.comment,
            'LastModification': c.modification_type,
            'ModifiedBy': c.modified_by,
            'Received': c.packets_received,
            'Filtered': c.packets_filtered,
            'LastFileWrite': last_write,
            'Dropped': c.packets_dropped,
            'ID': c.id.format(ID_FLAG_NO_BRACES).lower()
        }
        lst.append(cr)
    report['Captures'] = lst
    return report


def engine_report(options):
    if 'host' not in options:
        print("A host is required.")
        print_help()
        sys.exit(2)
    host = options['host']
    port = options['port']
    user = options['user']
    pwd = options['pwd']
    if 'token_dir' in options:
        token_dir = options['token_dir']
    if options['keyring']:
        pwd = get_password(host, user)
        token = get_token(host, user)
    else:
        token_file = os.path.join(token_dir, 'f{host}-{port}.bin')
        if os.path.exists(token_file):
            with open(token_file, 'rb') as tf:
                token = tf.read()

    omni = omniscript.OmniScript()
    engine = omni.create_engine(host, port)

    if not engine.login(user, pwd, token):
        print('Failed to connect to the engine')
        return

    new_token = engine.get_session_token()
    if new_token and new_token != token:
        if options['keyring']:
            set_token(host, user, new_token)
        else:
            if os.path.exists(token_dir):
                os.create_p
            with open(token_file, 'wb') as tout:
                tout.write(new_token)

    report = create_report(engine)
    print(json.dumps(report, sort_keys=False, indent=4))


def parse_arguments(arglist):
    try:
        (opts, args) = getopt.getopt(arglist, "h:p:u:w:t:k?")
    except getopt.GetoptError as error:
        # print(help information and exit:)
        print(str(error))  # will print something like "option -a not recognized")
        print_help()
        sys.exit(2)

    options = {
        'port': 443,
        'user': None,
        'pwd': None,
        'token_dir': 'tokens',
        'keyring': False
    }

    for opt, arg in opts:
        if opt == '-h':
            options['host'] = arg
        elif opt == '-p':
            options['port'] = int(arg)
        elif opt == '-u':
            options['user'] = arg
        elif opt == '-w':
            options['pwd'] = arg
        elif opt in '-t':
            options['token_dir'] = arg
        elif opt == '-k':
            options['keyring'] = True
    return options


def main(args):
    print(f'EngineMonitor v{script_version}')
    options = parse_arguments(args)
    engine_report(options)


if __name__ == '__main__':
    main(sys.argv[1:])
