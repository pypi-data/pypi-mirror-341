import os
import sys
import time
import datetime
import logging
import getopt
import keyring
import paramiko
import socket
import omniscript
import FBI_Test_Reporter
import wildpackets_autoresult
import capture_results as cr
# import Insight_wrapper as iw

# server types
DELL_R640 = 0
DELL_7060 = 1
EDGE_7525D = 2
EDGE_1510D = 3
VM_LARGE = 4
LC_1100 = 5
LC_3100 = 6

SERVER_LABEL = [
    'Dell PowerEdge 640 Server',
    'Dell Optiplex 7060 Desktop',
    'Edge 7525D',
    'Edge 1510D',
    'VM Large',
    'LiveCapture 1100',
    'LiveCapture 3100'
]

INCREASE_RATE = 25  # 75 #100 11.3.0.11
DECREASE_RATE = 15  # 50 #75 #50

REPLAY_HOST = '10.8.102.34'
REPLAY_USER = 'root'
REPLAY_PASSWORD = None  # 'wildpackets'
REPLAY_ADAPTER = 'ntxc2 -c 0x01'

VERSION = '1.3.0.0'


def get_password(host, user):
    try:
        ip = [str(i[4][0]) for i in socket.getaddrinfo(host, 443)][0]
    except Exception:
        ip = host
    return keyring.get_password(ip, user)


class Options(object):
    def __init__(self, args):
        self.address = ''
        self.capture_count = 0
        self.duration = 0
        self.slow_count = 0
        self.adapter = ''
        self.host = ''
        self.user = ''
        self.password = None
        self.replay_host = REPLAY_HOST
        self.replay_user = REPLAY_USER
        self.replay_password = REPLAY_PASSWORD
        self.replay_adapter = REPLAY_ADAPTER
        self.replay_file = ''
        self.version = False
        self.help = False
        self.parse(args)

    def _dump(self):
        dummy_password = '******'
        print(f'        Address: {self.address}')
        print(f'  Capture Count: {self.capture_count}')
        print(f'       Duration: {self.duration}')
        print(f'     Slow Count: {self.slow_count}')
        print(f'        Adapter: {self.adapter}')
        print(f'           Host: {self.host}')
        print(f'      User Name: {self.user}')
        print(f'       Password: {dummy_password}')
        print(f'    Replay Host: {self.replay_host}')
        print(f'    Replay User: {self.replay_user}')
        print(f'Replay Password: {dummy_password}')
        print(f' Replay Adapter: {self.replay_adapter}')
        print(f'    Replay File: {self.replay_file}')
        print(f'        Version: {self.version}')
        print(f'           Help: {self.help}')

    def display_help(self):
        print('CapturePerf.py')
        print('  [-a <address>]   : Starting IP Address.')
        print('  [-c <count>]     : Number of captures.')
        print('  [-d <seconds>]   : Duration in seconds.')
        print('  [-s <count>]     : Number of slow captures.')
        print('  [-e <adapter>]   : Ethernet adapter.')
        print('  [-h <host>]      : Host name.')
        print('  [-u <username>]  : User account name.')
        print('  [-p <password>]  : User account password. Omit to look-up in keyring.')
        print('  [-H <replay>]    : Replay host name.')
        print('  [-U <username>]  : Replay user account name.')
        print('  [-P <password>]  : Replay user account password. Omit to look-up in keyring.')
        print('  [-E <adapter>]   : Replay adapter.')
        print('  [-t <tracefile>] : File to replay.')
        print('  [-v]             : Display the version.')
        print('  [-?]             : Print help.')

    def parse(self, args):
        try:
            (_opts, _args) = getopt.getopt(args, 'a:c:d:e:h:p:r:s:t:u:H:U:P:E:v?')
        except getopt.GetoptError:
            self.display_help()
            sys.exit(2)

        for opt, arg in _opts:
            t_arg = arg.strip()
            if opt in ('-a'):
                self.address = t_arg
            elif opt in ('-c'):
                self.capture_count = int(t_arg)
            elif opt in ('-d'):
                self.duration = int(t_arg)
            elif opt in ('-s'):
                self.slow_count = int(t_arg)
            elif opt in ('-e'):
                self.adapter = t_arg
            elif opt in ('-h'):
                self.host = t_arg
            elif opt in ('-u'):
                self.user = t_arg
            elif opt in ('-p'):
                self.password = t_arg
            elif opt in ('-H'):
                self.replay_host = t_arg
            elif opt in ('-U'):
                self.replay_user = t_arg
            elif opt in ('-P'):
                self.replay_password = t_arg
            elif opt in ('-E'):
                self.replay_adapter = t_arg
            elif opt in ('-t'):
                self.replayfile = t_arg
                # print(f'tracefile: {self.replay_file}')
            elif opt in ('-v'):
                self.version = True
            elif opt in ('-?'):
                self.help = True
            else:
                print('Unkown argument: %s', opt)
                self.help = True

    def start(self):
        if self.version:
            print('Version: %s' % (VERSION))
        if self.password is None:
            self.password = get_password(self.host, self.user)
        if self.replay_password is None:
            self.replay_password = get_password(self.replay_host, self.replay_user)
        if self.help:
            self.display_help()
            sys.exit(2)


class Test(object):
    # IMPORTANT: self.port must be updated to match the number of captures
    def __init__(self, engine, options):
        self.engine = engine
        self.captures = []
        self.kill_adapter = 'adapter 2'
        print(f'tracefile: {options.replay_file}')
        self.adapter = options.adapter
        self.ports = options.capture_count
        # Dell 640 40 Capture + slow filter = 750 & single capture = 1700
        # (Dell OPtiplex 7060 desktop single capture = 1355)
        self.change_rate = 1715
        self.test_count = 1
        self.pass_flag = 0
        self.passed_rates = []
        self.passed_replay_Mbps = []
        self.passed_replay_rate = []
        self.passed_duration = []
        self.passed_fps = []
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.load_system_host_keys()
        self.ssh.connect(options.replay_host, 22, options.replay_user, options.replay_password)
        print('PASSED REPLAY CONNECTION')
        time.sleep(5)
        self.version = self.engine.get_status().product_version
        print(f'VERSION: {self.version}')

        path = r'\\pandora\\archive\Performance_Results\{0}'.format('FBI'+self.version)
        if not os.path.exists(path):
            os.makedirs(path)

        self.dbase_results = r'\\pandora\archive\Performance_Results\{0}\{1}_{2}.txt'.format(
            'FBI' + self.version, 'FBI_filter_results',
            datetime.datetime.now().strftime('%Y_%m_%d_%I_%M_%S_%p'))
        self.LOG_FILE = r'\\pandora\archive\Performance_Results\{0}\{1}_{2}.txt'.format(
            'FBI'+self.version, 'FBI_MThread_Test',
            datetime.datetime.now().strftime('%Y_%m_%d_%I_%M_%S_%p'))
        self.FORMAT = '%(message)s'

        # create console logger (write to file only comment out adhandler(ch))
        self.log = logging.getLogger('monitor')
        if not self.log.handlers:
            self.log.setLevel(logging.INFO)
            formatter = logging.Formatter(self.FORMAT)
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(formatter)
            fh = logging.FileHandler(self.LOG_FILE)
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            self.log.addHandler(ch)
            self.log.addHandler(fh)

    def final_notes_report(self):
        # Writes final results to a file, then reads in the data and assings the string/resutls
        # to self.notes variable.
        with open(self.dbase_results, 'w+') as results:
            # results.write('System Under Test: {0}\n'.format('Dell PowerEdge 640'))
            results.write('FINAL TEST RESULTS:\n')
            results.write('REPLAY RATE:{0}  Mbps\n'.format(self.f_replay_rate))
            results.write('REPLAY REPORTED RATE:{0} Mbps\n'.format(self.f_replay_Mbps))
            results.write('CONVERSION RATE:{0}\n'.format(self.f_conversion_rate))
            results.write('DURATION:{0}\n'.format(self.f_duration))
            results.write('FPS:{0}\n'.format(self.f_fps))
            results.write('TRACE-FILE:{0}\n\n'.format('smtp_64byte.pcap'))
            results.flush()
            time.sleep(2)
            with open(self.dbase_results, 'r') as myfile:
                self.note = myfile.read()
                print('PRINTING NOTES FILE:' + self.note)
            self.ssh.close()
        return

    def setup_captures(self, options):
        starting_addr = omniscript.omniaddress.parse_ip_address(options.address)
        decimal_value = int(starting_addr.address, 16)
        self.captures = []
        for i in range(options.capture_count):
            ip_addr = omniscript.omniaddress.parse_ip_address(decimal_value)
            slow = (i < options.slow_count)
            capt = self.create_capture(options.adapter, ip_addr, slow)
            self.captures.append(capt)
            print(capt)
            decimal_value += 1

    def start_captures(self):
        self.engine.start_capture(self.captures)

    def stop_captures(self):
        self.engine.stop_capture(self.captures)

    def replay_capture_count(self, options):
        print(f'replay rate: {self.change_rate}')
        time.sleep(10)
        self.log.info(f'Replay Bit Rate:{self.change_rate} Mbps')
        stdin, stdout, stderr = self.ssh.exec_command(
            f'/opt/napatech/bin/Replay_WP3 -i {self.replay_adap} -r {self.change_rate} -txs 600 '
            f'-f /var/lib/omni/data/{self.tracefile} > /tmp/output2.txt &')
        stdin.close()
        time.sleep(60)
        if stderr.read():
            print('replay error')
            sys.exit()

        while True:
            time.sleep(5)
            stdin, stdout, stderr = self.ssh.exec_command('pidof Replay_WP3', timeout=10)
            stdin.close()
            ID_output = stdout.read()
            if ID_output == '':
                self.log.info('PIDOF Replay_WP3 is not present')
                time.sleep(5)
                self.stop_captures()
                cap_pkt, pkts_flt, percent_flt, a_cap_dropped = cr.getPackets_ftl(self.engine)
                break
            else:
                time.sleep(5)
                self.log.info(f'PID is present ID:{ID_output}\n')
                cap_pkt, pkts_flt, percent_flt, a_cap_dropped = cr.getPackets_ftl(self.engine)
                time.sleep(1)
                self.log.info(f'Packets Dropped:{a_cap_dropped}\n')
                self.log.info('Pass Flag is set to:{self.pass_flag}\n')
                if int(cap_pkt) == 0:
                    self.log.info('Packets are NOT being captured - Exiting the TEST!')
                    self.log.info('Killing Replay - TestError will try again!')
                    cr.kill_replay_feeds(options.replay_host, self.kill_adapter)
                    # raise TestError

                elif int(a_cap_dropped) > 0:
                    self.log.info(f'Packets Dropped:{a_cap_dropped}\n')
                    self.log.info('Killing Replay Feeds\n\n')
                    time.sleep(3)
                    cr.kill_replay_feeds(self.replay_host, self.kill_adapter)
            time.sleep(20)

        if int(a_cap_dropped) > 0 and self.pass_flag == 1:
            print('IN DROPPED PACKETS or Overrun > 0 PASS FLAG = 1\n')
            self.log.info(f'Dropped packets:{a_cap_dropped}\n')
            self.log.info(f'Pass Flag is set to:{self.pass_flag}\n')
            # MUST subtract 1 from Test Count so the results log receives the correct
            # passed test value for the last passed test.
            self.test_count -= 1
            self.f_replay_rate = cr.replay_rate(self.passed_replay_rate)
            self.f_replay_Mbps = cr.replay_Mbps(self.passed_replay_Mbps)
            self.f_conversion_rate = cr.final_rate(self.passed_rates)
            self.f_duration = cr.final_duration(self.passed_duration)
            self.f_fps = cr.finalfps(self.passed_fps)
            self.log.info(f'FINAL TEST: {self.test_count} PASSED!')
            self.log.info(f'PASSED REPLAY REQUESTED BIT RATE: {self.f_replay_rate} Mbps')
            self.log.info(f'PASSED REPLAY RATE CALCUATION: {self.f_replay_Mbps}')
            self.log.info(f'FINAL PASSED BIT RATE: {self.f_conversion_rate} Mbps')
            self.log.info(f'FINAL TEST DURATION: {self.f_duration}')
            self.log.info(f'FINAL FPS: {self.f_fps} sec\n')
            self.log.info('Exiting Test. Done!')
            # # Results Database log info # # # #
            self.log.info('Write to Database NOTES File Next!')
            self.final_notes_report()
            return

        elif int(a_cap_dropped) > 0 and self.pass_flag < 1:
            self.log.info(f'Test:{self.test_count} Failed!\n')
            self.change_rate -= DECREASE_RATE
            self.test_count += 1
            self.log.info(f'New Decreased Bit rate:{self.change_rate} Mbps\n\n')
            self.start_captures()
            time.sleep(10)
            self.replay_capture_count(options)

        else:  # PASSED CONDITION
            print('Leading into pass condition\n')
            packets_tx, seconds_tx, fps, replayMbps, Mbits_rate = cr.get_replay_counts_fbi(
                self.replay_host, self.ports)
            time.sleep(5)
            self.log.info(f'Packets Captured: {cap_pkt}\n')
            self.log.info(f'Packets Transmit: {packets_tx}\n')
            self.log.info(f'Replay Mbits Rate: {replayMbps}\n')
            self.log.info(f'Packets Filtered: {pkts_flt}\n')
            self.log.info(f'FPS:{fps} sec\n\n')

            if int(cap_pkt) == int(packets_tx) and int(percent_flt) >= 99:
                self.passed_replay_Mbps.append(replayMbps)
                self.passed_rates.append(Mbits_rate)
                self.passed_duration.append(int(seconds_tx))
                self.passed_fps.append(int(fps))
                self.passed_replay_rate.append(int(self.change_rate))
                self.log.info(f'Test:{self.test_count} Passed!\n')
                self.log.info(f'Passed Replay Requested Bit Rate: {self.change_rate} Mbps')
                self.log.info(f'Passed Bit rate:{Mbits_rate} Mbps')
                self.log.info(f'Passed Replay rate calculation: {replayMbps}')
                self.log.info(f'FPS:{fps} sec\n')
                self.change_rate += INCREASE_RATE
                self.pass_flag = 1
                self.test_count += 1
                self.log.info(f'Increased Bit Rate:{self.change_rate} Mbps\n\n')
                self.start_captures()
                time.sleep(5)
                self.replay_capture_count(options)

            elif ((int(cap_pkt) != int(packets_tx))
                    and (int(percent_flt) != 99)
                    and (self.pass_flag == 1)):
                self.log.info('Exiting Test - Counts Fail to match AND Filter does not = 99 '
                              'AND Pass Flag = 1! CHECK YOUR ENGINE')
                self.log.info('Final Results from last PASSED Test:\n')
                # MUST subtract 1 from Test Count so the results log receives the correct
                # passed test value for the last passed test.
                self.test_count -= 1
                self.f_replay_rate = cr.replay_rate(self.passed_replay_rate)
                self.f_replay_Mbps = cr.replay_Mbps(self.passed_replay_Mbps)
                self.f_conversion_rate = cr.final_rate(self.passed_rates)
                self.f_duration = cr.final_duration(self.passed_duration)
                self.f_fps = cr.finalfps(self.passed_fps)
                self.log.info(f'FINAL TEST: {self.test_count} PASSED!')
                self.log.info(f'PASSED REPLAY BIT RATE: {self.f_replay_rate} Mbps')
                self.log.info(f'PASSED BIT RATE: {self.f_conversion_rate}')
                self.log.info(f'FPS: {self.f_fps} sec\n')
                self.log.info('Exiting Test. Done!')
                self.log.info('Write to Database NOTES File Next!')
                self.final_notes_report()
                return

            elif (int(cap_pkt) != int(packets_tx)
                  and int(a_cap_dropped == 0)
                  and (self.pass_flag == 1)):
                self.log.info('Exiting Test - COUNTS FAIL with NO Dropped packets '
                              'AND PASS FlAG = 1! CHECK YOUR ENGINE\n')
                self.log.info(f'Packets Transmit: {packets_tx}\n')
                self.log.info(f'Packets Captured: {cap_pkt}\n')

                self.log.info('Final Results from last PASSED Test:\n')
                # MUST subtract 1 from Test Count so the results log receives the correct
                # passed test value for the last passed test.
                self.test_count -= 1
                self.f_replay_rate = cr.replay_rate(self.passed_replay_rate)
                self.f_replay_Mbps = cr.replay_Mbps(self.passed_replay_Mbps)
                self.f_conversion_rate = cr.final_rate(self.passed_rates)
                self.f_duration = cr.final_duration(self.passed_duration)
                self.f_fps = cr.finalfps(self.passed_fps)
                self.log.info(f'FINAL TEST: {self.test_count} PASSED!')
                self.log.info(f'PASSED REPLAY BIT RATE: {self.f_replay_rate} Mbps')
                self.log.info(f'PASSED BIT RATE: {self.f_conversion_rate}')
                self.log.info(f'FPS: {self.f_fps} sec\n')
                self.log.info('Exiting Test. Done!\n')
                # # Results Database log info # # # # #
                self.log.info('Write to Database NOTES File Next!\n')
                self.final_notes_report()
                sys.exit(0)

            # added missing packet:

            elif (int(cap_pkt) != int(packets_tx)
                  and int(a_cap_dropped == 0)
                  and (self.pass_flag != 1)):
                self.log.info('MISSING PACKETS! Pass Flag IS NOT SET!\n')
                self.change_rate -= DECREASE_RATE
                self.test_count += 1
                self.log.info(f'New Decreased Bit rate:{self.change_rate} Mbps\n\n')
                self.start_captures()
                time.sleep(5)
                self.replay_capture_count(options)
            else:
                print('Replay text file is empty - OR NO CONDITIONS PASS\n')
                print('EXITING SCRIPT, CHECK ENGINE AND STATS, EXITING TEST\note')
                sys.exit(0)

    def create_ip_filter(self, name, ip_addr):
        # Delete existing filter.
        _filter = self.engine.find_filter(name)
        self.engine.delete_filter(_filter)

        ip_filter = omniscript.Filter(name)
        addr_node = omniscript.AddressNode()
        addr_node.address_1 = omniscript.IPv4Address(str(ip_addr))
        addr_node.accept_1_to_2 = True
        addr_node.accept_2_to_1 = True
        ip_filter.criteria = addr_node
        return ip_filter

    def create_slow_filter(self, name, ip_addr):
        addr_node = omniscript.AddressNode()
        addr_node.address_1 = omniscript.IPv4Address(str(ip_addr))
        addr_node.accept_1_to_2 = True
        addr_node.accept_2_to_1 = True

        patterns = [
            '616C616B6A666861667C6173646A6B68666C61667C646A6B68676B6C6864677C616B6A67686B737C6B7'
            '368676B61686C677C6B68676B6861677C6B68676B6168677C676C686C67686761736C677C646C676B6A'
            '616C676A7C626C6A6C6A64677C6C616A676C616A676C20',
            '616C6A656F747565726765726A656A676F6764656C6A2E20313232',
            '616C616B6A666861667C6173646A6B68666C61667C646A6B68676B6C6864677C616B6A67686B737C6B7'
            '368676B61686C677C6B68676B6861677C6B68676B6168677C676C686C67686761736C677C646C676B6A'
            '616C676A7C626C6A6C6A64677C6C616A676C616A676C20',
            '5D297B302C317D5B302D395D295C2E297B332C337D2832355B302D355D7C28325B302D345D7C317B302'
            'C317D5B302D395D297B302C317D5B302D395D297C285B302D39612D66412D465D7B312C347D3A297B31'
            '2C347D3A282832355B302D355D7C28325B302D345D7C317B302C317D5B302D395D297B302C317D5B302'
            'D395D295C2E297B332C337D2832355B302D355D7C28325B302D345D7C317B302C317D5B302D395D297B'
            '302C317D5B302D395D2929',
            '5D297B302C317D5B302D395D295C2E297B332C337D2832355B302D355D7C28325B302D345D7C317B302'
            'C317D5B302D395D297B302C317D5B302D395D297C285B302D39612D66412D465D7B312C347D3A297B31'
            '2C347D3A282832355B302D355D7C28325B302D345D7C317B302C317D5B302D395D297B302C317D5B302'
            'D395D295C2E297B332C337D2832355B302D355D7C28325B302D345D7C317B302C317D5B302D395D297B'
            '302C317D5B302D395D2929',
            '616C616B6A666861667C6173646A6B68666C61667C646A6B68676B6C6864677C616B6A67686B737C6B7'
            '368676B61686C677C6B68676B6861677C6B68676B6168677C676C686C67686761736C677C646C676B6A'
            '616C676A7C626C6A6C6A64677C6C616A676C616A676C20',
            '616C6A656F747565726765726A656A676F6764656C6A2E20313232',
            '616C616B6A666861667C6173646A6B68666C61667C646A6B68676B6C6864677C616B6A67686B737C6B7'
            '368676B61686C677C6B68676B6861677C6B68676B6168677C676C686C67686761736C677C646C676B6A'
            '616C676A7C626C6A6C6A64677C6C616A676C616A676C20',
            '616C616B6A666861667C6173646A6B68666C61667C646A6B68676B6C6864677C616B6A67686B737C6B7'
            '368676B61686C677C6B68676B6861677C6B68676B6168677C676C686C67686761736C677C646C676B6A'
            '616C676A7C626C6A6C6A64677C6C616A676C616A676C20',
            '616C6A656F747565726765726A656A676F6764656C6A2E20313232',
            '5D297B302C317D5B302D395D295C2E297B332C337D2832355B302D355D7C28325B302D345D7C317B302'
            'C317D5B302D395D297B302C317D5B302D395D297C285B302D39612D66412D465D7B312C347D3A297B31'
            '2C347D3A282832355B302D355D7C28325B302D345D7C317B302C317D5B302D395D297B302C317D5B302'
            'D395D295C2E297B332C337D2832355B302D355D7C28325B302D345D7C317B302C317D5B302D395D297B'
            '302C317D5B302D395D2929',
            '616C616B6A666861667C6173646A6B68666C61667C646A6B68676B6C6864677C616B6A67686B737C6B7'
            '368676B61686C677C6B68676B6861677C6B68676B6168677C676C686C67686761736C677C646C676B6A'
            '616C676A7C626C6A6C6A64677C6C616A676C616A676C20',
            '5D297B302C317D5B302D395D295C2E297B332C337D2832355B302D355D7C28325B302D345D7C317B302'
            'C317D5B302D395D297B302C317D5B302D395D297C285B302D39612D66412D465D7B312C347D3A297B31'
            '2C347D3A282832355B302D355D7C28325B302D345D7C317B302C317D5B302D395D297B302C317D5B302'
            'D395D295C2E297B332C337D2832355B302D355D7C28325B302D345D7C317B302C317D5B302D395D297B'
            '302C317D5B302D395D2929',
            '616C616B6A666861667C6173646A6B68666C61667C646A6B68676B6C6864677C616B6A67686B737C6B7'
            '368676B61686C677C6B68676B6861677C6B68676B6168677C676C686C67686761736C677C646C676B6A'
            '616C676A7C626C6A6C6A64677C6C616A676C616A676C20'
        ]

        p_nodes = []
        next_node = addr_node
        for pat in patterns:
            pn = omniscript.PatternNode()
            pn.pattern_type = omniscript.PATTERN_TYPE_REGEX
            pn.pattern = pat
            pn.start_offset = -1
            pn.end_offset = -1
            pn.case_sensitive = True
            pn.or_node = next_node
            p_nodes.append(pn)
            next_node = pn

        slow_filter = omniscript.Filter(name)
        slow_filter.criteria = p_nodes[-1]
        return slow_filter

    def create_capture(self, adapter, ip_addr, slow=False):
        name = f'Perf Capture - {ip_addr}'
        # IP Filter
        if not slow:
            ip_filter = self.create_ip_filter(name, ip_addr)
        else:
            name += ' slow'
            ip_filter = self.create_slow_filter(name, ip_addr)
        old_filter = self.engine.find_filter(name)
        self.engine.delete_filter(old_filter)
        self.engine.add_filter(ip_filter)

        ct = omniscript.CaptureTemplate()
        ct.general.name = name
        ct.general.option_continuous_capture = True
        ct.general.option_capture_to_disk = False
        ct.general.option_start_capture = True
        ct.general.buffer_size = 256 * 1048576
        ct.set_adapter(adapter)
        ct.set_all(False)
        ct.analysis.option_network = True
        ct.analysis.option_summary = True
        ct.add_filter(ip_filter)
        return self.engine.create_capture(ct)

    def delete_captures(self, captures):
        for capt in captures:
            ct = capt.get_capture_template()
            filters = ct.filter.filters
            for filter in filters:
                capt.engine.find_filters()


def main(args, server):
    print(f'SUT: {SERVER_LABEL[server]}')

    options = Options(args)
    print('PASSED options')
    # time.sleep(10)
    options.start()
    options._dump()

    omni = omniscript.OmniScript()
    engine = omni.create_engine(options.host)
    if not engine.login(options.user, options.password):
        print(f'Failed to connect to the engine: {options.host}')
        sys.exit(2)

    adapter = engine.find_adapter(options.adapter)
    if not adapter:
        print(f'Invalid adapter specified: {options.adapter}\n')
        sys.exit(1)
    print('Capture Adapter:', adapter)

    test = Test(engine, options)
    cr.init_test_env2(test.engine)
    print('calling kill_replay_feeds')
    # cr.kill_replay_feeds(options.replay_host,test.kill_adapter)
    test.setup_captures(options)
    time.sleep(2)
    test.replay_capture_count(options)
    script_name = 'FBI_MThread_Filter_Test_Capture_Count_'
    autoresults_dict = {}
    dbresults = FBI_Test_Reporter.TestReporter(options.host, test.dbase_results)
    autoresults_dict = dbresults.HardWareInfo()
    autoresults_dict.update({
        'TEST_TYPE': 'cpt',
        'DESCR': 'Performance on Intel based adapters',
        'CONTACT': 'Candace',
        'DATE': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

    print(f'SUT: {SERVER_LABEL[server]}')
    if server == DELL_R640:
        autoresults_dict.update({
            'SCRIPT': str(script_name) + str(test.ports),
            'TRACE_FILE': 'smtp_64byte.pcap',
            'FRAME_SIZE': '64',
            'ENGINE_PLATFORM': 'Dell PowerEdge 640'
        })
        autoresults_dict.update({
            'ADAPTER_NAME': 'INTEL X710 10Gb SFP',
            'TEST_RUN_DURATION': test.f_duration,
            'TOP_BIT_RATE': '{0}'.format(test.f_conversion_rate),
            'NOTE': test.note,
            'FPS': test.f_fps,
            'LOG': test.LOG_FILE
        })
    else:
        autoresults_dict.update({
            'SCRIPT': str(script_name) + str(test.ports),
            'TRACE_FILE': 'smtp_64byte.pcap',
            'FRAME_SIZE': '64',
            'ENGINE_PLATFORM': 'Dell Optiplex 7060',
            'ENGINE_CPU': 'Intel(R) Core(TM) i7-8700 CPU @ 3.20GHz Core Count: 12'
        })
        autoresults_dict.update({
            'ADAPTER_NAME': 'INTEL X550T 10G Copper',
            'TEST_RUN_DURATION': test.f_duration,
            'TOP_BIT_RATE': '{0}'.format(test.f_conversion_rate),
            'NOTE': test.note,
            'FPS': test.f_fps,
            'LOG': test.LOG_FILE
        })

    autoresult = wildpackets_autoresult.AUTORESULT()
    autoresult.connect_db()
    results = autoresult.insert_results(autoresults_dict)
    print(results)
    sys.exit(0)


# ----------------------------------------------------------------------------
if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1:], DELL_R640)
    else:
        # , '-t smtp_64byte.pcap']
        args1 = [
            '-a 192.0.0.1',
            '-c 10',
            '-e ens1f0',
            '-h 10.8.100.3',
            '-u root',
            '-t smtp_64byte.pcap'
        ]

        # eno2np1 = broadcom 10G
        args2 = [
            '-a 192.0.0.1',
            '-c 1',
            '-e ens1f0',
            '-h 10.8.100.3',
            '-u root',
            '-t smtp_64byte.pcap'
        ]

        # (CHANGE -c to 40! '-s 1') 10.4.2.87 linux eno3  smb eno2   SLOT 8 Port 4
        args3 = [
            '-a 192.0.0.1',
            '-c 40',
            '-e ens1f0',
            '-h 10.8.100.3',
            '-u root',
            '-s 1',
            '-t smtp_64-byte-fix.pcap']

        args4 = [
            '-a 192.0.0.1',
            '-c 1',
            '-e eth2',
            '-h 10.8.100.24',
            '-u root'  # eno2np1 = broadcom 10G
        ]

        args5 = [
            '-a 192.0.0.1',
            '-c 1',
            '-e eno1',
            '-h gary-dt2',
            '-u gary',
            '-H edge-2',
            '-U admin',
            '-E eth2'
        ]

        # IMPORTANT: Set the 'server' value to DELL_R640 or DELL_7060
        main(args5, server=DELL_7060)
