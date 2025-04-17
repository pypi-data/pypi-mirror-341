"""OmniScript 3.0 Python Test Script.
"""
# Copyright (c) LiveAction, Inc. 2022-2023. All rights reserved.
# Copyright (c) Savvius, Inc. 2013-2019. All rights reserved.
# Copyright (c) WildPackets, Inc. 2013-2014. All rights reserved.

# pylint: disable-msg=w0614

import os
import sys
import datetime
import time
import json
import tempfile
import paramiko
from contextlib import redirect_stdout
from pathlib import PurePath
from random import random

import addrelativepath
import omni_options

from omni_options import get_password

from omni_printers import (
    print_adapter_list, print_alarm_list, print_analysis_module_list, print_application_list,
    print_application_stats, print_application_flow_stats, print_call_stats,
    print_conversation_stats, print_country_stats,
    # print_error_stats, print_history_stats,
    print_network_stats, print_node_stats, print_protocol_stats, print_protocol_by_id_stats,
    print_size_stats, print_summary_snapshot,
    print_summary_stats, print_audit_log, print_capabilities, print_capture,
    print_capture_list, print_capture_session_list, print_capture_session_data,
    print_capture_template, print_capture_template_list,
    print_directory, print_engine_settings,
    print_engine_status, print_event_log, print_event_log_indexes, print_filter, print_filter_list,
    print_forensic_file_list, print_forensic_search_list, print_graph_template_list,
    print_liveflow_configuration, print_liveflow_context, print_liveflow_status,
    print_name_table, print_packet, print_protocol_list, print_remote_engine,
    print_remote_engine_list, print_user, print_user_list)

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from addrelativepath import addrelativepath

import omniscript
from omniscript.invariant import (
    BYTES_PER_MEGABYTE, BYTES_PER_GIGABYTE, SECONDS_PER_HOUR, TAP_TIMESTAMPS_DEFAULT)

# Do nothing code to satifiy Flake8 rules.
addrelativepath.do_addrelative_path()

port = None
domain = None
options = None

test_enabled = True
# test_enabled = False

bPerformance_Logging = False
bRestart = False

do_unit_tests = test_enabled

do_acl = test_enabled
do_adapters = test_enabled
do_audit_log = test_enabled
do_capt_create = test_enabled
do_capture_all = test_enabled
do_capture_stats = test_enabled
do_delete_all = test_enabled
do_event_log = test_enabled
do_file_ops = test_enabled
do_file_adapter = test_enabled
do_file_database_operations = test_enabled
do_filters = test_enabled
do_filter_all = test_enabled
do_flows = test_enabled
do_forensic_template = test_enabled
do_forensic_stats = test_enabled
do_gets = test_enabled
do_liveflow = test_enabled
do_miscellaneous = test_enabled
do_packets = test_enabled
do_remote_engine = test_enabled
do_reports = test_enabled
do_select_related = test_enabled
do_wireless = test_enabled

# Forensic Search needs the files db to be populated.
do_forensic_template_all = False

# do_legacy_connection = False
do_tcpdump_adapter = False
do_lauren_test = False

# Restart is broken
do_restart = False

capture_name = 'Python Test Script'
stats_capture_name = 'Python Stats Test Script'
adapter_capt_name = capture_name + ' - Fortworth'
save_all_name_engine = 'PythonTestScript_Engine.pkt'
save_all_name_capture = 'PythonTestScript_Capture.pkt'
filter_name = 'Python-Simple'
forensic_name = 'Python Forensic'
packet_file_name = 'fortworth101.pkt'
stats_file_names = ('10dot5_Morning.pcap', '8_calls_both_VandV.pcap')
packet_ipv6_file_name = 'More IPv6.pkt'
packets_needed = 3190
result_file = 'results.pkt'
fs_refresh_count = 10
report_name = 'Stats Report Test'
report_file = 'stats_report_test.pkt'
report_count = 2921
temp_path = tempfile.gettempdir() if sys.platform != 'win32' else r'C:\Temp'
self_file_path = os.path.abspath(os.path.dirname(__file__))
full_props = ''
with open(os.path.abspath(os.path.join(self_file_path, 'full_props.json')), 'rb') as f:
    full_props = json.load(f)

if not os.path.exists(temp_path):
    os.mkdir(temp_path)

_file_path = os.path.dirname(__file__)
shared_files = os.path.abspath(os.path.join(_file_path, r'../../../../files'))
_test_file = os.path.join(shared_files, packet_file_name)
if not os.path.isfile(_test_file):
    shared_files = os.path.abspath(os.path.join(_file_path, r'../../files'))
    _test_file = os.path.join(shared_files, packet_file_name)
    if not os.path.isfile(_test_file):
        shared_files = os.path.abspath(os.path.join(_file_path, r'../files'))
        _test_file = os.path.join(shared_files, packet_file_name)
        if not os.path.isfile(_test_file):
            shared_files = os.path.abspath(os.path.join(_file_path, r'files'))
            _test_file = os.path.join(shared_files, packet_file_name)
            if not os.path.isfile(_test_file):
                print('shared_files path not found.')
                sys.exit(1)

fortworth_capture = [capture_name, packet_file_name, packets_needed]
ipv6_capture = [capture_name, packet_ipv6_file_name, 710]

node_report = ('Report_Nodes-ip_py.txt',
               'Report_Nodes-ipv6_py.txt', 'Report_Nodes-eth_py.txt')
protocol_report = 'Report_Protocols_py.txt'
summary_report = 'Report_Summary_py.txt'

node_columns = [
    omniscript.NODE_COLUMN_BYTES_SENT,
    omniscript.NODE_COLUMN_BYTES_RECEIVED,
    omniscript.NODE_COLUMN_PACKETS_SENT,
    omniscript.NODE_COLUMN_PACKETS_RECEIVED,
    omniscript.NODE_COLUMN_BROADCAST_PACKETS,
    omniscript.NODE_COLUMN_BROADCAST_BYTES,
    omniscript.NODE_COLUMN_MULTICAST_PACKETS,
    omniscript.NODE_COLUMN_MULTICAST_BYTES,
    omniscript.NODE_COLUMN_MIN_SIZE_SENT,
    omniscript.NODE_COLUMN_MAX_SIZE_SENT,
    omniscript.NODE_COLUMN_MIN_SIZE_RECEIVED,
    omniscript.NODE_COLUMN_MAX_SIZE_RECEIVED,
    omniscript.NODE_COLUMN_FIRST_TIME_SENT,
    omniscript.NODE_COLUMN_LAST_TIME_SENT,
    omniscript.NODE_COLUMN_FIRST_TIME_RECEIVED,
    omniscript.NODE_COLUMN_LAST_TIME_RECEIVED
]

E_TIMEOUT = 0x800705B4

BS = '\\'

# def dummy_dummy():
#     """Call imported but unused functions."""
#     find_alarm([], '')
#     find_capture([], '')
#     find_decryption_key([], '')
#     find_protocol([], '')
#     find_graph_template([], '')
#     find_remote_engine([], '')


class Remote(object):
    def __init__(self, host, user):
        self.host = host
        self.user = user
        self.ssh = None

    def connect(self) -> None:
        self.disconnect()
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.RejectPolicy())
        self.ssh.load_system_host_keys()
        password = omni_options.get_password(self.host, self.user)
        if not password:
            raise Exception(f"Replay password for {self.user} was not provided nor set in keyring.")
        self.ssh.connect(self.host, 22, self.user, password)

    def disconnect(self) -> None:
        if self.ssh:
            self.ssh.close()
            self.ssh = None

    def get_url(self, url):
        if not self.ssh:
            self.connect()
        _, _, _ = self.ssh.exec_command(f'curl {url}')


def capture_template(engine):
    if not engine:
        return None
    ct = omniscript.CaptureTemplate()
    adpt = get_default_adapter(engine)
    if adpt:
        ct.set_adapter(adpt)
    else:
        return None
    ct.general.option_continuous_capture = True
    ct.general.option_capture_to_disk = True
    ct.general.option_start_capture = False
    ct.general.option_timeline_app_stats = True
    ct.general.option_timeline_stats = True
    ct.general.option_timeline_top_stats = True
    ct.general.option_timeline_voip_stats = True
    ct.analysis.set_all(True)
    return ct


# use_file_db = True
# try:
#     OMNI_USEFILEDB = os.environ['OMNI_USEFILEDB']
#     if len(OMNI_USEFILEDB) > 0:
#         use_file_db = int(OMNI_USEFILEDB) != 0
# except KeyError as err:
#     pass


def create_ip_filter(name, ip_addr):
    ip_filter = omniscript.Filter(name)
    addr_node = omniscript.AddressNode()
    addr_node.address_1 = omniscript.IPv4Address(str(ip_addr))
    addr_node.accept_1_to_2 = True
    addr_node.accept_2_to_1 = True
    ip_filter.criteria = addr_node
    return ip_filter


def login_to_engine(engine, auth, domain, user, pwd, token=None):
    if not engine:
        return False
    if engine.is_connected():
        return True
    return engine.login(user, pwd, token)


def get_default_adapter(engine, name=None):
    al = engine.get_adapter_list()
    if name is not None:
        d = omniscript.find_adapter(al, name)
        if d is not None:
            return d
    d = omniscript.find_adapter(al, 'eth0')
    if d is None:
        d = omniscript.find_adapter(al, 'eno3')
    return d


def get_folder_adapter(engine, folder):
    module_list = engine.get_analysis_module_list()
    folder_adapter = omniscript.find_analysis_module(module_list, 'FolderAdapterOE')
    if folder_adapter is None:
        print('Failed to find FolderAdapterOE plugin.')
        sys.exit(2)

    # create the monitoring folder if it doesn't exist.
    remote_make_dir(options.host, options.user, folder)

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
    engine.send_plugin_message(folder_adapter, create_adapter_msg)

    adpt_list = engine.get_adapter_list()
    adpt = omniscript.find_adapter(adpt_list, folder)
    return adpt


def get_traffic():
    root = 'https://www.liveaction.com/resources/'
    pages = [
        'blog-post/maximizing-efficiency-in-it-and-security-budgets-a-strategic-approach-2/',
        ('blog-post/the-importance-of-capturing-both-flow-and-network-packets-to-support-netops-'
         'teams-and-use-cases/'),
        'blog-post/enhancing-the-management-visibility-and-security-of-cisco-sase/',
        'blog-post/enhancing-network-visibility-the-synergy-of-gigamon-and-liveaction/',
        'blog-post/deeper-network-insights-for-sd-wan-deployments/',
        'blog-post/mitigating-the-impact-of-unplanned-downtime-in-manufacturing/',
        'whitepapers/network-monitoring-and-analytics-to-enhance-cisco-fso/',
        'whitepapers/liveaction-thousandeyes-complementary-features-key-differences/',
        'event/cisco-live-us-2024/'
    ]

    ssh = Remote(options.host, options.user)
    ssh.connect()
    for page in pages:
        url = root + page
        ssh.get_url(url)
    ssh.disconnect()


def load_forensic_search(fs):
    max_count = 10
    timeout = 0
    # or while fs.status == FORENSIC_OPENING
    while fs.status < omniscript.FORENSIC_COMPLETE:
        time.sleep(1)
        fs.refresh()
        timeout += 1
        if timeout > max_count:
            break
    fs.refresh()
    return (fs.status == omniscript.FORENSIC_COMPLETE)


def remote_copy_file(host, user, filename, destination):
    dest_path = PurePath(destination)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    # self.ssh.set_combine_stderr()
    password = get_password(host, user)
    if not password:
        raise Exception(f"Failed to get password for {user} was not provided nor set in keyring.")
    ssh.connect(host, 22, user, password)
    cmd = f'cp {filename} {dest_path}{os.sep}'
    ssh.exec_command(cmd)


def remote_make_dir(host, user, directory):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    # self.ssh.set_combine_stderr()
    password = get_password(host, user)
    if not password:
        raise Exception(f"Failed to get password for {user} was not provided nor set in keyring.")
    ssh.connect(host, 22, user, password)
    cmd = f'if [ ! -d {directory} ] ; then mkdir {directory}; fi'
    ssh.exec_command(cmd)


def send_file(ssh, local_path, remote_path=None):
    """
    Send a file via SCP to the remote device.

    :param local_path: File name, or path and file name, for file on
        local system
    :param remote_path: Full path and name of file on remote host
    :return:
    """
    try:
        # Create an SCP client
        scp = ssh.open_sftp()

        if not remote_path:
            lp = PurePath(local_path)
            destination = f"./{lp.name}"
        else:
            destination = remote_path

        # Upload the file
        scp.put(local_path, destination)
    finally:
        # Close the SCP connection (Does not close SSH connection)
        scp.close()

    return destination


# def create_capture(engine, capture_name, capture_file, packets_needed):
#     time.sleep(1)
#     failures = 0
#     capt = None
#     try:
#         fl = engine.get_file_list()
#         ffi = list(i for i in fl if i.name == capture_file)
#         if len(ffi) == 0:
#             sf_filename = os.path.normpath(os.path.join(shared_files, capture_file))
#             engine.send_file(sf_filename)
#             fl = engine.get_file_list()
#             ffi = list(i for i in fl if i.name == capture_file)
#             if len(ffi) == 0:
#                 print('*** Failed to send file to engine: %s' % capture_file)
#                 return None
#     except Exception:
#         failures += 1

#     try:
#         cl = engine.get_capture_list()
#         cli = list(i for i in cl if i.name == capture_name)
#         engine.delete_capture(cli)
#     except Exception:
#         failures += 1

#     try:
#         cf_path = fl[0].name + capture_file # do not use os.path.join.
#         fa = omniscript.FileAdapter(cf_path)
#         fa.limit = 1
#         fa.speed = 0.0

#         ct = omniscript.CaptureTemplate()
#         ct.set_adapter(fa)
#         ct.general.name = capture_name
#         ct.general.option_continuous_capture = True
#         ct.general.option_capture_to_disk = True
#         ct.general.option_start_capture = False
#         ct.set_all(True)
#         capt = engine.create_capture(ct)
#         if capt is None:
#             return None
#     except Exception:
#         failures += 1

#     try:
#         capt.start()
#         capt.refresh()
#         while (capt.status & 0x0001) and (capt.packets_filtered < packets_needed):
#             time.sleep(3)
#             capt.refresh()
#     except Exception:
#         failures += 1

#     try:
#         capt.stop()
#         capt.refresh()
#     except Exception:
#         failures += 1

#     return capt


# def query_expert_counts(engine):
#     failures = 0

#     try:
#         ft = omniscript.ForensicTemplate()
#         ft.name = 'ForensicSearch-Expert'
#         ft.option_expert = True
#         ft.option_packets = True
#         ft.option_summary = True

#         fs = engine.create_forensic_search(ft)

#         query = omniscript.ExpertQuery('HEADER_COUNTERS')
#         results = fs.query_expert(query)
#         print_expert_result_list(results)
#     except Exception:
#         failures += 1
#     return failures


# def query_expert_short(engine, context):
#     failures = 0

#     if not context:
#         return 1

#     try:
#         query = [omniscript.ExpertQuery('STREAM'), omniscript.ExpertQuery('EVENT_LOG')]
#         query[0].columns = ['STREAM_ID', 'CLIENT_ADDRESS', 'CLIENT_PORT',
#                             'SERVER_ADDRESS', 'SERVER_PORT']
#         query[0].order = ['STREAM_ID']
#         query[0].row_count = 100

#         query[1].columns = ['PROBLEM_ID', 'STREAM_ID', 'MESSAGE']
#         query[1].order = ['PROBLEM_ID']
#         query[1].where = ['informational', 'minor', 'major', 'severe']
#         query[1].row_count = 100

#         results = context.query_expert(query)
#         for r in results[0].rows:
#             cip = omniscript.parse_ip_address(r['CLIENT_ADDRESS'])
#             sip = omniscript.parse_ip_address(r['SERVER_ADDRESS'])
#             print('%d [%s]:%d [%s]:%d' % (r['STREAM_ID'], str(cip), r['CLIENT_PORT'],
#                   str(sip), r['SERVER_PORT']))
#         for r in results[1].rows:
#             print('%3d %3d %s' % (r['PROBLEM_ID'], r['STREAM_ID'], r['MESSAGE']))
#         print
#     except Exception:
#         failures += 1

#     return failures


# def query_expert_long(engine, context):
#     failures = 0

#     if not context:
#         return 1

#     try:
#         # 4 Queries Peek Makes when updating Expert - Flows.
#         q_stream = [
#             omniscript.ExpertQuery('STREAM'),
#             omniscript.ExpertQuery('EVENT_LOG'),
#             omniscript.ExpertQuery('EVENT_COUNTS'),
#             omniscript.ExpertQuery('HEADER_COUNTERS')
#             ]
#         q_stream[0].columns = [
#             'TYPE',
#             'HIGHLIGHT',
#             'TREE_STATE',
#             'EVENT_SEVERITY_MAX',
#             'EVENT_TIME',
#             'START_TIME',
#             'END_TIME',
#             'NODEPAIR',
#             'FLOW_TYPE',
#             'STREAM_ID',
#             'PROBLEM_ID',
#             'CLIENT_PORT',
#             'SERVER_PORT',
#             'THROUGHPUT_CLIENT_TO_SERVER_BITS_PER_SECOND',
#             'THROUGHPUT_SERVER_TO_CLIENT_BITS_PER_SECOND',
#             'THROUGHPUT_CLIENT_TO_SERVER_BITS_PER_SECOND_BEST',
#             'THROUGHPUT_SERVER_TO_CLIENT_BITS_PER_SECOND_BEST',
#             'THROUGHPUT_CLIENT_TO_SERVER_BITS_PER_SECOND_WORST',
#             'THROUGHPUT_SERVER_TO_CLIENT_BITS_PER_SECOND_WORST',
#             'THROUGHPUT_CLIENT_TO_SERVER_SAMPLE_COUNT',
#             'THROUGHPUT_SERVER_TO_CLIENT_SAMPLE_COUNT',
#             'CLIENT_START_TIME',
#             'SERVER_START_TIME',
#             'CLIENT_END_TIME',
#             'SERVER_END_TIME',
#             'CLIENT_HOP_COUNT',
#             'SERVER_HOP_COUNT',
#             'CLIENT_TCP_WINDOW_MIN',
#             'SERVER_TCP_WINDOW_MIN',
#             'CLIENT_TCP_WINDOW_MAX',
#             'SERVER_TCP_WINDOW_MAX',
#             'PROBLEM_SUMMARY_LIST',
#             'CLIENT_ADDRESS',
#             'SERVER_ADDRESS',
#             'CLIENT_SENT_PACKET_COUNT',
#             'SERVER_SENT_PACKET_COUNT',
#             'CLIENT_SENT_BYTE_COUNT',
#             'SERVER_SENT_BYTE_COUNT',
#             'DELAY',
#             'DELAY_BEST',
#             'DELAY_WORST',
#             'DELAY_SAMPLE_COUNT',
#             'PROBLEM_COUNT',
#             'PROTOCOL',
#             'APPLICATION',
#             'PACKET_COUNT',
#             'BYTE_COUNT',
#             'DURATION',
#             'THREE_WAY_HANDSHAKE_TIME',
#             'TCP_STATUS'
#             ]
#         q_stream[0].order = ['STREAM_ID', 'CLIENT_ADDRESS', 'PROBLEM_ID']
#         q_stream[0].row_count = 72

#         q_stream[1].columns = [
#             'TYPE',
#             'PROBLEM_ID',
#             'STREAM_ID',
#             'EVENT_SERIAL_NUMBER',
#             'EVENT_SEVERITY_MAX',
#             'EVENT_TIME',
#             'PROTOCOL_LAYER',
#             'MESSAGE',
#             'SOURCE_ADDRESS',
#             'DEST_ADDRESS',
#             'SOURCE_PORT',
#             'DEST_PORT',
#             'PACKET_NUMBER',
#             'OTHER_PACKET_NUMBER',
#             'IS_FROM_CLIENT',
#             'NODEPAIR',
#             'PROTOSPEC',
#             'REQUEST_ID',
#             'CALL_ID',
#             'FLOW_INDEX'
#             ]
#         q_stream[1].order = ['EVENT_TIME', 'PACKET_NUMBER', 'EVENT_SERIAL_NUMBER']
#         q_stream[1].where = ['informational', 'minor', 'major', 'severe']
#         q_stream[1].row_count = 24

#         q_stream[2].columns = [
#             'PROBLEM_ID',
#             'EVENT_NAME',
#             'PROBLEM_COUNT',
#             'EVENT_SEVERITY_MAX',
#             'PROTOCOL_LAYER',
#             'START_TIME',
#             'END_TIME'
#             ]
#         q_stream[2].order = ['PROBLEM_ID']
#         q_stream[2].row_count = sys.maxsize
#         q_stream[2].view_settings.time_precision = 'nanoseconds'
#         q_stream[2].view_settings.option_address_names = False
#         q_stream[2].view_settings.option_port_names = False

#         q_stream[3].row_count = sys.maxsize
#         q_stream[3].view_settings.time_precision = 'nanoseconds'
#         q_stream[3].view_settings.option_address_names = False
#         q_stream[3].view_settings.option_port_names = False

#         if False:
#             results = context.query_expert(q_stream)
#             rs = next((r for r in results if r.table == 'STREAM'), None)
#             if rs:
#                 for r in rs.rows:
#                     cip = omniscript.parse_ip_address(r['CLIENT_ADDRESS'])
#                     sip = omniscript.parse_ip_address(r['SERVER_ADDRESS'])
#                     print('%d %s:%d %s%d' % (r['STREAM_ID'], str(cip), r['CLIENT_PORT'],
#                                              str(sip), r['SERVER_PORT']))
#         print
#     except Exception:
#         failures += 1
#     return failures


def test_unit_tests(engine):
    print('Unit Test')
    failures = 0
    messages = ['Unit Tests']

    # Testing OmniId
    id = omniscript.OmniId()
    id.new()
    txt = str(id)
    print('New id: %s' % txt)
    idp = omniscript.OmniId()
    idp.parse(txt)
    if id != idp:
        messages.append('OmniId new/parse failure.')
        failures += 1

    # Testing PeekTime
    pt1 = omniscript.PeekTime()
    time.sleep(2)
    pt2 = omniscript.PeekTime()
    df = pt2 - pt1
    if df.value > (10 * 1000000000):
        messages.append('Failure in PeekTime subtraction.')
        failures += 1

    try:
        pt3 = omniscript.PeekTime('2022-08-30T00:08:18.105796123Z')
        pt3_iso = pt3.iso_time()
        print(f'Time 2022-08-30T00:08:18.105796123Z is {pt3_iso}')
        if pt3_iso != '2022-08-30T00:08:18.105796123Z':
            messages.append('Failed to match pt3.')
            failures += 1
    except Exception:
        messages.append('PeekTime failed to parse pt3: 2022-08-30T00:08:18.105796123Z')
        failures += 1

    try:
        pt4 = omniscript.PeekTime('2022-08-30T00:08:18.105796123')
        pt4_iso = pt4.iso_time()
        print(f'Time 2022-08-30T00:08:18.105796123 is  {pt4_iso}')
        if pt4_iso != '2022-08-30T00:08:18.105796123Z':
            messages.append('Failed to match pt4.')
            failures += 1
    except Exception:
        messages.append('PeekTime failed to parse pt4: 2022-08-30T00:08:18.105796123')
        failures += 1

    try:
        pt5 = omniscript.PeekTime('2022-08-30T00:08:18.105796Z')
        pt5_iso = pt5.iso_time()
        print(f'Time 2022-08-30T00:08:18.105796Z is    {pt5_iso}')
        if pt5_iso != '2022-08-30T00:08:18.105796000Z':
            messages.append('Failed to match pt5.')
            failures += 1
    except Exception as e:
        messages.append(f'  {str(e.args[0])}')
        failures += 1

    try:
        pt6 = omniscript.PeekTime('2022-08-30T00:08:18.105796')
        pt6_iso = pt6.iso_time()
        print(f'Time 2022-08-30T00:08:18.105796 is     {pt6_iso}')
        if pt6_iso != '2022-08-30T00:08:18.105796000Z':
            messages.append('Failed to match pt6.')
            failures += 1
    except Exception:
        messages.append('PeekTime failed to parse pt6: 2022-08-30T00:08:18.105796')
        failures += 1

    try:
        pt7 = omniscript.PeekTime('2022-08-30T00:08:18.105796987Z')
        pt7_iso = pt7.iso_time()
        print(f'Time 2022-08-30T00:08:18.105796987Z is {pt7_iso}')
        if pt7_iso != '2022-08-30T00:08:18.105796987Z':
            messages.append('Failed to match pt7.')
            failures += 1
    except Exception:
        messages.append('PeekTime failed to parse pt7: 2022-08-30T00:08:18.105796987Z')
        failures += 1

    try:
        pt8 = omniscript.PeekTime('2022-08-30T00:08:18.105796987-0700')
        pt8_iso = pt8.iso_time()
        print(f'Time 2022-08-30T00:08:18.105796987-0700 is {pt8_iso}')
        if pt8_iso != '2022-08-30T07:08:18.105796987Z':
            messages.append('Failed to match pt8.')
            failures += 1
    except Exception:
        messages.append('PeekTime failed to parse pt8: 2022-08-30T00:08:18.105796987-0700')
        failures += 1

    try:
        pt9 = omniscript.PeekTime('2022-08-30T00:08:18.105796987-07:00')
        pt9_iso = pt9.iso_time()
        print(f'Time 2022-08-30T00:08:18.105796987-0700 is {pt9_iso}')
        if pt9_iso != '2022-08-30T07:08:18.105796987Z':
            messages.append('Failed to match pt9.')
            failures += 1
    except Exception:
        messages.append('PeekTime failed to parse pt9: 2022-08-30T00:08:18.105796987-0700')
        failures += 1

    try:
        ptA = omniscript.PeekTime('2022-08-30T00:08:18.105796987-07')
        ptA_iso = ptA.iso_time()
        print(f'Time 2022-08-30T00:08:18.105796987-07 is {ptA_iso}')
        if pt9_iso != '2022-08-30T07:08:18.105796987Z':
            messages.append('Failed to match ptA.')
            failures += 1
    except Exception:
        messages.append('PeekTime failed to parse ptA: 2022-08-30T00:08:18.105796987-07')
        failures += 1

    try:
        ptB = omniscript.PeekTime('2022-08-30T08:08:18.105796987+0800')
        ptB_iso = ptB.iso_time()
        print(f'Time 2022-08-30T08:08:18.105796987+0800 is {ptB_iso}')
        if ptB_iso != '2022-08-30T00:08:18.105796987Z':
            messages.append('Failed to match ptB.')
            failures += 1
    except Exception:
        messages.append('PeekTime failed to parse ptB: 2022-08-30T08:08:18.105796987+0800')
        failures += 1

    try:
        ptC = omniscript.PeekTime('2022-08-30T08:08:18.105796987+08:00')
        ptC_iso = ptC.iso_time()
        print(f'Time 2022-08-30T08:08:18.105796987+08:00 is {ptC_iso}')
        if ptC_iso != '2022-08-30T00:08:18.105796987Z':
            messages.append('Failed to match ptC.')
            failures += 1
    except Exception:
        messages.append('PeekTime failed to parse ptC: 2022-08-30T08:08:18.105796987+08:00')
        failures += 1

    try:
        ptD = omniscript.PeekTime('2022-08-30T08:08:18.105796987+08')
        ptD_iso = ptD.iso_time()
        print(f'Time 2022-08-30T08:08:18.105796987+08 is {ptD_iso}')
        if ptD_iso != '2022-08-30T00:08:18.105796987Z':
            messages.append('Failed to match ptD.')
            failures += 1
    except Exception:
        messages.append('PeekTime failed to parse ptD: 2022-08-30T08:08:18.105796987+08')
        failures += 1

    # From 1/1/1601 to 12/31/2022 including the last day:
    #            421 years, 11 months, 30 days
    #          5,064 months
    #         22,018 weeks, 5 days
    #        154,131 days
    #      3,699,144 hours
    #    221,948,640 minutes
    # 13,316,918,400 seconds

    pto_0 = omniscript.PeekTime(0)
    pto_0_iso = pto_0.iso_time()
    print(pto_0_iso)
    pto_1 = omniscript.PeekTime(pto_0_iso)
    pto_1_iso = pto_1.iso_time()
    print(pto_1_iso)

    # Testing IPv4 Address parsing with CIDR and Wildcards (*).
    ip = omniscript.IPv4Address('10.8.100.65')
    if str(ip) != '10.8.100.65':
        messages.append(f'{"10.8.100.65":>15}: {ip}')
        failures += 1

    ip20 = omniscript.IPv4Address('10.8.100.*')
    print(f'{"10.8.100.*":>15}: {ip20}')
    ip21 = omniscript.IPv4Address('10.8.*.*')
    print(f'{"10.8.*.*":>15}: {ip21}')
    ip22 = omniscript.IPv4Address('10.*.*.*')
    print(f'{"10.*.*.*":>15}: {ip22}')

    ip10 = omniscript.IPv4Address('10.8.100.65/24')
    print(f'{"10.8.100.65/24":>15}: {ip10}')
    ip11 = omniscript.IPv4Address('10.8.100.65/16')
    print(f'{"10.8.100.65/16":>15}: {ip11}')
    ip12 = omniscript.IPv4Address('10.8.100.65/8')
    print(f'{"10.8.100.65/8":>15}: {ip12}')
    ip13 = omniscript.IPv4Address('10.8.100.65/32')
    print(f'{"10.8.100.65/32":>15}: {ip13}')

    # Check for new Expert Events.
    id_expert_names = omniscript.get_id_expert_names()
    id_stat_names = omniscript.get_id_stat_names()
    missing = []
    for k, v in id_expert_names.items():
        if k not in id_stat_names:
            missing.append(id_expert_names[k])
    if len(missing) > 0:
        messages.append('Failure in id_sxpert_nsame')
        failures += 1

    id_graph_names = omniscript.get_id_graph_names()
    print(f'\nGraph Name: {len(id_graph_names)}')
    print(f'{"id":5}: Value')
    for k, v in sorted(id_graph_names):
        print(f'{k:5}: {v}')

    id_protocol_names = omniscript.get_id_protocol_names()
    print('\nProtocol Id and Name list: ')
    print(f'{"id":5}: Value')
    for k, v in sorted(id_protocol_names.items()):
        print(f'{k:5}: {v}')

    id_protocol_short_names = omniscript.get_id_protocol_short_names()
    print('\nProtocol Id and Short Name list: ')
    print(f'{"id":5}: Value')
    for k, v in sorted(id_protocol_short_names.items()):
        print(f'{k:5}: {v}')

    protocol_short_names = omniscript.get_protocol_short_name_ids()
    print('\nProtocol Short Name and Id list: ')
    print(f'{"id":50}: Value')
    for k, v in sorted(protocol_short_names.items()):
        print(f'{k:50}: {v}')

    expert_problem_ids = omniscript.get_expert_problem_id()
    print('\nExpert Problem and Id list: ')
    print(f'{"id":3}: Value')
    for k, v in sorted(expert_problem_ids.items()):
        print(f'{k:5}: {v}')

    # Search for problems...
    r = []
    s = 'DNS'.lower()
    for k, v in expert_problem_ids.items():
        if s in k.lower():
            r.append(v)
    print(len(r))

    fl = engine.get_filter_list()
    # for f in fl:
    #     props = f._store()
    #     print(props)

    for f in fl:
        if isinstance(f.criteria, omniscript.AddressNode):
            print(f.criteria.to_string(4, 'op'))
        if isinstance(f.criteria, omniscript.PortNode):
            print(f.criteria.to_string(4, 'op'))
        #     if isinstance(f.criteria.address_1, list):
        #         if len(f.criteria.address_1) > 1:
        #             print(f'found address_1 list: {f.name} : count {len(f.criteria.address_1)}')
        #     if isinstance(f.criteria.address_2, list):
        #         if len(f.criteria.address_2) > 1:
        #             print(f'found address_2 list: {f.name} : count {len(f.criteria.address_2)}')

        # if isinstance(f.criteria, PortNode):
        #     if isinstance(f.criteria.port_1, list):
        #         if len(f.criteria.port_1) > 1:
        #             print(f'found port_1 list: {f.name} : count {len(f.criteria.port_1)}')
        #     if isinstance(f.criteria.port_2, list):
        #         if len(f.criteria.port_2) > 1:
        #             print(f'found port_2 list: {f.name} : count {len(f.criteria.port_2)}')

    # Testing start/stop capture's xml_capture_list method.
    cl = engine.get_capture_list()
    if cl:
        for c in cl:
            if c.name == 'Super Capture':
                ct = c.get_capture_template()
                ct.general.name += '1'
                engine.create_capture(ct)
    captures = [i for i in cl if i.name[:7] == 'Capture']

    # capt = captures[0]
    # pkts = capt.get_packets(capt.first_packet, capt.packet_count)

    # engine.delete_capture(captures)

    ct = omniscript.CaptureTemplate()
    adpt = get_default_adapter(engine)
    if adpt:
        ct.set_adapter(adpt)
    ct.general.option_continuous_capture = True
    ct.general.option_capture_to_disk = True
    ct.general.option_start_capture = False
    ct.general.option_timeline_app_stats = True
    ct.general.option_timeline_stats = True
    ct.general.option_timeline_top_stats = True
    ct.general.option_timeline_voip_stats = True
    ct.analysis.option_alarms = True
    ct.analysis.option_analysis_modules = True
    ct.analysis.option_application = True
    ct.analysis.option_compass = True
    ct.analysis.option_country = True
    ct.analysis.option_error = True
    ct.analysis.option_expert = True
    ct.analysis.option_network = True
    ct.analysis.option_passive_name_resolution = True
    ct.analysis.node_protocol_detail_limit.enabled = True
    ct.analysis.node_limit.enabled = True
    ct.analysis.protocol_limit.enabled = True
    ct.analysis.option_size = True
    ct.analysis.option_summary = True
    ct.analysis.option_traffic_history = True
    ct.analysis.option_voice_video = True
    ct.analysis.option_web = True

    ct.general.name = 'Capture 1'
    c1 = engine.create_capture(ct)
    if not c1:
        messages.append('Failed to create Capture 1.')
        failures += 1

    ctl = engine.get_capture_template_list()
    print_capture_template_list(ctl)

    ct.general.name = 'Capture 2'
    c2 = engine.create_capture(ct)
    if not c2:
        messages.append('Failed to create Capture 2')
        failures += 1

    ct.general.name = 'Capture 3'
    c3 = engine.create_capture(ct)
    if not c3:
        messages.append('Failed to create Capture 3')
        failures += 1

    time.sleep(2)
    cl = engine.get_capture_list()
    captures = [i for i in cl if i.name[:7] == 'Capture']
    if len(captures) > 2:
        try:
            engine.start_capture(captures[1])
            engine.start_capture(captures)
            engine.stop_capture(captures[0])
            engine.stop_capture(captures)
        except omniscript.OmniError as e:
            messages.append(f'Start/Stop failure: {e.message}')
            failures += 1

    time.sleep(5)
    capt = cl[0]
    _running = capt.is_capturing(False)
    print(_running)
    capt.start()
    capt.start()
    capt.start()
    capt.stop()
    capt.stop()
    capt.stop()

    # for c in cl:
    #     engine.delete_capture(c)

    band_id_names = omniscript.get_wireless_band_id_names()
    for k, v in band_id_names.items():
        print(f'{k}: {v}')

    if failures:
        messages.append(f'Unit Tests Failures: {failures}')
    return failures, messages


def test_adapters(engine):
    print('Adapter Test')
    failures = 0

    al = engine.get_adapter_list()
    print_adapter_list(al)
    if len(al) > 0:
        a = engine.find_adapter(al[0].name)
        if not a:
            print('*** Failed to find first adapter by name.')
            failures += 1
        a = engine.find_adapter(al[0].adapter_id, 'id')
        if not a:
            print('*** Failed to find first adapter by id.')
            failures += 1
        if len(al[0].device_name) > 0:
            a = engine.find_adapter(al[0].device_name, 'device_name')
            if not a:
                print('*** Failed to find first adapter by device name.')
                failures += 1

    print()
    return failures


def test_audit_log(engine):
    print('Audit Log Test')
    failures = 0

    # get_audit_log(offset, limit, search, client, user, start, stop)
    offset = 0
    try:
        al_prime = engine.get_audit_log(offset, 10)
        print('Audit Log: Prime')
        print_audit_log(al_prime)
        max_prime = min(al_prime.total_count, 200)
        while offset < max_prime:
            offset += 10
            al_temp = engine.get_audit_log(offset, 10)
            print_audit_log(al_temp)
    except Exception:
        failures += 1

    # When querying the Audit Log, the offset is based on the number of matches,
    # not the total_count.
    try:
        status = engine.get_status()
        al_user = engine.get_audit_log(1, 1, user=status.user_name)
        print('Audit Log: User')
        print_audit_log(al_user)
    except Exception:
        failures += 1

    try:
        offset = 0
        max_user = min(al_user.count, 200)
        while offset < max_user:
            offset += 10
            al_user_temp = engine.get_audit_log(offset, 10, user=status.user_name)
            print_audit_log(al_user_temp)
    except Exception:
        failures += 1

    if al_user.message_count > 0:
        client = al_user.message_list[0].client
        al_client = engine.get_audit_log(1, 1, client=client)
        print('Audit Log: Client')
        print_audit_log(al_client)

        offset = 0
        max_client = min(al_client.count, 200)
        while offset < max_client:
            offset += 10
            al_client_temp = engine.get_audit_log(offset, 10, client=client)
            print_audit_log(al_client_temp)

    try:
        al_login = engine.get_audit_log(1, 1, search='Successful Login', user=status.user_name)
        print('Audit Log: Successful Login')
        print_audit_log(al_login)

        offset = 0
        max_login = min(al_login.count, 200)
        while offset < max_login:
            offset += 10
            al_login_temp = engine.get_audit_log(offset, 10, search='Successful Login',
                                                 user=status.user_name)
            print_audit_log(al_login_temp)
    except Exception:
        failures += 1

    return failures


def test_capt_create(engine, capture_name, filter_name, needed_packets):
    print('Capture Creation Test')
    failures = 0

    cl = engine.get_capture_list()
    capt_list = [c for c in cl if c.name[:len(capture_name)] == capture_name]
    engine.delete_capture(capt_list)

    # gtl = engine.get_graph_template_list()
    # gtl_sublist = []
    # for i, v in enumerate(gtl):
    #     if i % 2:
    #         gtl_sublist.append(v)

    adpt = get_default_adapter(engine)

    ca = omniscript.CaptureTemplate()
    if adpt:
        ca.set_adapter(adpt)
    ca.general.name = capture_name
    ca.general.buffer_size = 10 * BYTES_PER_MEGABYTE
    ca.general.comment = 'Python generated capture.'
    ca.general.directory = os.path.join(temp_path, 'Capture Files')
    ca.general.file_pattern = capture_name + '-'
    ca.general.file_size = 128 * BYTES_PER_MEGABYTE
    ca.general.keep_last_files_count = 5
    ca.general.max_file_age = SECONDS_PER_HOUR
    ca.general.max_total_file_size = BYTES_PER_MEGABYTE
    ca.general.slice_length = 256
    ca.general.tap_timestamps = omniscript.TAP_TIMESTAMPS_DEFAULT
    ca.general.option_capture_to_disk = True
    ca.set_all(True)
    ca.indexing.set_all(True)
    ca.plugins.set_all(True)
    ca.plugins.modules = []
    ca.filter.mode = omniscript.FILTER_MODE_ACCEPT_MATCHING_ANY
    ca.add_filter(filter_name)

    # ca.general._GeneralSettings__apollo_capture_in_xml = True
    # ca.general._option_apollo_capture = True

    print_capture_template(ca)

    capt = engine.create_capture(ca)
    if capt is None:
        print('*** Failed to create capture.')
        failures += 1
        return failures
    print_capture(capt)

    gca = capt.get_capture_template()
    gca.analysis.set_all(False)
    gca.plugins.set_all(False)
    gca.indexing.set_all(False)
    # capt.modify(gca)
    # capt.refresh()
    # print_capture(capt)

    # gca = capt.get_capture_template()
    # gca.indexing.option_ipv4 = True
    # capt.modify(gca)
    # capt.refresh()
#     tca = capt.get_capture_template()
#     if not tca.indexing.option_ipv4:
#         failures += 1
#     if (tca.indexing.option_application or tca.indexing.option_country
#             or tca.indexing.option_ethernet or tca.indexing.option_ipv6
#             or tca.indexing.option_mpls or tca.indexing.option_port
#             or tca.indexing.option_protospec or tca.indexing.option_vlan):
#         failures += 1
#     print_capture(capt)

    engine.delete_capture(capt)
    capt = None

    capts = []
    for c in range(17):
        cx = omniscript.CaptureTemplate()
        if adpt:
            cx.set_adapter(adpt)
        cx.general.name = f'{capture_name} - {c}'
        cx.general.buffer_size = 10 * BYTES_PER_MEGABYTE
        cx.general.comment = 'Python generated capture.'
        cx.general.directory = os.path.join(temp_path, 'Capture Files')
        cx.general.file_pattern = capture_name + '-'
        cx.general.file_size = 128 * BYTES_PER_MEGABYTE
        cx.general.keep_last_files_count = 5
        cx.general.max_file_age = SECONDS_PER_HOUR
        cx.general.max_total_file_size = BYTES_PER_GIGABYTE
        cx.general.slice_length = 256
        cx.general.tap_timestamps = omniscript.TAP_TIMESTAMPS_DEFAULT
        cx.general.option_capture_to_disk = True
        cx.general.option_continuous_capture = True
        cx.general.option_deduplicate = True
        cx.general.option_file_age = True
        cx.general.option_keep_last_files = True
        cx.general.option_priority_ctd = True
        cx.general.option_save_as_template = True
        cx.general.option_slicing = True
        cx.general.option_start_capture = False
        cx.general.option_timeline_app_stats = True
        cx.general.option_timeline_stats = True
        cx.general.option_timeline_top_stats = True
        cx.general.option_timeline_voip_stats = True
        cx.general.option_total_file_size = True

        cx.analysis.option_alarms = (c < 1)
        cx.analysis.option_analysis_modules = (c < 2)
        cx.analysis.option_application = (c < 3)
        cx.analysis.option_compass = (c < 4)
        cx.analysis.option_country = (c < 5)
        cx.analysis.option_error = (c < 6)
        cx.analysis.option_expert = (c < 7)
        cx.analysis.option_network = (c < 8)
        cx.analysis.node_protocol_detail_limit.enabled = (c < 9)
        cx.analysis.node_limit.enabled = (c < 10)
        cx.analysis.protocol_limit.enabled = (c < 11)
        cx.analysis.option_size = (c < 12)
        cx.analysis.option_summary = (c < 13)
        cx.analysis.option_traffic = (c < 14)
        cx.analysis.option_voice_video = (c < 15)

#         obj = cx.analysis.node_protocol_detail_limit.to_xml()
#         t = ET.tostring(obj)
#         print(t)

        # cx.graphs.enabled = True
        # cx.graphs.interval = 10
        # cx.graphs.file_count = 5
        # cx.graphs.file_buffer_size = 20
        # cx.graphs.hours_to_keep = 4
        # cx.graphs.option_preserve_files = True
        # cx.graphs.graphs = gtl_sublist

        cx.filter.mode = omniscript.FILTER_MODE_ACCEPT_MATCHING_ANY
        cx.add_filter(filter_name)

        # cx.start_trigger.enabled = True
        # cx.start_trigger.option_notify = True
        # cx.start_trigger.severity = omniscript.SEVERE
        # cx.start_trigger.option_toggle_capture = True
        # cx.start_trigger.captured.enabled = True
        # cx.start_trigger.captured.bytes = 10 * 1024 * 1024
        # cx.start_trigger.filter.enabled = True
        # cx.start_trigger.filter.mode = omniscript.FILTER_MODE_ACCEPT_MATCHING_ALL
        # cx.start_trigger.filter.filters = ['FTP']
        # cx.start_trigger.time.enabled = True
        # cx.start_trigger.time.option_use_elapsed = False
        # cx.start_trigger.time.option_use_date = True
        # cx.start_trigger.time.time = omniscript.PeekTime().value   # Now

        # cx.stop_trigger.enabled = True
        # cx.stop_trigger.option_notify = True
        # cx.stop_trigger.severity = omniscript.MAJOR
        # cx.stop_trigger.option_toggle_capture = True
        # cx.stop_trigger.captured.enabled = True
        # cx.stop_trigger.captured.bytes = 1024 * 1024
        # cx.stop_trigger.filter.enabled = True
        # cx.stop_trigger.filter.mode = omniscript.FILTER_MODE_ACCEPT_MATCHING_ALL
        # cx.stop_trigger.filter.filters = ['HTTP']
        # cx.stop_trigger.time.enabled = True
        # cx.stop_trigger.time.option_use_elapsed = True
        # cx.stop_trigger.time.time = omniscript.PeekTime(120 * 1000000000) # 120 seconds.

        try:
            capt = engine.create_capture(cx)
        except Exception:
            pass

        if capt is None:
            print('*** Failed to create capture %d.' % (c))
            failures += 1
            continue
        print_capture(capt)
        cx_t = capt.get_capture_template()
        print_capture_template(cx_t)
        capts.append(capt)

    engine.delete_capture(capts)

    template_list = engine.get_capture_template_list()
    for ct in template_list:
        s_ct = engine.get_capture_template(ct.id)
        print_capture_template(s_ct)
    cl = engine.get_capture_list()
    for c in cl:
        ct = c.get_capture_template()
        print_capture_template(ct)

    template_name = 'Python Script Capture'
    ctl = engine.get_capture_template_list()
    d_ct = omniscript.find_capture_template(ctl, template_name)
    if d_ct:
        engine.delete_capture_template(d_ct)

    ct = ctl[0]
    ct.general.id = omniscript.OmniId(True)
    ct.general.name = template_name
    engine.add_capture_template(ct)

    ctl = engine.get_capture_template_list()
    m_ct = omniscript.find_capture_template(ctl, template_name)
    if m_ct:
        m_ct.general.option_capture_to_disk = False
        engine.update_capture_template(m_ct)

    d_ct = omniscript.find_capture_template(ctl, template_name)
    if d_ct:
        engine.delete_capture_template(d_ct)

    removal_list = []
    for t in template_list:
        if t.name[:len(capture_name)] == capture_name:
            removal_list.append(t)
    engine.delete_capture_template(removal_list)

    ct = omniscript.CaptureTemplate()
    if adpt:
        ct.set_adapter(adpt)
    ct.general.name = capture_name
    ct.general.buffer_size = 10 * BYTES_PER_MEGABYTE
    ct.general.comment = 'Python generated capture.'
    ct.general.directory = os.path.join(temp_path, 'Capture Files')
    ct.general.file_pattern = capture_name + '-'
    ct.general.file_size = 128 * BYTES_PER_MEGABYTE
    ct.general.keep_last_files_count = 5
    ct.general.max_file_age = SECONDS_PER_HOUR
    ct.general.max_total_file_size = BYTES_PER_GIGABYTE
    ct.general.slice_length = 256
    ct.general.tap_timestamps = TAP_TIMESTAMPS_DEFAULT
    ct.general.option_capture_to_disk = True
    ct.general.option_continuous_capture = True
    ct.general.option_deduplicate = True
    ct.general.option_file_age = True
    ct.general.option_keep_last_files = True
    ct.general.option_priority_ctd = True
    ct.general.option_save_as_template = True
    ct.general.option_slicing = True
    ct.general.option_start_capture = False
    ct.general.option_timeline_app_stats = True
    ct.general.option_timeline_stats = True
    ct.general.option_timeline_top_stats = True
    ct.general.option_timeline_voip_stats = True
    ct.general.option_total_file_size = True

    ct.analysis.option_alarms = True
    ct.analysis.option_analysis_modules = True
    ct.analysis.option_application = True
    ct.analysis.option_compass = True
    ct.analysis.option_country = True
    ct.analysis.option_error = True
    ct.analysis.option_expert = True
    ct.analysis.option_network = True
    ct.analysis.option_size = True
    ct.analysis.option_summary = True
    ct.analysis.option_traffic_history = True
    ct.analysis.option_voice_video = True
    ct.analysis.node_limit.enabled = True
    ct.analysis.protocol_limit.enabled = True
    ct.analysis.node_protocol_detail_limit.enabled = True

    # ct.graphs.enabled = True
    # ct.graphs.interval = 10
    # ct.graphs.file_count = 5
    # ct.graphs.file_buffer_size = 20
    # ct.graphs.hours_to_keep = 4
    # ct.graphs.option_preserve_files = True
    # ct.graphs.graphs = gtl_sublist

    ct.filter.mode = omniscript.FILTER_MODE_ACCEPT_MATCHING_ANY
    ct.add_filter(filter_name)

    capt = engine.create_capture(ct)
    if capt is None:
        print('*** Failed to create capture.')
        failures += 1
        return failures
    print_capture(capt)
#     gct = capt.get_capture_template()
#     print_capture_template(gct)

#     print('Start capturing')
#     engine.start_capture(capt)
#     if not capt.is_capturing():
#         print('*** Failed to start the capture.')
#         failures += 1

#     sites = ['yahoo', 'liveaction', 'apple', 'digg']
#     for site in sites:
#         try:
#             url = r'http://%s.com' % site
#             site_text = urllib2.urlopen(url).read()
#             print(site_text)
#         except Exception:
#             pass
#     print('Stop capturing')
#     engine.stop_capture(capt)
#     if capt.is_capturing():
#         print('*** Failed to stop the capture.')
#         failures += 1

#     print('Start capturing')
#     capt.start()
#     if not capt.is_capturing():
#         print('*** Failed to re-start the capture.')
#         failures += 1
#     print(capt.format_status())
#     for site in sites:
#         if not capt.is_capturing():
#             break
#         print('Captured %d packets' % capt.packets_filtered)
#         try:
#             url = urllib2.urlopen('http://www.%s.com' % site)
#         except urllib2.HTTPError:
#             pass
#     print('Stop capturing')
#     capt.stop()
#     if capt.is_capturing():
#         print('*** Failed to re-stop the capture.')
#         failures += 1
#     print(capt.format_status())
#     print('Capture has %d packets' % capt.packets_filtered)
#     print('Delete the capture: %s' % capture_name)
#     engine.delete_capture(capt)

    # Clean up.
    capt = engine.find_capture(capture_name)
    while capt:
        ctt = capt.get_capture_template()
        print(ctt)
        engine.delete_capture(capt)
        capt = engine.find_capture(capture_name)

    return failures


def test_capture_all(engine):
    print('Capture All Test')
    failures = 0

    gtl = engine.get_graph_template_list()
    print_graph_template_list(gtl)

    full_capture_props = full_props.get('full_capture_props')
    if isinstance(full_capture_props, dict):
        ct = omniscript.CaptureTemplate(props=full_capture_props, engine=engine)
        print_capture_template(ct)
    else:
        print('*** Test Capture All failure.')
        failures += 1

    return failures


def test_capture_stats(engine, capture_name, packets_needed):
    print('Capture Statistics Test')
    failures = 0
    remote_source = PurePath(f'/home/{options.user}/pcap/')
    remote_destination = PurePath('/input/monitor')

    ca = None
    capt = engine.find_capture(capture_name)
    if not capt:
        ca = omniscript.CaptureTemplate()
        adpt = get_folder_adapter(engine, str(remote_destination))
        if adpt is None:
            print(f'*** Did not find Folder Adapter: {remote_destination}')
            failures += 1
            return failures
        ca.set_adapter(adpt)
        ca.general.name = capture_name
        ca.general.buffer_size = 10 * BYTES_PER_MEGABYTE
        ca.general.comment = 'Python generated capture.'
        ca.general.directory = os.path.join(temp_path, 'Capture Files')
        ca.general.file_pattern = capture_name + '-'
        ca.general.file_size = 128 * BYTES_PER_MEGABYTE
        ca.general.keep_last_files_count = 5
        ca.general.max_file_age = SECONDS_PER_HOUR
        ca.general.max_total_file_size = BYTES_PER_GIGABYTE
        ca.general.slice_length = 256
        ca.general.tap_timestamps = omniscript.TAP_TIMESTAMPS_DEFAULT
        ca.general.option_capture_to_disk = True
        ca.set_all(True)
        ca.indexing.set_all(True)
        ca.plugins.set_all(True)

        capt = engine.create_capture(ca)
        if capt is None:
            print('*** Did not create the capture: %s' % capture_name)
            failures += 1
            return failures
    else:
        ca = capt.get_capture_template()
        print_capture_template(ca)

    for file_name in stats_file_names:
        source = remote_source.joinpath(file_name)
        remote_copy_file(options.host, options.user, source, remote_destination)

    capt.start()
    while capt.packets_filtered < packets_needed:
        time.sleep(5)
        capt.refresh()
    capt.stop()

    if capt.packets_filtered < packets_needed:
        print('*** Not enough packets.')
        failures += 1
        return failures

    app_stats = capt.get_application_stats()
    if app_stats:
        print_application_stats(app_stats)
    else:
        print('*** Did not get Application Statistics.')
        print()
        failures += 1

    app_flow_stats = capt.get_application_flow_stats()
    if app_flow_stats:
        print_application_flow_stats(app_flow_stats)
    else:
        print('*** Did not get Application Flow Statistics.')
        print()
        failures += 1

    if ca.analysis.option_voice_video:
        call_stats = capt.get_call_stats()
        if call_stats:
            print_call_stats(call_stats)
        else:
            print('*** Did not get Call Statistics.')
            print()
            failures += 1

    conversation_stats = capt.get_conversation_stats()
    if conversation_stats:
        print_conversation_stats(conversation_stats)
    else:
        print('*** Did not get Conversation Statistics.')
        print()
        failures += 1

    country_stats = capt.get_country_stats()
    if country_stats:
        print_country_stats(country_stats)
    else:
        print('*** Did not get Country Statistics.')
        print()
        failures += 1

    network_stats = capt.get_network_stats()
    if network_stats:
        print_network_stats(network_stats)
    else:
        print('*** Did not get Network Statistics.')
        print()
        failures += 1

    node_stats = capt.get_node_stats()
    if node_stats:
        print_node_stats(node_stats)
    else:
        print('*** Did not get Node Statistics.')
        print()
        failures += 1

    protocol_stats = capt.get_protocol_stats()
    if protocol_stats:
        print_protocol_stats(protocol_stats)
    else:
        print('*** Did not get Protocol Statistics.')
        print()
        failures += 1

    protocol_by_id_stats = capt.get_protocol_by_id_stats()
    if protocol_by_id_stats:
        print_protocol_by_id_stats(protocol_by_id_stats)
    else:
        print('*** Did not get Protocol By Id Statistics.')
        print()
        failures += 1

    size_stats = capt.get_size_stats()
    if size_stats:
        print_size_stats(size_stats)
    else:
        print('*** Did not get Size Statistics.')
        print()
        failures += 1

    summary_stats = capt.get_summary_stats()
    current_summary_snapshot = summary_stats.get_current_snapshot()
    if current_summary_snapshot is not None:
        print_summary_snapshot(current_summary_snapshot, True)
    if summary_stats:
        print_summary_stats(summary_stats)
    else:
        print('*** Did not get Summary Statistics.')
        print()
        failures += 1

    # Todo: Add Stat Printers.

    return failures


def test_delete_all(engine):
    print('Delete All Test')
    failures = 0

    csl = engine.get_capture_session_list()
    print(csl)
    engine.delete_all_capture_sessions()
    cl = engine.get_capture_list()
    engine.delete_capture(cl)
    fsl = engine.get_forensic_search_list()
    engine.delete_all_forensic_searches()

    # Not in REST API
    # ffl = engine.get_forensic_file_list()
    # engine.delete_file(ffl)

    tcl = engine.get_capture_list()
    if len(tcl) > 0:
        print('*** Failed to delete all captures.')
        failures += 1
    fsl = engine.get_forensic_search_list()
    if len(fsl) > 0:
        print('*** Failed to delete all Forensic Searches.')
        failures += 1

    # Not in REST API
    # tffl = engine.get_forensic_file_list()
    # if len(tffl) > 0:
    #     print('*** Failed to delete all Forensic Files.')
    #     failures += 1
    return failures


def test_event_log(engine):
    print('Event Log Test')
    failures = 0
    messages = []

    query_word = 'Ziggy Stardust'

    e = omniscript.EventLogEntry()
    e.message = 'A message from PyTest.py: This is severe.'
    e.severity = omniscript.Severity.SEVERE
    engine.add_events(e)

    cl = engine.get_capture_list()
    if len(cl) == 0:
        print('*** No captures for Event Log testing.')
        messages.append('Test Event Log: 1')
        failures += 1
        return failures, messages
    cap = cl[0]

    evts = []
    r = int(random() * 10000)
    for i in range(3):
        evt = omniscript.EventLogEntry()
        evt.capture_id = cap.id
        evt.message = f'PyTest.py {query_word}: {r}.'
        evt.severity = omniscript.Severity.INFORMATIONAL
        evt.timestamp = omniscript.PeekTime()
        evts.append(evt)
        r += 1

    engine.add_events(evts)

    es = engine.get_status()
    start_time = omniscript.PeekTime(es.time.value - es.uptime)
    end_time = es.time

    loop_max = 100
    primer_el = engine.get_event_log(time_span=(start_time, end_time))
    while primer_el.count < 50 and loop_max > 0:
        time.sleep(1)
        cap.start()
        cap.stop()
        es = engine.get_status()
        start_time = omniscript.PeekTime(es.time.value - es.uptime)
        end_time = es.time
        primer_el = engine.get_event_log(time_span=(start_time, end_time))
        loop_max -= 1
    cap.start()

    el = engine.get_event_log(count=20)
    print_event_log(el)
    el.get_next(10)
    print_event_log(el)
    el.get(30, 5)
    print_event_log_indexes(el)
    el.get_next(-10)
    print_event_log_indexes(el)

    print(f'Capture: {cap.name}')
    # log_id = engine.get_event_log(count=10, capture=cap.id,
    #                               time_span=(cap.creation_time, cap.stop_time))
    log_id = engine.get_event_log(count=10, capture=cap.id)
    print_event_log(log_id)

    el_backup = engine.get_event_log(0, log_id.count, cap.id)

    log_str = engine.get_event_log(0, 5, cap.id.format())
    print_event_log(log_str)

    log_cap = engine.get_event_log(0, 5, cap)
    print_event_log(log_cap)

    if log_id.count > 0:
        engine.delete_event_log(cap.id)
        log_check = engine.get_event_log(0, log_id.count, cap.id)
        if log_check.count > 0:
            print(f'*** Failed to delete Event Log for {cap.name}')
            messages.append(f'Test Event Log: 2 Capture: {cap.name}')
            failures += 1

    el_engine = engine.get_event_log()
    engine.delete_event_log()

    engine.add_events(el_engine.entries)
    engine.add_events(el_backup.entries)

    el_cap = engine.get_event_log(capture=cap, query=query_word)
    print_event_log(el_cap)
    el_cap.get_next(-1)
    print_event_log(el_cap)

    try:
        el_cap = engine.get_event_log(1, 10, capture=cap, query=query_word)
        print_event_log(el_cap)
    except Exception:
        print('*** Failed to get Event Log - 1')
        messages.append('Test Event Log: 3')
        failures += 1

    return failures, messages


def test_file_ops(engine, file_name, result_file):
    print('File Operations Test')
    failures = 0

    pf = None
    pfl = engine.get_packet_file_list()
    for _pf in pfl:
        print(f'Packet File: {_pf.name}')
        if not pf or (_pf.packet_count > pf.packet_count):
            pf = _pf

    if pf:
        contents = engine.get_file(pf)
        print(f'File: {pf.path},  {len(contents)} bytes.')

    file_names = [
        'Napatech-2022-02-18T18.32.53.986.pkt',
        'smtp_64-byte.pcap',
        'list-pcap.txt',
        'back_ground.png'
    ]
    for f in file_names:
        sf = os.path.join(shared_files, f)
        count = engine.send_file(sf)
        print(f'File: {sf},  {count} bytes.')

    es = engine.get_status()
    data_dir = engine.get_directory(es.data_directory)
    print(data_dir)
    try:
        file_names.append('bogus_file')  # Deleting bogus_file does not generate an error.
        res = engine.delete_file(file_names)
        print(res)
    except omniscript.OmniError as e:
        if isinstance(e.result, list):
            failures += len(e.result)

    dir = engine.get_directory()
    print(dir)
    return failures


# def test_file_adapter(engine, file_name, capture_name, needed_packets, save_all_names):
#     print('File Adapters Test')
#     failures = 0

#     fl = engine.get_file_list()
#     ffi = list(i for i in fl if i.name == file_name)
#     wd = os.getcwd()
#     print(wd)
#     if len(ffi) == 0:
#         sf_filename = os.path.normpath(os.path.join(shared_files, file_name))
#         engine.send_file(sf_filename)
#         fl = engine.get_file_list()
#         ffi = list(i for i in fl if i.name == file_name)
#         if len(ffi) == 0:
#             print('*** Failed to send file to engine: %s' % file_name)
#             failures += 1
#             return failures

#     cl = engine.get_capture_list()
#     cli = list(i for i in cl if i.name == capture_name)
#     engine.delete_capture(cli)

#     cf_path = fl[0].name + file_name    # do not use os.path.join!
#     fa = omniscript.FileAdapter(cf_path)
#     fa.limit = 1
#     fa.speed = 0.0

#     ct = omniscript.CaptureTemplate()
#     ct.general.buffer_size = 10 * BYTES_PER_MEGABYTE
#     ct.general.name = capture_name
#     ct.general.option_continuous_capture = True
#     ct.general.option_capture_to_disk = True
#     ct.general.option_start_capture = False
#     ct.general.option_timeline_app_stats = True
#     ct.general.option_timeline_stats = True
#     ct.general.option_timeline_top_stats = True
#     ct.general.option_timeline_voip_stats = True
#     ct.analysis.option_alarms = True
#     ct.analysis.option_analysis_modules = True
#     ct.analysis.option_application = True
#     ct.analysis.option_compass = True
#     ct.analysis.option_country = True
#     ct.analysis.option_error = True
#     ct.analysis.option_expert = True
#     ct.analysis.option_network = True
#     ct.analysis.node_protocol_detail_limit.enabled = True
#     ct.analysis.node_limit.enabled = True
#     ct.analysis.protocol_limit.enabled = True
#     ct.analysis.option_size = True
#     ct.analysis.option_summary = True
#     ct.analysis.option_traffic = True
#     ct.analysis.option_voice_video = True
#     ct.stop_trigger.enabled = True
#     ct.stop_trigger.time.enabled = True
#     ct.stop_trigger.time.option_use_elapsed = True
#     ct.stop_trigger.time.time = (54+5) * 1000000000L # 60 seconds.
#     ct.stop_trigger.captured.enabled = True
#     ct.stop_trigger.captured.bytes = (970043 + 64)
#     ct.set_adapter(fa)
#     capt = engine.create_capture(ct)
#     if capt is None:
#         print('*** Failed to create capture.')
#         failures += 1
#         return failures
#     print_capture(capt)
#     capt.start()
#     capt = engine.find_capture(capt)
#     print(capt.format_status())
#     while (capt.status & 0x0001) and (capt.packets_filtered < needed_packets):
#         get_traffic()
#         capt.refresh()
#     capt.stop()
#     capt.refresh()
#     print(capt.format_status())
#     print(capt.packets_filtered)

#     ffl = engine.get_forensic_file_list()
#     for ff in ffl:
#         if ff.name == save_all_name_engine:
#             engine.delete_file(save_all_name_engine)
#         elif ff.name == save_all_name_capture:
#             engine.delete_file(save_all_name_capture)

#     ffl = engine.get_forensic_file_list()
#     engine.sync_forensic_database()
#     ffl = engine.get_forensic_file_list()

#     engine.save_all_packets(capt, save_all_name_engine)
#     capt.save_all_packets(save_all_name_capture)

#     found_engine = False
#     found_capture = False
#     ffl = engine.get_forensic_file_list()
#     for ff in ffl:
#         if ff.name == save_all_names[0]:
#             found_engine = True
#         elif ff.name == save_all_names[1]:
#             found_capture = True
#     if found_engine or found_capture:
#         print('*** Failure: file added to Forensic File List before sync.')
#         failures += 1

#     engine.sync_forensic_database()

#     found_engine = False
#     found_capture = False
#     ffl = engine.get_forensic_file_list()
#     for ff in ffl:
#         if ff.name == save_all_names[0]:
#             found_engine = True
#         elif ff.name == save_all_names[1]:
#             found_capture = True
#     if not use_file_db:
#         print('File Database disabled')
#         if found_engine or found_capture:
#             print('*** Failure: files incorrectly added to Forensic File List.')
#             failures += 1
#     else:
#         if not found_engine or not found_capture:
#             print('*** Failure: files not added to Forensic File List.')
#             failures += 1

#     ffl = engine.get_forensic_file_list()
#     for ff in ffl:
#         if ff.name == save_all_name_engine:
#             engine.delete_file(save_all_names[0])
#         elif ff.name == save_all_name_capture:
#             engine.delete_file(save_all_names[1])
#     engine.sync_forensic_database()
#     return failures


def test_file_database_operations(engine):
    print('Database Operations Test')
    failures = 0

    try:
        engine.file_database_operation(omniscript.DatabaseOperation.SYNC)
    except Exception:
        print('Engine does not have Database enabled.')

    try:
        engine.file_database_operation(omniscript.DatabaseOperation.INDEX)
    except Exception:
        print('Engine does not have Database enabled.')

    try:
        resp = engine.file_database_operation(omniscript.DatabaseOperation.MAINTENANCE)
        print(f'Database Maintenance: {resp}')
    except Exception:
        print('Engine does not have Database enabled.')

    return failures


def test_filters(engine, filter_name):
    print('Filters Test')
    failures = 0

    filters_xml = os.path.normpath(os.path.join(shared_files, 'filters.xml'))
    filters_flt = os.path.normpath(os.path.join(shared_files, 'filters.flt'))
    print(filters_flt)

    bin_filters = omniscript.read_filter_file(filters_xml)
    print_filter_list(bin_filters)

    fl = engine.get_filter_list()
    print_filter_list(fl)
    fli = list(i for i in fl if i.name == filter_name)
    engine.delete_filter(fli)

    simple_name = 'Python-Simple'
    address_name = 'Python-Address'
    wildcard_name = 'Python-Wildcard'
    vlan_mpls_name = 'Python-VLAN-MPLS'
    vlan_mpls_vlan_name = 'Python-VLAN-MPLS - vlan'
    vlan_mpls_mpls_name = 'Python-VLAN-MPLS - mpls'
    complex_name = 'Python-Complex'
    filter_names = [simple_name, address_name,
                    wildcard_name, vlan_mpls_name, complex_name]

    aml = engine.get_analysis_module_list()
    email_analysis = omniscript.find_analysis_module(aml, 'Email Analysis')
    tcp_dump = omniscript.find_analysis_module(aml, 'tcpdump')

    # Delete Python Filters
    for name in filter_names:
        fli = list(i for i in fl if i.name == name)
        for f in fli:
            engine.delete_filter(f)

    # Simple Filter
    simple = omniscript.Filter(simple_name)
    simple.comment = 'Python created filter.'
    addr_node = omniscript.AddressNode()
    addr_node.address_1 = omniscript.IPv4Address('1.2.3.4')
    # addr_node.address_2 = omniscript.IPv4Address()
    addr_node.accept_1_to_2 = True
    addr_node.accept_2_to_1 = True
    simple.criteria = addr_node
    engine.add_filter(simple)
    print_filter(simple)
    print(simple.to_string(0))

    # Address Filter
    address = omniscript.Filter(address_name)
    address.comment = 'Python created filter.'
    addr_node = omniscript.AddressNode()
    addr_node.accept_1_to_2 = True
    addr_node.accept_2_to_1 = True
    address.criteria = addr_node
    engine.add_filter(address)
    print_filter(address)
    print(address.to_string(0))

    # Wildcard Filter
    wildcard = omniscript.Filter(wildcard_name)
    wildcard.comment = 'Python created filter.'
    addr_node = omniscript.AddressNode()
    addr_node.address_1 = omniscript.EthernetAddress('00:14:2F:*:*:*')
    addr_node.accept_1_to_2 = True
    addr_node.accept_2_to_1 = True
    wildcard.criteria = addr_node
    engine.add_filter(wildcard)
    print_filter(wildcard)
    print(wildcard.to_string(0))

    # VLAN MPLS Filter
    vlan_mpls = omniscript.Filter(vlan_mpls_name)
    vlan_mpls.comment = 'Python created filter.'
    vlan_mpls_node = omniscript.VlanMplsNode()
    # vlan_mpls_node.add_id('80')
    # vlan_mpls_node.add_id('100-110')
    vlan_mpls_node.add_ids(80, '100-110')
    # vlan_mpls_node.add_label('200-220')
    # vlan_mpls_node.add_label('1024')
    vlan_mpls_node.add_labels('200-220', 1024)
    vlan_mpls.criteria = vlan_mpls_node
    engine.add_filter(vlan_mpls)
    print_filter(vlan_mpls)
    print(vlan_mpls.to_string(0))

    # VLAN MPLS Filter VLAN only
    vlan_mpls = omniscript.Filter(vlan_mpls_vlan_name)
    vlan_mpls.comment = 'Python created filter.'
    vlan_mpls_node = omniscript.VlanMplsNode()
    # vlan_mpls_node.add_id('80')
    # vlan_mpls_node.add_id('100-110')
    vlan_mpls_node.add_ids(80, '100-110')
    vlan_mpls.criteria = vlan_mpls_node
    engine.add_filter(vlan_mpls)
    print_filter(vlan_mpls)
    print(vlan_mpls.to_string(0))

    # VLAN MPLS Filter MPLS only
    vlan_mpls = omniscript.Filter(vlan_mpls_mpls_name)
    vlan_mpls.comment = 'Python created filter.'
    vlan_mpls_node = omniscript.VlanMplsNode()
    # vlan_mpls_node.add_label('200-220')
    # vlan_mpls_node.add_label('1024')
    vlan_mpls_node.add_labels('200-220', 1024)
    vlan_mpls.criteria = vlan_mpls_node
    engine.add_filter(vlan_mpls)
    print_filter(vlan_mpls)
    print(vlan_mpls.to_string(0))

    # Complex Filter
    cx = omniscript.find_filter(fl, ' Complex-1')
    if cx:
        cx_props = cx._store()
        print(cx_props)

    complex = omniscript.Filter(complex_name)
    complex.comment = 'Python created filter.'

    addr_node = omniscript.AddressNode()
    addr_node.address_1 = omniscript.IPv4Address('1.2.3.4')
    addr_node.address_2 = omniscript.IPv4Address('0.0.0.0')
    addr_node.accept_1_to_2 = True
    addr_node.accept_2_to_1 = True

    protocol_node = omniscript.ProtocolNode()
    protocol_node.set_protocol('HTTP')

    port_node = omniscript.PortNode()
    port_node.port_1 = 80
    port_node.accept_1_to_2 = True
    port_node.accept_2_to_1 = True

    pattern_node = omniscript.PatternNode()
    pattern_node.set_pattern('12345678')
    pattern_node.start_offset = 64
    pattern_node.end_offset = 1024

    value_node = omniscript.ValueNode()
    value_node.value = 8675309

    length_node = omniscript.LengthNode()
    length_node.minimum = 64
    length_node.maximum = 1024

    wireless_node = omniscript.WirelessNode()
    wireless_node.channel_band = omniscript.WIRELESS_BAND_ALL
    wireless_node.channel_number = 1
    wireless_node.channel_frequency = 2412
    wireless_node.data_rate = 11.0
    wireless_node.flags = (
        omniscript.WIRELESS_FLAG_20MHZ_LOWER |
        omniscript.WIRELESS_FLAG_20MHZ_UPPER |
        omniscript.WIRELESS_FLAG_40MHZ)
    wireless_node.signal_minimum = 20
    wireless_node.signal_maximum = 80
    wireless_node.noise_minimum = 0
    wireless_node.noise_maximum = 10

    channel_node = omniscript.ChannelNode()
    channel_node.channel = 3

    error_node = omniscript.ErrorNode()
    error_node.crc_errors = True
    error_node.frame_errors = True
    error_node.oversize_errors = True
    error_node.runt_errors = True

    plugin_node = omniscript.PluginNode()
    if email_analysis:
        plugin_node.add_analysis_module(email_analysis)
    elif tcp_dump:
        plugin_node.add_analysis_module(tcp_dump)

    wan_node = omniscript.WANDirectionNode()
    wan_node.direction = omniscript.WAN_DIRECTION_TO_DTE

    vlan_mpls_node = omniscript.VlanMplsNode()
    vlan_mpls_node.add_id(1024)
    vlan_mpls_node.add_label(8888)

    tcpdump_node = omniscript.BpfNode()
    tcpdump_node.filter = 'port(8080)'

    nodes = [addr_node, protocol_node, pattern_node, value_node, length_node, wireless_node,
             channel_node, error_node, plugin_node, wan_node, vlan_mpls_node, tcpdump_node]

    for n in nodes:
        complex.name = f'{complex_name} - {n._display_name}'
        old = omniscript.find_filter(fl, complex_name)
        if old:
            engine.delete_filter(old)
        time.sleep(1)
        complex.criteria = n
        print(f'Adding Filter: {complex.name}')
        engine.add_filter(complex)

    complex.criteria = addr_node
    addr_node.and_node = protocol_node
    addr_node.or_node = pattern_node
    pattern_node.or_node = value_node
    value_node.and_node = length_node
    length_node.and_node = wireless_node
    length_node.or_node = channel_node
    channel_node.and_node = error_node
    error_node.and_node = plugin_node
    error_node.or_node = wan_node
    plugin_node.and_node = vlan_mpls_node
    plugin_node.or_node = tcpdump_node

    cf = complex._store()
    print(cf)

    engine.add_filter(complex)
    print_filter(complex)
    print(complex.to_string(0))

#     try:
#         fl = engine.get_filter_list()
#         engine.delete_filter(fl)
#         if len(fl) > 0:
#             engine.add_filter(fl[0])
#             engine.delete_filter(engine.get_filter_list())

#         console_filters = omniscript.read_filter_file(filters_flt)
#         print_filter_list(console_filters)
#         for flt in console_filters:
#             try:
#                 engine.add_filter(flt)
#             except Exception:
#                 print('Failed to add filter: %s' % flt.name)
#         engine.delete_filter(engine.get_filter_list())
#         engine.add_filter(console_filters)

#         engine_filters = omniscript.read_filter_file(filters_xml)
#         print_filter_list(engine_filters)
#         for flt in engine_filters:
#             try:
#                 engine.add_filter(flt)
#             except Exception:
#                 print('Failed to add filter: %s' % flt.name)
#         engine.delete_filter(engine.get_filter_list())
#         engine.add_filter(engine_filters)

#     finally:
#         engine.delete_filter(engine.get_filter_list())
#         engine.add_filter(bin_filters)

    return failures


def test_filter_all_test(engine):
    print('Filter All Test')
    failures = 0

    filter_name = ' PyTest Filter'
    old_filter = engine.find_filter(filter_name)
    # old = engine.get_filter(old_filter)
    # print(old)
    engine.delete_filter(old_filter)

    ip_filter = create_ip_filter(filter_name, '192.0.0.1')
    flt = ip_filter._store()
    print(flt)
    engine.add_filter(ip_filter)

    complex_filter_criteria = full_props.get('complex_filter_criteria')
    if isinstance(complex_filter_criteria, dict):
        f = omniscript.Filter(criteria=complex_filter_criteria)
        print_filter(f)
        f._store()
        print(f'\n{f}\n')
    else:
        print('*** Failed Filter All Test.')
        failures += 1

    return failures


# def test_flows_test(engine, capt_args, ipv6_args):
#     print('Flows Test')
#     failures = 0

#     if False:
#         try:
#             filename = 'Expert-Query-Flows-Response.xml'
#             if os.path.exists(filename):
#                 root = ET.parse(filename)
#                 msg = root.getroot()
#                 eqs = [ExpertQuery(i) for i in msg.findall('query')]
#                 rss = [ExpertResult(i) for i in msg.findall('result-set')]
#                 print('%d %d' %(len(eqs), len(rss)))
#                 for e in eqs:
#                     print('Query: %s\n  Columns: %d' % (e.name, len(e.columns)))
#                 print
#                 for r in rss:
#                     print('Result: %s\n  Columns: %d\n  Rows: %d'
#                           % (r.name, len(r.columns), len(r.rows)))
#             print
#             return failures
#         except Exception:
#             print
#             return 1

#     cap = create_capture(engine, *capt_args)
#     if cap is None:
#         failures += 1
#         return failures
#     failures += query_expert_short(engine, cap)

#     cap = create_capture(engine, *capt_args)
#     if cap is None:
#         failures += 1
#         return failures
#     failures += query_expert_long(engine, cap)

#     return failures


# def test_forensic_stats(engine, forensic_name, packets_needed):
#     print('Forensic Statistics Test')
#     failures = 0

#     fs = engine.find_forensic_search(forensic_name)
#     if not fs:
#         print('Did not find forensic search: %s' % forensic_name)
#         failures += 1
#         return failures
#     if fs.packet_count < packets_needed:
#         print('Not enough packets.')
#         failures += 1
#         return failures

#     context = fs.get_stats_context()
#     if not context:
#         print('Did not get Statistics Context.')
#         failures += 1
#         return failures

#     apps = fs.get_application_stats()
#     calls = fs.get_call_stats()
#     countrys = fs.get_country_stats()
#     nodes = fs.get_node_stats()
#     protocols = fs.get_protocol_stats()
#     summarys = fs.get_summary_stats()

#     total_packets = 0
#     total_bytes = 0
#     if context:
#         total_packets = context.total_packets
#         total_bytes = context.total_bytes

#     if summarys and summarys.has_key('Network'):
#         total_packets = summarys['Network']['Total Packets'].value
#         total_bytes = summarys['Network']['Total Bytes'].value

#     if protocols and len(protocols) > 0:
#         try:
#             udps = next(p for p in protocols if p.name == 'UDP')
#         except Exception:
#             udps = None
#         if udps:
#             print(udps)

#     print_stats_context(context)
#     print_application_stats(apps)
#     print_call_stats(calls)
#     print_country_stats(countrys)
#     print_node_stats(nodes, total_packets, total_bytes)
#     if nodes and len(nodes) > 0:
#         print_node_stat(nodes[0])
#     print_protocol_stats(protocols)
#     if protocols and len(protocols) > 0:
#         print_protocol_stat(protocols[0])
#         flats = omniscript.protocolstatistic.flatten(protocols)
#         print_protocol_stats(flats)
#     print_summary_stats(summarys)
#     if summarys and len(summarys) > 0:
#         if isinstance(summarys, dict):
#             for name, group in summarys.items():
#                 print_summary_group(name, group)
#                 break
#         elif isinstance(summarys, list):
#             for summary in summarys:
#                 print_summary_stat(summary)
#                 break
#     return failures


def test_forensic_template(engine, forensic_name):
    print('Forensic Template Test')
    failures = 0

#     ffl = engine.get_forensic_file_list()
#     print_forensic_file_list(ffl)

#     ff = next((i for i in ffl if ((getattr(i, 'packet_count') > 1000)
#                                   and (getattr(i, 'packet_count') < 10000))), None)
#     if not ff:
#         print('No forensic files or files are too large.')
#         failures += 1
#         return failures

#     fsl = engine.get_forensic_search_list()
#     engine.delete_forensic_search(fsl)

#     fs = engine.find_forensic_search(forensic_name)
#     while fs:
#         fsid = fs.id
#         engine.delete_forensic_search(fs)
#         fs = engine.find_forensic_search(forensic_name)
#         if fs and fs.id == fsid:
#             print('Forensic Search not deleted: %s' % fs.name)
#             failures += 1
#             break

#     fs_filter = omniscript.Filter('Forensic Search - HTTP or X-Windows')
#     fs_filter.comment = 'Python created filter.'
#     http_protocol_node = omniscript.ProtocolNode()
#     http_protocol_node.set_protocol('HTTP')
#     xwin_protocol_node = omniscript.ProtocolNode()
#     xwin_protocol_node.set_protocol('X-Windows')
#     http_protocol_node.or_node = xwin_protocol_node
#     fs_filter.criteria = http_protocol_node

    ft = omniscript.ForensicTemplate()
    ft.name = forensic_name
    # ft.add_file(ff.path)
    # ft.filter = fs_filter
    ft.option_packets = True
    ft.option_indexing = True
    try:
        fs = engine.create_forensic_search(ft)
    except omniscript.OmniError:
        print('*** Failed: Forensic Template Test - 1')
        failures += 1
    timeout = 0
    # or while fs.status == FORENSIC_OPENING
    while fs.status < omniscript.FORENSIC_COMPLETE:
        time.sleep(1)
        fs.refresh()
        timeout += 1
        if timeout > fs_refresh_count:
            break
    if fs.status < omniscript.FORENSIC_COMPLETE:
        print('*** Failed: Forensic Template Test - 2')
        failures += 1

#     failures += query_expert_counts(engine)

#     print_forensic_search(fs)
# #   failures += query_expert_short(engine, fs)

#     ft_all = omniscript.ForensicTemplate()
#     ft_all.name = forensic_name + ' All'
#     ft_all.add_file(ff.path)
#     ft_all.options_packets = True
#     ft_all.options_log = True
#     ft_all.set_all_analysis_options(True)
#     fs_all = engine.create_forensic_search(ft_all)
#     for _ in range(fs_refresh_count):
#         fs.refresh()
#     print_forensic_search(fs_all)

#     failures += query_expert_long(engine, fs_all)
    return failures


def test_forensic_template_all(engine):
    failures = 0

    existing_fsl = engine.get_forensic_search_list()
    print(existing_fsl)
    engine.delete_all_forensic_searches()
    fsl = engine.get_forensic_search_list()
    if len(fsl) > 0:
        print('*** Failed Forensic Template All: 1')
        failures += 1

    # engine.synchronize_file_database()

    pf = None
    pfl = engine.get_packet_file_list()
    if not pfl:
        print('*** Failed Forensic Template All: 2')
        failures += 1
        return failures
    for _pf in pfl:
        print(f'Packet File: {_pf.name}')
        if _pf.packet_count > 1000:
            pf = _pf
    if not pf and pfl:
        pf = pfl[0]

    fs_name = 'Python Forensic Test'

    fst0 = omniscript.ForensicTemplate(fs_name + ' 0')
    fs0 = engine.create_forensic_search(fst0)
    gfs0 = engine.get_forensic_search(fs0)
    engine.delete_forensic_search(gfs0)

    fst1 = omniscript.ForensicTemplate(fs_name + ' 1')
    fst_props = fst1.store()
    print(fst_props)
    fs1 = engine.create_forensic_search(fst1)
    gfs1 = engine.get_forensic_search(fs1)
    print(gfs1)

    fst2 = omniscript.ForensicTemplate(fs_name + ' 2')
    fst2.adapter_name = pf.adapter_name
    fst2.capture_name = pf.capture_name
    # fst2.start_time = pf.session_start_time if pf
    #                   else PeekTime('2022-09-01T00:00:00.000000000').iso_time()
    # fst2.end_time = pf.session_end_time if pf
    #                   else PeekTime('2022-10-01T00:00:00.000000000').iso_time()
    fst2.add_file(pf)
    fst_props_full2 = fst2.store()
    print(fst_props_full2)
    fs2 = engine.create_forensic_search(fst2)
    if not load_forensic_search(fs2):
        print('*** Failed Forensic Template Test All - 3')
        failures += 1
    else:
        count = min(10, fs2.packet_count)
        pk = []
        dec = []
        for i in range(1, (count + 1)):
            pk.append(fs2.get_packet_data(i))
            dec.append(fs2.get_packet_decode(i))

    return failures


def test_gets(engine):
    print('Gets Test')
    failures = 0

    csl = engine.get_capture_session_list()
    print_capture_session_list(csl)

    if csl:
        for i in omniscript.SessionDataType:
            csd = csl[0].get_data(i)
            print_capture_session_data(csd)

        start = omniscript.PeekTime('2022-11-01T00:00:00.000000000Z')
        end = omniscript.PeekTime('2022-11-15T23:59:59.000000000Z')
        for i in omniscript.SessionStatisticsType:
            css = csl[-1].get_statistics(i, start, end)
            print(css)

        engine.delete_capture_session(csl[0])

    es = engine.get_status()
    print_engine_status(es)

    es.refresh()
    print('Refresh Engine Status')
    print_engine_status(es)

    es = engine.get_engine_settings()
    print_engine_settings(es)

    class_names = omniscript.omniscript.get_id_class_names()
    cap_names = omniscript.omniscript.get_id_capability_names()
    with open(os.path.abspath(os.path.join(self_file_path, 'engine-settings.json')), 'rb') as f:
        json_data = json.load(f)
        es_obj = omniscript.EngineSettings(json_data)
        print_engine_settings(es_obj, 20, class_names, cap_names)

    caps = engine.get_capabilities()
    class_names = omniscript.get_id_class_names()
    cap__names = omniscript.get_id_capability_names()
    print_capabilities(caps, class_names, cap__names)

    al = engine.get_adapter_list()
    print_adapter_list(al)
    if len(al) > 0:
        a = engine.find_adapter(al[0].name)
        if not a:
            print('*** Failed to find first adapter by name.')
            failures += 1
        a = engine.find_adapter(al[0].adapter_id, 'id')
        if not a:
            print('*** Failed to find first adapter by id.')
            failures += 1
        if len(al[0].device_name) > 0:
            a = engine.find_adapter(al[0].device_name, 'device_name')
            if not a:
                print('*** Failed to find first adapter by device name.')
                failures += 1

    alarms = engine.get_alarm_list()
    print_alarm_list(alarms)

    aml = engine.get_analysis_module_list()
    print_analysis_module_list(aml)

    nl = engine.get_name_table()
    print_name_table(nl)

    pl = engine.get_protocol_list()
    print_protocol_list(pl)
    sl = omniscript.find_all_protocol(pl, 'Skinny', 'hierarchy')
    print(sl)

    cl = engine.get_capture_list()
    if not cl:
        ct = capture_template(engine)
        for i in range(3):
            ct.general.name = f'Capture {i}'
            engine.create_capture(ct)
        cl = engine.get_capture_list()

    print_capture_list(cl)
    if len(cl) > 0:
        c = engine.find_capture(cl[0].name)
        if not c:
            print('*** Failed to find first capture by name.')
            failures += 1
        c = engine.find_capture(cl[0].id, 'id')
        if not c:
            print('*** Failed to find first capture by id.')
            failures += 1

    for c in cl:
        ct = c.get_capture_template()
        print_capture_template(ct)

    csl = engine.get_capture_session_list()
    print_capture_session_list(csl)

    fl = engine.get_filter_list()
    print_filter_list(fl)
    if len(fl) > 0:
        f = engine.find_filter(fl[0].name)
        if not f:
            print('*** Failed to find first filter by name.')
            failures += 1
        f = engine.find_filter(fl[0].id, 'id')
        if not f:
            print('*** Failed to find first filter by id.')
            failures += 1

    ffl = engine.get_forensic_file_list()
    print_forensic_file_list(ffl)

    fsl = engine.get_forensic_search_list()
    print_forensic_search_list(fsl)
    if len(fsl) > 0:
        fs = omniscript.find_forensic_search(fsl, fsl[0].name)
        if not fs:
            print('*** Failed to find first forensic search by name.')
            failures += 1
        fs = omniscript.find_forensic_search(fsl, fsl[0].id, 'id')
        if not fs:
            print('*** Failed to find first forensic search by id.')
            failures += 1

    gtl = engine.get_graph_template_list()
    print_graph_template_list(gtl)

    al = engine.get_audit_log()
    print_audit_log(al)
#     al.get_next(10)
#     print_audit_log(al)
# #    al.get_next()
# #    print_audit_log(al)

    ll = engine.get_trace_log_level()
    engine.set_trace_log_level(ll)

    # # TODO: ensure the path exists...
    log_file_path = os.path.abspath(os.path.join(_file_path, r'./log'))
    std_out_path = os.path.join(log_file_path, 'std_out.log')
    std_err_path = os.path.join(log_file_path, 'std_err.log')
    engine.redirect_standard_out(std_out_path, std_err_path)

    data_dir = engine.get_directory('/var/lib/omni/data')
    print_directory(data_dir)
    root_dir = engine.get_directory()
    print_directory(root_dir)

    ul = engine.get_user_list()
    if len(ul) == 1:
        print_user(ul[0])
    print_user_list(ul)

    cul = engine.get_connected_user_list()
    print_user_list(cul)
    return failures


def test_liveflow(engine, options):
    print('Liveflow Test')
    failures = 0

    default_config = (
        '{"output": {"record_types": [{"flowdir_enabled": true,"targets": [],"type": "avc"},{'
        '"targets": [],"type": "financial_services"},{"flow_time_interval": true,'
        '"flowdir_enabled": true,"targets": [],"type": "fnf"},{"flowdir_enabled": true,"targets": '
        '[],"type": "medianet"},{"flowdir_enabled": true,"targets": [],"type": "platform"},{'
        '"targets": [],"type": "signaling_dn"},{"byte_distribution_enabled": false,'
        '"first_data_pkt_enabled": false,"splt_enabled": true,"targets": [],"type": "sna"}],'
        '"targets": []},"preferences": {"active_flow_refresh_interval": 60,'
        '"config_check_interval": 1000,"debug_logging": 0,"decryption_enabled": false,'
        '"dhcp_analysis": true,"dns_analysis": true,"encrypted_traffic_analysis": {'
        '"eta_debug_logging": false},"enforce_tcp_3way_handshake": false,"flow_id": 0,'
        '"hashtable_size": 0,"hostname_analysis": true,"https_port": 443,"ipfix": {"max_payload": '
        '1500,"options_template_refresh_interval": 600,"template_refresh_interval": 600},'
        '"latency_enabled": true,"quality_enabled": false,"retransmissions_enabled": true,'
        '"rtp_enabled": true,"rtp_packets_disabled": false,"signaling_packet_window": 0,'
        '"tcp_handshake_timeout": 2000,"tcp_orphan_timeout": 15000,"tcp_packets_disabled": false,'
        '"tcp_post_close_timeout": 1000,"tcp_wait_timeout": 4000,"tls_analysis": true,'
        '"tls_packet_window": 16,"udp_packets_disabled": false,"udp_wait_timeout": 3000,'
        '"vlan_enabled": false,"voip_quality_percent": 25,"wan_mac_list": [],"web_enabled": false'
        '},"unit_tests": {"unittests_config_path": "./unit_tests/unit_tests_config.json"},'
        '"version": 18}'
    )

    liveflow_config = (
        '{"output": {"record_types": [{"flowdir_enabled": true,"targets": [1],"type": "avc"},'
        '{"targets": [1],"type": "financial_services"},{"flow_time_interval": true,'
        '"flowdir_enabled": true,"targets": [1],"type": "fnf"},{"targets": [1],'
        '"type": "signaling_dn"},{"byte_distribution_enabled": true,"first_data_pkt_enabled": true,'
        '"splt_enabled": true,"targets": [1],"type": "sna"}],'
        '"targets": [{"address": "170.229.96.18","enabled": true,"format": "json","id": 1,'
        '"max_batch_size": 1000000,"name": "Financial Services Telemetry",'
        '"transport_protocol": "kafka"},{"address": "170.229.96.18","enabled": true,'
        '"format": "ipfix","id": 1,"name": "LiveNX Telemetry","transport_protocol": "udp"},'
        '{"api_key": "","compression_enabled": true,"enabled": true,"format": "msgpack","id": 1,'
        '"max_batch_size": 6000000,"name": "ThreatEye Telemetry","ssl_host": "","ssl_uri": "",'
        '"transport_protocol": "websocket"}]},'
        '"preferences": {"active_flow_refresh_interval": 60,"config_check_interval": 1000,'
        '"debug_logging": 0,"decryption_enabled": false,"dhcp_analysis": false,'
        '"dns_analysis": false,"encrypted_traffic_analysis": {"eta_debug_logging": false},'
        '"enforce_tcp_3way_handshake": false,"flow_id": 0,"hashtable_size": 1000,'
        '"hostname_analysis": true,"https_port": 443,"ipfix": {"max_payload": 1500,'
        '"options_template_refresh_interval": 600,"template_refresh_interval": 600},'
        '"latency_enabled": true,"quality_enabled": true,"retransmissions_enabled": true,'
        '"rtp_enabled": true,"rtp_packets_disabled": false,"signaling_packet_window": 0,'
        '"tcp_handshake_timeout": 2000,"tcp_orphan_timeout": 60000,"tcp_packets_disabled": false,'
        '"tcp_post_close_timeout": 1000,"tcp_wait_timeout": 3000,"tls_analysis": true,'
        '"tls_packet_window": 16,"udp_packets_disabled": false,"udp_wait_timeout": 3000,'
        '"vlan_enabled": true,"voip_quality_percent": 25,"wan_mac_list": [{"ifidx": 7,'
        '"ifname": "router_1","mac": "22:33:44:55:66:77","mpls_label": 7,"vlan_id": 1,'
        '"vxlan_vni": 100}],"web_enabled": false},'
        '"version": 18}'
    )

    # Custom .run file does not support LiveFlow.
    liveflow_support = False
    capabilities = engine.get_capabilities()
    if capabilities:
        name_ids = omniscript.get_capability_name_ids()
        liveflow_id = name_ids.get('LiveFlow')
        module_list = engine.get_analysis_module_list()
        liveflow_plugin = omniscript.find_analysis_module(module_list, 'LiveFlow')
        liveflow_support = ((liveflow_id in capabilities.capability_list) and
                            (liveflow_plugin is not None))
    if not liveflow_support:
        print('LiveFlow is not supported on this engine.')
        return 0

    lf_config = None
    try:
        props = json.loads(liveflow_config)
        lf_config = omniscript.LiveFlowConfiguration(props)
        lf_props = lf_config._store(True)
        if lf_props == props:
            print('Success')
    except Exception as e:
        failures += 1
        if e:
            print(f'*** Failure: {e}')

    try:
        version = engine.get_version(True)
        print(f'Engine version: {version}')
        config = engine.get_liveflow_configuration()
        print_liveflow_configuration(config)
    except Exception as e:
        failures += 1
        if e:
            print(f'*** Failed get_liveflow_configuration: {e}')

    try:
        context = engine.get_liveflow_context()
        print_liveflow_context(context)
    except Exception as e:
        failures += 1
        if e:
            print(f'*** Failed get_liveflow_context: {e}')

    try:
        status = engine.get_liveflow_status()
        print_liveflow_status(status)
    except Exception as e:
        failures += 1
        if e:
            print(f'*** Failed get_liveflow_status: {e}')

    try:
        reboot = engine.set_liveflow_configuration(lf_config)
        if reboot:
            engine.restart()
            st = engine.get_status()
            print_engine_status(st)
        print(f'    Reboot: {reboot}')
    except Exception as e:
        failures += 1
        if e:
            print(f'*** Failed set_liveflow_configuration to custom: {e}')

    try:
        reboot = engine.set_liveflow_configuration(default_config)
        if reboot:
            engine.restart()
            if not engine.is_connected():
                options.login()
                st = engine.get_status()
                print_engine_status(st)
        print(f'    Reboot: {reboot}')
    except Exception as e:
        failures += 1
        if e:
            print(f'*** Failed set_liveflow_configuration to default: {e}')

    return failures


def test_miscellaneous(engine):
    print('Miscellaneous Test')
    failures = 0

    class_ids = omniscript.omniscript.get_class_name_ids()
    id_classes = omniscript.omniscript.get_id_class_names()
    id_capabilities = omniscript.omniscript.get_id_capability_names()
    protocol_names = omniscript.omniscript.get_id_protocol_names()
    protocol_short_name = omniscript.omniscript.get_id_protocol_short_names()
    id_stats = omniscript.omniscript.get_id_stat_names()
    protocol_short_name_ids = omniscript.omniscript.get_protocol_short_name_ids()

    print(class_ids)
    print(id_classes)
    print(id_capabilities)
    print(protocol_names)
    print(protocol_short_name)
    print(id_stats)
    print(protocol_short_name_ids)

    app_list = engine.get_application_list()
    capt_list = engine.get_capture_list()
    co_list = engine.get_country_list()
    co_names = omniscript.create_country_name_dictionary(co_list)
    co_codes = omniscript.create_country_code_dictionary(co_list)

    print_application_list(app_list)
    print(capt_list)
    print(co_list)
    print(co_names)
    print(co_codes)

    caps = engine.get_capabilities()
    class_names = omniscript.get_id_class_names()
    cap__names = omniscript.get_id_capability_names()
    print_capabilities(caps, class_names, cap__names)

    print()

    # if len(cl) > 0:
    #    capture = cl[0]
    #    ## Forensic Template
    #    f_template = omniscript.ForensicTemplate()
    #    f_template.name = 'test_forensic_search'
    #    f_template.capture_name = capture.name
    #    f_template.start_time = capture.start_time
    #    f_template.end_time = capture.stop_time
    #    f_template.option_packets = True
    #    f_template.limit = 0
    #    fs = engine.create_forensic_search(f_template)
    #    engine.delete_forensic_search(fs)

    # ffl = engine.get_forensic_file_list()
    # if ffl and len(ffl) > 0:
    #    ff = ffl[0]
    #    ft = omniscript.ForensicTemplate()
    #    ft.name = 'Python Forensic Search'
    #    ft.add_file(ff.path)
    #    fs.start_time = ff.start_time
    #    fs.end_time = ff.stop_time
    #    ft.option_packets = True
    #    ft.limit = 0
    #    fs = engine.create_forensic_search(ft)
    #    for i in range(fs_refresh_count):
    #        fs.refresh()
    #    print_forensic_search(fs)

    emailCaptureId = None
    ml = engine.get_analysis_module_list()
    m = omniscript.find_analysis_module(ml, 'EmailCaptureOE')
    if m is not None:
        emailCaptureId = m.id

    if emailCaptureId:
        pass
    #     msg = '<GetAllOptions/>'
    #     buf = struct.pack('=QQ%ss' % len(msg), len(msg), 0, msg )
    #     response = engine.send_plugin_message(emailCaptureId, None, buf)
    #     if response and len(response) > 0:
    #         with open(os.path.join(temp_path, 'getalloptions.bin'), 'wb') as log:
    #             log.write(response)
    #         est_len = len(response) - 44
    #         (response_length, captId, plugId, result_size, result_code, result) =
    #             struct.unpack('I16s16sIi%ss' % est_len, response)
    #         print(response_length)
    #         print(captId)
    #         print(plugId)
    #         print(result_size)
    #         if result_code == 0 and len(result) > 0:
    #             xml_len = len(result) - 16
    #             (text_len, bin_len, xml) = struct.unpack('QQ%ss' % xml_len, result)
    #             print(text_len)
    #             print(bin_len)
    #             print(xml)

    timeout = engine.timeout
    engine.timeout = 1
    try:
        status = engine.get_status()
        print_engine_status(status)
    except omniscript.OmniError as error:
        print(error.message)
        if error.code != E_TIMEOUT:
            print('*** Failed Miscellaneous test')
            failures += 1
    except Exception:
        print('Caught some other error.')

    engine.timeout = timeout

    return failures


def test_packets(engine, capture_name, packets_needed):
    print('Packets Test')
    failures = 0

    adpt = get_default_adapter(engine, 'eno3')

    capt = engine.find_capture(capture_name)
    if capt:
        engine.delete_capture(capt)
        capt = None

    if not capt:
        ct = omniscript.CaptureTemplate()
        if adpt:
            ct.set_adapter(adpt)
        ct.general.buffer_size = BYTES_PER_MEGABYTE
        ct.general.name = capture_name
        ct.general.option_continuous_capture = True
        ct.general.option_capture_to_disk = True
        ct.general.option_start_capture = True
        ct.set_all(True)
        capt = engine.create_capture(ct)
        if not capt:
            print('*** Failed Packets to create capture.')
            failures += 1
            return failures
    while capt.packets_filtered < packets_needed:
        get_traffic()
        time.sleep(1)
        capt.refresh()
    capt.stop()
    capt.refresh()
    if capt.packets_filtered < packets_needed:
        print('*** Failed Packets - Not enough packets.')
        failures += 1
        return failures

    try:
        pl = capt.get_packets(capt.first_packet, 3)
        if pl:
            p = pl[0]
            print_packet(p)

            dc_plain = capt.get_packet_decode(1, omniscript.DECODE_PLAIN_TEXT)
            print(dc_plain)
            dc_html = capt.get_packet_decode(1, omniscript.DECODE_HTML)
            print(dc_html)
            dc_taged = capt.get_packet_decode(1, omniscript.DECODE_TAG_STREAM)
            print(dc_taged)
    except omniscript.OmniError as err:
        print(f'OmniError: {err.message}')
        print('*** Failed Packets - to get packets.')
        failures += 1

    # pl = capt.get_packets((capt.first_packet,capt.first_packet + 9))
    # if len(pl) != 10:
    #     print('Did not get 10 packets.')
    # print_packet_list(pl)

#     for p in pl:
#         dp = omniscript.DecodedPacket(p)
#         print(dp)

#     if False:
#         next_packet = capt.first_packet
#         last_packet = capt.packet_count - 1
#         with open(os.path.join(temp_path, 'packet_info.txt'), 'w') as fle:
#             while next_packet < last_packet:
#                 count = last_packet - next_packet
#                 if count > 49:
#                     count = 49
#                 pl = capt.get_packets((next_packet, next_packet + count))
#                 for p in pl:
#                     fle.write('%d : %s\n' % (p.number, p.timestamp.ctime()))
#                 next_packet += count + 1
    return failures


def test_remote_engine(engine):
    failures = 0
    rel = engine.get_remote_engine_list()
    print_remote_engine_list(rel)

    if len(rel) > 1:
        engine.delete_remote_engine(rel[0])
        one_less = engine.get_remote_engine_list()
        if len(one_less) >= len(rel):
            print('*** Failed to delete one RemoteEngine.')
            failures += 1

    engine.delete_all_remote_engines()
    empty_rel = engine.get_remote_engine_list()
    if len(empty_rel) > 0:
        print('*** Failed to delete all RemoteEngines')
        failures += 1
    engine.add_remote_engine(rel)
    verify_rel = engine.get_remote_engine_list()
    if len(verify_rel) != len(rel):
        print('*** Failed to restore RemoteEngines.')
        failures += 1

    re = omniscript.find_remote_engine(rel, 'cegsrvr2')
    if re:
        e = engine.get_remote_engine(re.id)
        print_remote_engine(e)

        group = e.group
        e.group = 'OmniScript'
        engine.update_remote_engine(e)
        print_remote_engine(e)

        e.group = group
        engine.update_remote_engine(e)
        print_remote_engine(e)
    return failures


# def test_reports(engine, capture_name, capture_file, packets_needed):
#     print('Reports Test')
#     failures = 0

#     fl = engine.get_file_list()
#     ffi = list(i for i in fl if i.name == capture_file)
#     if len(ffi) == 0:
#         sf_filename = os.path.normpath(os.path.join(shared_files, capture_file))
#         engine.send_file(sf_filename)
#     fl = engine.get_file_list()
#     ffi = list(i for i in fl if i.name == capture_file)
#     if len(ffi) == 0:
#         print('*** Failed to send file to engine: %s' % capture_file)
#         failures += 1
#         return failures

#     cl = engine.get_capture_list()
#     cli = list(i for i in cl if i.name == capture_name)
#     engine.delete_capture(cli)

#     cf_path = fl[0].name + capture_file # do not use os.path.join
#     fa = omniscript.FileAdapter(cf_path)
#     fa.limit = 1
#     fa.speed = 0.0
#     ct = omniscript.CaptureTemplate()
#     ct.set_adapter(fa)
#     ct.general.buffer_size = 10 * BYTES_PER_MEGABYTE
#     ct.general.name = capture_name
#     ct.general.option_continuous_capture = True
#     ct.general.option_capture_to_disk = False
#     ct.general.option_start_capture = False
#     ct.general.option_timeline_app_stats = True
#     ct.general.option_timeline_stats = True
#     ct.general.option_timeline_top_stats = True
#     ct.general.option_timeline_voip_stats = True
#     ct.analysis.option_alarms = True
#     ct.analysis.option_analysis_modules = True
#     ct.analysis.option_application = True
#     ct.analysis.option_compass = True
#     ct.analysis.option_country = True
#     ct.analysis.option_error = True
#     ct.analysis.option_expert = True
#     ct.analysis.option_network = True
#     ct.analysis.node_protocol_detail_limit.enabled = True
#     ct.analysis.node_limit.enabled = True
#     ct.analysis.protocol_limit.enabled = True
#     ct.analysis.option_size = True
#     ct.analysis.option_summary = True
#     ct.analysis.option_traffic = True
#     ct.analysis.option_voice_video = True
#     ct.stop_trigger.enabled = True
#     ct.stop_trigger.time.enabled = True
#     ct.stop_trigger.time.option_use_elapsed = True
#     ct.stop_trigger.time.time = 30 * 1000000000L # 10 seconds.
#     ct.stop_trigger.captured.enabled = True
#     ct.stop_trigger.captured.bytes = (2129405 + 64)
#     capt = engine.create_capture(ct)
#     if capt is None:
#         print('Failed to create capture.')
#         failures += 1
#         return failures

#     capt.start()
#     capt.refresh()
#     print(capt.format_status())
#     while (capt.status & 0x0001) and (capt.packets_filtered < packets_needed):
#         get_traffic()
#         capt.refresh()
#     capt.stop()
#     capt.refresh()
#     print(capt.format_status())
#     print(capt.packets_filtered)

#     apps = capt.get_application_stats()
#     calls = capt.get_call_stats()
#     nodes = capt.get_node_stats()
#     protos = capt.get_protocol_stats()
#     sums = capt.get_summary_stats()

#     if apps:
#         print(apps)

#     if calls:
#         print(calls)

#     if nodes:
#         print('\nNode Statistisc Report: IPv4')
#         with open(node_report[0], 'w') as report:
#             report.write(omniscript.NodeStatistic.report_header(node_columns))
#             print(omniscript.NodeStatistic.report_header(node_columns, newline=False))
#             for n in nodes:
#                 if n.is_spec(omniscript.MEDIA_CLASS_ADDRESS, omniscript.MEDIA_SPEC_IP_ADDRESS):
#                     report.write(n.report(node_columns))
#                     print n.report(node_columns, newline=False)
#         print('\nNode Statistisc Report: IPv6')
#         with open(node_report[1], 'w') as report:
#             report.write(omniscript.NodeStatistic.report_header(node_columns))
#             print(omniscript.NodeStatistic.report_header(node_columns, newline=False))
#             for n in nodes:
#                 if n.is_spec(omniscript.MEDIA_CLASS_ADDRESS, omniscript.MEDIA_SPEC_IPV6_ADDRESS):
#                     report.write(n.report(node_columns))
#                     print(n.report(node_columns, newline=False))
#         print('\nNode Statistisc Report: Ethernet')
#         with open(node_report[2], 'w') as report:
#             report.write(omniscript.NodeStatistic.report_header(node_columns))
#             print(omniscript.NodeStatistic.report_header(node_columns, newline=False))
#             for n in nodes:
#                 if n.is_spec(omniscript.MEDIA_CLASS_ADDRESS,
#                              omniscript.MEDIA_SPEC_ETHERNET_ADDRESS):
#                     report.write(n.report(node_columns))
#                     print(n.report(node_columns, newline=False))
#     else:
#         print('\nFailed to get node stats.')
#         failures += 1

#     if protos:
#         print('\nProtocol Statistisc Report')
#         with open (protocol_report, 'w') as report:
#             report.write(omniscript.ProtocolStatistic.report_header())
#             print(omniscript.ProtocolStatistic.report_header(newline=False))
#             p_flat = omniscript.protocolstatistic.flatten(protos, True)
#             for p in p_flat:
#                 report.write(p.report())
#                 print(p.report(newline=False))
#     else:
#         print('\nFailed to get protocol stats.')
#         failures += 1

#     gen_lbls = [
#         'Start Date',
#         'Start Time',
#         'Duration',
#         'Trigger Count'
#         ,'Trigger Wait Time',
#         'Dropped Packets',
#         'Duplicate Packets Discarded']
#     if sums:
#         for lbl in gen_lbls:
#             print(sums['General'][lbl].report(newline=False))
#         print

#         nt_lbls = [
#             'Total Bytes',
#             'Total Packets',
#             'Total Broadcast',
#             'Total Multicast',
#             'Average Utilization (percent)',
#             'Average Utilization (bits/s)',
#             'Current Utilization (percent)',
#             'Current Utilization (bits/s)']
#         for lbl in nt_lbls:
#             print(sums['Network'][lbl].report(newline=False))
#         print

#         print '\nSummary Statistisc Report'
#         groups = list(g for g, gg in sums.items())
#         groups.sort()
#         with open (summary_report, 'w') as report:
#             report.write(omniscript.SummaryStatistic.report_header())
#             print(omniscript.SummaryStatistic.report_header(newline=False))
#             for g in groups:
#                 for _, v in sums[g].items():
#                     report.write(v.report())
#                     print(v.report(newline=False))
#     else:
#         print('\nFailed to get summary stats.')
#         failures += 1

#     return failures


# def test_select_related(engine, capt_args):
#     print('Select Related Test')
#     failures = 0

#     cap = create_capture(engine, *capt_args)
#     if not cap:
#         failures += 1
#         return failures
#     related = cap.select_related([1,4], omniscript.SELECT_BY_CONVERSATION)
#     print(related)
#     return failures


# def test_acl(engine):
#     print('ACL Test')
#     failures = 0

#     acl = engine.get_access_control_list()
#     print_access_control_list(acl)
#     return failures


# def test_wireless(engine):
#     print('Wireless Test')
#     failures = 0

#     hwo_list = engine.get_hardware_options_list()
#     if not hwo_list:
#         return failures
#     print_hardware_options_list(hwo_list, False)

#     engine.set_hardware_options(hwo_list)
#     engine.set_hardware_options(hwo_list)
#     engine.set_hardware_options(hwo_list)
#     engine.set_hardware_options(hwo_list)


#     print_hardware_options_list(hwo_list)
#     ho = hwo_list[0]
#     if not isinstance(ho, omniscript.WirelessHardwareOptions):
#         failures += 1
#         return failures

#     al = engine.get_adapter_list()
#     print(al)
#     wa = engine.find_adapter('Wi-Fi')
#     if not wa:
#         return failures

#     ac = engine.get_adapter_configuration(wa)
#     print_adapter_configuration(ac)

#     ch2_list = ho.find_channel_scanning_entry(2)
#     print ch2_list
#     ch2 = ch2_list[0]
#     ho.set_channel(ch2)
#     ho.set_channel_scanning(False)

#     engine.set_hardware_options(ho)
#     engine.set_adapter_configuration(ac)

#     t_hwo_list = engine.get_hardware_options_list()
#     if not t_hwo_list:
#         return failures
#     t_ho = t_hwo_list[0]
#     if t_ho.configuration != omniscript.WIRELESS_CONFIGURATION_SINGLE_CHANNEL:
#         failures += 1
#     if t_ho.channel_number != ch2.channel_number:
#         failures += 1
#     if t_ho.channel_frequency != ch2.channel_frequency:
#         failures += 1
#     if t_ho.channel_band != ch2.channel_band:
#         failures += 1
#     if failures > 0:
#         return failures

#     ho.set_channel_scanning(True)
#     engine.set_hardware_options(ho)
#     engine.set_adapter_configuration(ac)

#     t_hwo_list = engine.get_hardware_options_list()
#     if not t_hwo_list:
#         return failures
#     t_ho = t_hwo_list[0]

#     ho.set_channel(ho.channel_scanning[0])
#     ho.set_channel_scanning(False)
#     engine.set_hardware_options(ho)
#     engine.set_adapter_configuration(ac)
#     return failures


def test_restart(engine):
    print('Restart Test')
    failures = 0

    if not engine.is_connected():
        print('*** Failed Test Restart - Engine not connected.')
        failures += 1
        # if not connect_to_engine(engine, auth, domain, user, pwd):
        #     print('*** Failed Test Restart - Failed initial engine connection.')
        #     failures += 1
        return failures

    engine.restart()
    if engine.is_connected():
        print('*** Failed Test Restart - is_connected after restart failure.')
        failures += 1

    # Don't reconnect
    # attempt = 0
    # while not engine.is_connected():
    #     time.sleep(2)
    #     attempt += 1
    #     try:
    #         engine.connect(auth, domain, user, pwd)
    #     except Exception:
    #         if attempt > 10:
    #             print('*** Failed to reconnect after restart: %d' % attempt)
    #             failures += 1
    #             return failures
    # if not engine.is_connected():
    #     print('*** test_restart - is_connected after reconnect failure.')
    #     failures += 1
    # try:
    #     al = engine.get_adapter_list()
    #     print(al)
    # except Exception:
    #     print('*** Failed to get adapter list after reset.')
    #     failures += 1
    return failures


# def test_tcpdump_adapter(engine):
#     print('TCP Dump Adapter Test')
#     failures = 0

#     remove_adapters = True
#     tcpdump_test = [True, True, True, True]
#     adapters_to_delete = []

#     if remove_adapters:
#         eal = engine.get_adapter_list()
#         atd = [a for a in eal if a.adapter_type == omniscript.ADAPTER_TYPE_PLUGIN]
#         engine.delete_adapter(atd)

#     if tcpdump_test[0]:
#         tcpdump = omniscript.TCPDump(engine, '10.4.2.78')  # optiplex Ubuntu 14.04
#         tcpdump.login('root', 'liveaction')
#         interface_list = tcpdump.get_adapter_list()
#         interface = None
#         for i in interface_list:
#             if i.name == 'eth0':
#                 interface = i
#                 break
#         if interface:
#             template = omniscript.TCPDumpTemplate(interface)
#             new_adapter_name = tcpdump.create_adapter(template)
#             if not new_adapter_name:
#                 failures += 1
#             print('Created new adapter: %s' % new_adapter_name)
#         else:
#             failures += 1
#         eal = engine.get_adapter_list()
#         if eal:
#             new_adapter = find_adapter(eal, new_adapter_name)
#             print_adapter(new_adapter)
#             adapters_to_delete.append(new_adapter)

#     if tcpdump_test[1]:
#         tcpdump = omniscript.TCPDump(engine, '10.4.2.151')
#         pk = open('10.4.2.151.tsadmin_key.txt').read()
#         tcpdump.login('tsadmin', private_key=pk)
#         # ens160, ens192, ens224, lo
#         interface_list = tcpdump.get_adapter_list()
#         interface = next((i for i in interface_list if i.name == 'ens192'), None)
#         new_adapter_name = None
#         if interface:
#             template = omniscript.TCPDumpTemplate(interface)
#             new_adapter_name = tcpdump.create_adapter(template)
#             if not new_adapter_name:
#                 failures += 1
#             print('Created new adapter: %s' % new_adapter)
#         else:
#             failures += 1
#         eal = engine.get_adapter_list()
#         if eal:
#             new_adapter = find_adapter(eal, new_adapter_name)
#             print_adapter(new_adapter)
#             adapters_to_delete.append(new_adapter)

#     if tcpdump_test[2]:
#         tcpdump = omniscript.TCPDump(engine, '10.4.2.78')
#         template = omniscript.TCPDumpTemplate('eth1')
#         new_adapter_name = tcpdump.create_adapter(template, 'root', 'liveaction')
#         if not new_adapter_name:
#             failures += 1
#         print('Created new adapter: %s' % new_adapter)
#         eal = engine.get_adapter_list()
#         if eal:
#             new_adapter = find_adapter(eal, new_adapter_name)
#             print_adapter(new_adapter)
#             adapters_to_delete.append(new_adapter)

#     if tcpdump_test[3]:
#         tcpdump = omniscript.TCPDump(engine, '10.4.2.151')
#         pk = open('10.4.2.151.tsadmin_key.txt').read()
#         tcpdump.set_credentials('tsadmin', private_key=pk)
#         # ens160, ens192, ens224, lo
#         template = omniscript.TCPDumpTemplate('ens160')
#         new_adapter_name = tcpdump.create_adapter(template)
#         if not new_adapter_name:
#             failures += 1
#         print('Created new adapter: %s' % new_adapter)
#         eal = engine.get_adapter_list()
#         if eal:
#             new_adapter = find_adapter(eal, new_adapter_name)
#             print_adapter(new_adapter)
#             adapters_to_delete.append(new_adapter)

#     if len(adapters_to_delete) > 0:
#         old_adapters = engine.get_adapter_list()
#         if len(old_adapters) == 0:
#             failures += 1
#         else:
#             engine.delete_adapter(adapters_to_delete)
#             new_adapters = engine.get_adapter_list()
#             if len(old_adapters) != len(adapters_to_delete) + len(new_adapters):
#                 failures += 1
#     else:
#         print('No adapters to delete.')
#     return failures


# def test_lauren_test(engine):
#     print('Lauren Test')
#     failures = 0

#     ### Create capture template
#     capTemplate = omniscript.CaptureTemplate('Lauren-CaptureTemplate.xml')
#     capTemplate.adapter.name = 'Local Area Connection'
#     capTemplate.general.name = 'Lauren Test'
#     capTemplate.general.file_pattern = 'Lauren Test-'
#     capTemplate.add_filter('HTTP')
#     capTemplate.filter.mode = 3  # REJECT Matching Any
#     cap = engine.create_capture(capTemplate)
#     print(cap)

#     return failures


def test_legacy_connection(omni, opt):
    failures = 0
    auth = ''
    domain = ''
    pwd = omni_options.get_password(opt.host, opt.user)
    legacy_engine = omni.connect(opt.host, opt.port, auth, domain, opt.user, pwd)
    if not legacy_engine:
        omni.critical('Legacy connection failed. Failed to create an engine.')
        print('*** Failed Legacy Connection - 1')
        failures += 1
        return failures

    ic = legacy_engine.is_connected()
    if not ic:
        omni.critical('Legacy connection failed. Not connected to an engine.')
        print('*** Failed Legacy Connection - 2')
        failures += 1
        return failures

    legacy_engine.disconnect()
    ic = legacy_engine.is_connected()
    if ic:
        omni.critical('Disconnect after legacy connection from engine failed.')
        print('*** Failed Legacy Connection - 3')
        failures += 1
    legacy_engine = None
    return failures


def capture_plugin_setup(engine, cpo: dict):
    # Check for needed plugins: FolderAdapterOE, CefPrefsOE-1
    module_list = engine.get_analysis_module_list()
    folder_adapter = omniscript.find_analysis_module(module_list, 'FolderAdapterOE')
    if folder_adapter is None:
        print('Failed to find FolderAdapterOE plugin.')
        return
    cef_prefs_1 = omniscript.find_analysis_module(module_list, 'CefPrefsOE-1')
    if cef_prefs_1 is None:
        print('Failed to find the CefPrefsOE-1 plugin.')
        return

    ct = omniscript.CaptureTemplate()
    adpt = None
    capt = None
    addr_flt = None

    # Find and set the FolderAdapterOE adapter monitoring monitor_folder.
    ad_list = engine.get_adapter_list()
    adpt = omniscript.find_adapter(ad_list, cpo['monitor_folder'])

    # Set the adapter if found, else create it.
    if isinstance(adpt, omniscript.Adapter):
        ct.set_adapter(adpt)
    else:
        adapter_id = omniscript.OmniId(True)
        mask = '*.pcap'
        speed = 100
        save = ''

        create_adapter_msg = (
            '<CreateAdapter>'
            '<FolderAdapter>'
            f'<Id>{adapter_id}</Id>'
            f'<Monitor>{cpo["monitor_folder"]}</Monitor>'
            f'<Mask>{mask}</Mask>'
            f'<Speed>{speed}</Speed>'
            f'<Save>{save}</Save>'
            '</FolderAdapter>'
            '</CreateAdapter>'
        )
        engine.send_plugin_message(folder_adapter, create_adapter_msg)

        ad_list = engine.get_adapter_list()
        adpt = omniscript.find_adapter(ad_list, cpo['monitor_folder'])
        if isinstance(adpt, omniscript.Adapter):
            ct.set_adapter(adpt)
        else:
            print(f'Failed to find or create FolderAdapterOE : {cpo["monitor_folder"]}')
            return

    # Delete existing filters.
    flt_lst = engine.get_filter_list()
    addr_flts = omniscript.find_all_filters(flt_lst, cpo['filter_name'])
    engine.delete_filter(addr_flts)

    # Create new Address Filter.
    addr_flt = omniscript.Filter(filter_name)
    addr_flt.comment = cpo['filter_comment'] % cpo['ip_address']
    addr_node = omniscript.AddressNode()
    addr_node.address_1 = omniscript.IPv4Address(cpo['ip_address'])
    addr_node.accept_1_to_2 = True
    addr_node.accept_2_to_1 = True
    addr_flt.criteria = addr_node
    engine.add_filter(addr_flt)
    print_filter(addr_flt)
    print()

    ct.general.name = cpo['capture_name']
    ct.general.buffer_size = 10 * BYTES_PER_MEGABYTE
    ct.general.comment = cpo['capture_comment']
    ct.general.directory = os.path.join(temp_path, capture_name)
    ct.general.file_pattern = cpo['capture_name'] + '-'
    ct.general.file_size = 128 * BYTES_PER_MEGABYTE
    ct.general.keep_last_files_count = 5
    ct.general.max_file_age = SECONDS_PER_HOUR
    ct.general.max_total_file_size = BYTES_PER_GIGABYTE
    ct.general.tap_timestamps = TAP_TIMESTAMPS_DEFAULT
    ct.general.option_capture_to_disk = True
    ct.general.option_continuous_capture = True
    ct.general.option_deduplicate = True
    ct.general.option_file_age = True
    ct.general.option_keep_last_files = True
    ct.general.option_priority_ctd = True
    ct.general.option_start_capture = False
    ct.general.option_total_file_size = True

    ct.analysis.option_network = True
    ct.analysis.option_summary = True

    ct.filter.mode = omniscript.FILTER_MODE_ACCEPT_MATCHING_ANY
    ct.add_filter(addr_flt)

    ct.plugins.modules = [cef_prefs_1]
    # Note this sets the configuration of the object in module_list.
    cef_prefs_1.set_configuration(
        '<Case>Alpha</Case>'
        '<Case>Beta</Case>'
        '<Case>Delta</Case>'
        '<Notes>Quick Test</Notes>'
    )

    try:
        capt = engine.create_capture(ct)
        if capt is None:
            print('*** Failed to create capture.')
        print_capture(capt)
    except Exception:
        print('Failed to create capture.')

    return (engine, capt, addr_flt, adpt)


def capture_plugin_run(state: tuple, file_name: str):
    (engine, capt, addr_flt, adpt) = state
    if not isinstance(engine, omniscript.OmniEngine) or not isinstance(capt, omniscript.Capture):
        return

    file_path = os.path.dirname(__file__)
    data_file = os.path.abspath(os.path.join(file_path, r'files', file_name))
    print(data_file)
    engine.send_file(data_file)

    capt.start()

    dir = engine.get_directory(adpt.name)
    print_directory(dir)

    time.sleep(5)

    capt.stop()


def capture_plugin_teardown(state: tuple):
    (engine, capt, addr_flt, adpt) = state
    if not isinstance(engine, omniscript.OmniEngine):
        return

    if isinstance(capt, omniscript.Capture):
        engine.delete_capture(capt)
    if addr_flt:
        engine.delete_filter(addr_flt)
    if adpt:
        engine.delete_adapter(adpt)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  main
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def main(args):
    global options
    options = omni_options.Options('PyTest.py', args)
    if options.help:
        options.print_help()
        return

    # Create the OmniScript object.
    omni = omniscript.OmniScript(level=2, flags=omniscript.OMNI_FLAG_NO_HTTPS_WARNINGS)

    omni.set_log_file(os.path.join(temp_path, 'PyTest-log.log'), 'w')
    omni.info('PyTest: Begin')
    print('PyTest: Begin')
    omni.info(f'OmniScript Version: {omniscript.__version__} Build {omniscript.__build__}')
    print(f'OmniScript Version: {omniscript.__version__} Build {omniscript.__build__}')

    engine = options.create_engine(omni)
    omni.info(f'PyTest: Engine: {options.host}')
    print(f'PyTest: Engine: {options.host}')
    if not engine:
        print('Failed to create the engine.')
        return

    omni.info(f'PyTest:   User: {options.user}')
    print(f'PyTest:   User: {options.user}')
    if not options.login(engine):
        print('Failed to connect to the engine')
        return

    if bPerformance_Logging:
        engine.start_performance_logging(os.path.join(temp_path, 'PyTest-perf.log'), 'w')

    ver = engine.get_version()
    omni.info(f'OmniEngine Version: {ver}')
    print(f'OmniEngine Version: {ver}')

    print
    es = engine.get_status()
    print_engine_status(es)

    failures = 0
    unit_tests_failures = 0
    gets_failures = 0
    adapters_failures = 0
    filters_failures = 0
    filter_all_failures = 0
    delete_all_failures = 0
    file_ops_failures = 0
    capt_create_failures = 0
    capture_all_failures = 0
    file_database_operations_failures = 0
    # file_adapter_failures = 0
    packets_failures = 0
    capture_stats_failures = 0
    # reports_failures = 0
    forensic_template_failures = 0
    # forensic_stats_failures = 0
    miscellaneous_failures = 0
    restart_failures = 0
    # diagnostics_failures = 0
    # flows_failures = 0
    # select_related_failures = 0
    # tcpdump_failures = 0
    audit_log_failures = 0
    event_log_failures = 0
    # acl_failures = 0
    # wireless_failures = 0
    # legacy_connection_failures = 0
    remote_engine_failures = 0

    messages = []

    # et = omniscript.EngineTimeout()
    # print(et)
    # et = omniscript.EngineTimeout(20.1, 5.2)
    # print(et)
    # et = omniscript.EngineTimeout('35.2, 3.2')
    # print(et)
    # et = omniscript.EngineTimeout('60.3, 13.3')
    # print(et)
    # et2 = omniscript.EngineTimeout(et)
    # print(et2)

    # version = engine.get_version()
    # print(f'version: {version}')
    # engine.create_directory('/tmp/xyzzy')
    # engine.create_directory('/tmp/xyzzy')
    # engine.create_directory('/tmp/xyzzy')
    # engine.create_file('/tmp/xyzzy/alpha.txt')
    # engine.create_file('/tmp/xyzzy/alpha.txt')
    # dir = engine.get_directory('/tmp/xyzzy')
    # print_directory(dir)
    # engine.create_directory('/tmp/xyzzy/omni')
    # engine.create_directory('/tmp/xyzzy/peek')
    # engine.create_directory('/tmp/xyzzy/engine')
    # dir = engine.get_directory('/tmp/xyzzy')
    # print_directory(dir)
    # txt = engine.get_file('/tmp/xyzzy/alpha.txt')
    # print('alpha.txt')
    # print(txt)
    # print('/alpha.txt')

    # print(f'cwd: {os.getcwd()}')
    # print(f'this file: {__file__}')
    # adr = 'addrelativepath.py'
    # adr_path = os.path.abspath(os.path.join(_file_path, adr))
    # cnt = engine.send_file(adr_path)
    # print(f'Wrote bytes: {cnt}')

    # adr_txt = engine.get_file(adr)
    # print('addrelativepath.py')
    # print(adr_txt)
    # print('/addrelativepath.py')

    # adr_txt = engine.get_file(adr, True)
    # print('addrelativepath.py')
    # print(adr_txt)
    # print('/addrelativepath.py')

    # print()

    # is_stale = engine._is_filter_list_stale()
    # if is_stale:
    #     engine.get_filter_list()
    # is_stale = engine._is_filter_list_stale()

    # caps = engine.get_capabilities()
    # print_engine_capabilities(caps)

    # for i in omniscript.ProtocolLayer:
    #     print(i.value, i.label())

    # ep = engine.get_expert_preferences()
    # print_expert_preferences(ep)

    if do_unit_tests:
        unit_tests_failures, unit_tests_messages = test_unit_tests(engine)
        if unit_tests_failures:
            messages.extend(unit_tests_messages)
        failures += unit_tests_failures

    # Don't move test_event_log() into alphabetical sort order.
    # test_event_log() needs the captures created by test_unit_tests().
    if do_event_log:
        event_log_failures, event_log_messages = test_event_log(engine)
        if event_log_failures:
            messages.append(f'Test Event Log failures: {event_log_failures}')
            messages.extend(event_log_messages)
        failures += event_log_failures

    # if do_acl:
    #     acl_failures = test_acl(engine)
    #     if acl_failures:
    #         messages.append(f'Test ACL failures: {acl_failures}')
    #     failures += acl_failures

    if do_adapters:
        adapters_failures = test_adapters(engine)
        if adapters_failures:
            messages.append(f'Test Adapter failures: {adapters_failures}')
        failures += adapters_failures

    if do_audit_log:
        audit_log_failures = test_audit_log(engine)
        if audit_log_failures:
            messages.append(f'Test Event Log failures: {audit_log_failures}')
        failures += audit_log_failures

    if do_capt_create:
        capt_create_failures = test_capt_create(engine, capture_name, 'HTTP', 1000)
        if capt_create_failures:
            messages.append(f'Test Capture Create failures: {capt_create_failures}')
        failures += capt_create_failures

    if do_capture_all:
        capture_all_failures = test_capture_all(engine)
        if capture_all_failures:
            messages.append(f'Test Capture Create All failures: {capture_all_failures}')
        failures += capture_all_failures

    if do_capture_stats:
        capture_stats_failures = test_capture_stats(engine, stats_capture_name, 546553)
        if capture_stats_failures:
            messages.append(f'Test Capture Stats failures: {capture_stats_failures}')
        failures += capture_stats_failures

    if do_delete_all:
        delete_all_failures = test_delete_all(engine)
        if delete_all_failures:
            messages.append(f'Test Delete All failures: {delete_all_failures}')
        failures += delete_all_failures

    if do_file_ops:
        file_ops_failures = test_file_ops(engine, packet_file_name, result_file)
        if file_ops_failures:
            messages.append(f'Test File Ops failures: {file_ops_failures}')
        failures += file_ops_failures

    if do_filters:
        filters_failures = test_filters(engine, filter_name)
        if filters_failures:
            messages.append(f'Test Filters failures: {filters_failures}')
        failures += filters_failures

    if do_filter_all:
        filter_all_failures = test_filter_all_test(engine)
        if filter_all_failures:
            messages.append(f'Test Filter All failures: {filter_all_failures}')
        failures += filter_all_failures

    # if do_file_adapter:
    #     save_all_names = [save_all_name_engine, save_all_name_capture]
    #     file_adapter_failures = test_file_adapter(engine, packet_file_name, capture_name,
    #                                 packets_needed, save_all_names)
    #     if file_adapter_failures:
    #         messages.append(f'Test File Adapter failures: {file_adapter_failures}')
    #     failures += file_adapter_failures

    if do_file_database_operations:
        file_database_operations_failures = test_file_database_operations(engine)
        if file_database_operations_failures:
            messages.append(
                f'Test File Database Operations failures: {file_database_operations_failures}')
        failures += file_database_operations_failures

    # if do_flows:
    #     flows_failures = test_flows_test(engine, fortworth_capture, ipv6_capture)
    #     if flows_failures:
    #         messages.append(f'Test Flows failures: {flows_failures}')
    #     failures += flows_failures

    if do_forensic_template:
        forensic_template_failures = test_forensic_template(engine, forensic_name)
        if forensic_template_failures:
            messages.append(f'Test Forensic Template failures: {forensic_template_failures}')
        failures += forensic_template_failures

    if do_forensic_template_all:
        forensic_template_all_failures = test_forensic_template_all(engine)
        if forensic_template_all_failures:
            messages.append(
                f'Test Forensic Template All failures: {forensic_template_all_failures}')
        failures += forensic_template_all_failures

    # if do_forensic_stats:
    #     forensic_stats_failures = test_forensic_stats(engine, forensic_name, 1000)
    #     if forensic_stats_failures:
    #         messages.append(f'Test Forensic Stats failures: {forensic_stats_failures}')
    #     failures += forensic_stats_failures

    if do_gets:
        gets_failures = test_gets(engine)
        if gets_failures:
            messages.append(f'Test Gets failures: {gets_failures}')
        failures += gets_failures

    if do_liveflow:
        liveflow_failures = test_liveflow(engine, options)
        if liveflow_failures:
            messages.append(f'Test Liveflow failures: {liveflow_failures}')
        failures += liveflow_failures

    if do_miscellaneous:
        miscellaneous_failures = test_miscellaneous(engine)
        if miscellaneous_failures:
            messages.append(f'Test Miscellaneous failures: {miscellaneous_failures}')
        failures += miscellaneous_failures

    if do_packets:
        packets_failures = test_packets(engine, capture_name, 1000)
        if packets_failures:
            messages.append(f'Test Packets failures: {packets_failures}')
        failures += packets_failures

    if do_remote_engine:
        remote_engine_failures = test_remote_engine(engine)
        if remote_engine_failures:
            messages.append(f'Test Remote Engine failures: {remote_engine_failures}')
        failures += remote_engine_failures

    # if do_reports:
    #     reports_failures = test_reports(engine, report_name, report_file, report_count)
    #     if reports_failures:
    #         messages.append(f'Test Reports failures: {reports_failures}')
    #     failures += reports_failures

    # if do_select_related:
    #     select_related_failures = test_select_related(engine, fortworth_capture)
    #     if select_related_failures:
    #         messages.append(f'Test Select Related failures: {select_related_failures}')
    #     failures += select_related_failures

    # if do_wireless:
    #     wireless_failures = test_wireless(engine)
    #     if wireless_failures:
    #         messages.append(f'Test Wireless failures: {wireless_failures}')
    #     failures += wireless_failures

    # if do_legacy_connection:
    #     legacy_connection_failures = test_legacy_connection(omni, opt)
    #     if legacy_connection_failures:
    #         messages.append(f'Test Legacy Connection failures: {legacy_connection_failures}')
    #     failures += legacy_connection_failures

    # if do_tcpdump_adapter:
    #     tcpdump_failures = test_tcpdump_adapter(engine)
    #     if tcpdump_failures:
    #         messages.append(f'Test TCPDump failures: {tcpdump_failures}')
    #     failures += tcpdump_failures

    # if do_lauren_test:
    #     test_lauren_test(engine)

    if bPerformance_Logging:
        engine.stop_performance_logging()

    if do_restart:
        restart_failures = test_restart(engine)
        if restart_failures:
            messages.append(f'Test Restart failures: {restart_failures}')
        failures += restart_failures
    else:
        engine.disconnect()
        ic = engine.is_connected()
        if ic:
            omni.error('*** Failed to disconnected from the engine.')
            print('*** Failed to disconnected from the engine.')

    if failures == 0:
        omni.info('Success, no failures.')
    else:
        omni.error(f'Failed, {failures} failures.')
        for msg in messages:
            omni.error(msg)
            print(msg)

    print()
    omni.info('PyTest: Done')
    print('PyTest: Done')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        ceg_gamma = ['-h', 'ceg-gamma', '-u', 'gary']
        ceg_delta = ['-h', 'ceg-delta', '-u', 'gary']
        lw_24_2 = ['-h', 'lw-24.2', '-u', 'admin']

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%I:%M:%S%p")
        if not os.path.isdir('output'):
            os.mkdir('output')
        with open(f'output/PyTest-{timestamp}.txt', 'w') as redirect:
            with redirect_stdout(redirect):
                main(ceg_gamma)
