import sys
import argparse
import re
import requests
from urllib3 import disable_warnings

# Squelch the warning from the engine's self-signed certificate.
disable_warnings()

HTTP_SUCCESS = 200


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'host',
        default='localhost',
        help='The IP Address or the name of the system hosting the OmniEngine. '
        'Default is localhost.')
    parser.add_argument(
        '-port',
        '--port',
        type=int,
        default=443,
        help='The port number the OmniEngine web server is listening on. Default is 443.')
    parser.add_argument(
        '-v',
        '--verbose',
        action="store_true",
        help='Enable verbose output. Default is False.')
    settings = parser.parse_args(args)

    host = f'{settings.host}:{settings.port}'
    host_url = f'https://{host}'
    java_url = ''
    version = ''
    verbose = settings.verbose

    if verbose:
        print(f'Host URL: {host_url}')

    try:
        home = requests.get(host_url, verify=False)
    except Exception:
        print(f'Faled to get home page from: {host_url}')
        if home:
            print('Status code: {home.status_code}.')
            print('Reason: {home.reason}.')
        sys.exit(1)

    if home and home.status_code == HTTP_SUCCESS:
        page = str(home.text)
        if page is not None:
            if verbose:
                print(f'Size: {len(page):,} bytes')
            url = re.search(r'script[ \t].*src="(.*)"></script[ \t]*', page)
            if url is not None:
                # m = java.regs[0]
                if len(url.regs) > 1:
                    u_start, u_end = url.regs[1]
                    if verbose:
                        print(f'JavaScript page: {page[u_start:u_end]}')
                    java_url = f'https://{host}{page[u_start:u_end]}'
                else:
                    print('Did not JavaScript URL on {host}.')
                    sys.exit(1)
        else:
            print('Did not find javascript page on {host}.')
            sys.exit(1)

        if verbose:
            print(f'JavaScript URL: {java_url}')

        try:
            java = requests.get(java_url, verify=False)
        except Exception:
            print(f'Failed to get main javascript page from {host}.')
            if java:
                print('Status code: {java.status_code}.')
                print('Reason: {java.reason}.')
            sys.exit(1)

        if java and java.status_code == HTTP_SUCCESS:
            text = str(java.text)
            if verbose:
                print(f'Size: {len(text):,} bytes')
            ver = re.search(r'REACT_APP_VERSION:"([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)"', text)
            if ver is not None:
                # m = ver.regs[0]
                if len(ver.regs) > 1:
                    vs, ve = ver.regs[1]
                    version = text[vs:ve]
                    if verbose:
                        print(f'Engine Version: {version}')
                else:
                    print('Did not find OmniEngine Version on {host}.')
                    sys.exit(1)
        else:
            print(f'Failed to get main javascript page from {host}.')
            sys.exit(1)
    else:
        print(f'Failed to get home page from {host_url}')
        sys.exit(1)

    print(version)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        gary_dt2 = ['gary-dt2']
        edge_2 = ['edge-2']
        main(edge_2)
