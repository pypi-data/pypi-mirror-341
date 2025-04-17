import os
import sys
import time
import omniscript
import paramiko
import re
import logging
# from elasticsearch import (
#     Elasticsearch, ImproperlyConfigured, ElasticsearchException, ConflictError)

OS_WINDOWS = 0
OS_LINUX = 1
if sys.platform == 'linux':
    host_os = OS_LINUX
else:
    host_os = OS_WINDOWS

# This function requires the user to pass the 'host address' & replay to write the output to
# a 'output.txt' file in the /tmp directory.
# Example command/use case: '/opt/napatech/bin/Replay_WP_ves -i %s  -r %s -txs 30
#                            -f /opt/napatech/bin/%s > /tmp/output.txt &' % (self.replay_adap,
#                            self.change_rate, self.tracefile))
# The function will return the number of pkts replay sent:
#     (packets_tx), duration (seconds_tx), fps (fps), and rate (Mbits_rate)
# create console logger (write to file only comment out adhandler(ch))

LOG_FILE = 'C:\\tmp\\Capture_results.txt' if host_os == OS_WINDOWS else '/tmp/Capture_results.txt'

FORMAT = '%(message)s'
log = logging.getLogger('results_monitor')
if not log.handlers:
    log.setLevel(logging.INFO)
    formatter = logging.Formatter(FORMAT)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    fh = logging.FileHandler(LOG_FILE)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(ch)
    log.addHandler(fh)


# Writes final results to a file, then reads in the data and assings the string/resutls
# to self.notes variable.
def final_notes_report(dbase_results, platform, adap, f_replay_rate, f_conversion_rate, f_fps,
                       f_duration, tracefile):
    with open(dbase_results, 'w+') as results:
        results.write('System Under Test: {0}\n'.format(platform))
        results.write('Adapters Under Test: {0}\n'.format(adap))
        results.write('FINAL TEST RESULTS:\n')
        results.write('Bit RATE:{0}  Mbps\n'.format(f_replay_rate))
        results.write('CONVERSION RATE:{0} Mbps\n'.format(f_conversion_rate))
        results.write('FPS:{0}\n'.format(f_fps))
        results.write('DURATION:{0}\n'.format(f_duration))
        results.write('TRACE-FILE:{0}\n\n'.format(tracefile))
        results.flush()
        time.sleep(2)
        with open(dbase_results, 'r') as myfile:
            note = myfile.read()
            print(note)
        return note
    return


# def tools(self):
#     for x,y in zip(tests, filters):
#         print(x, y)


def create_capture_test(engine, template_name, test_name, adap, disk_reserve):
    filesize = 1024
    template = omniscript.CaptureTemplate(template_name)
    template.general.name = test_name
    template.adapter.name = adap
    template.general.max_total_file_size = disk_reserve * (1024 * 1024 * 1024)
    time.sleep(2)
    # converts files size from MB to Bytes
    template.general.file_size = filesize * (1024 * 1024)
    template.general.option_keep_last_files = True
    # Calculate 'keep_last_files_count':
    template.general.keep_last_files_count = (template.general.max_total_file_size
                                              / template.general.file_size)
    print('keep last file count:', template.general.keep_last_files_count)
    capture = engine.create_capture(template)
    print(capture)


def disk_reserve(host, size):
    # Gets the available disk size value either returns 50% or 100%
    # of the size for the capture template
    print('Getting disk partition info')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, 22, 'root', 'Spider8fly!')
    stdin, stdout, stderr = ssh.exec_command(
        'df -BG --output=avail /var/lib/omni/data | grep -vi avail')
    stdin.close()
    disk_size = int(str(stdout.read()).strip('G\n'))
    if (disk_size) > 0:
        if size == 50:
            reserve_size = (int(50 * int(disk_size) / 100))
            print('Disk reserve value' + reserve_size)
        elif size == 75:
            reserve_size = (int(75 * int(disk_size) / 100))
            print('Disk reserve value' + reserve_size)
        elif size == 100:
            reserve_size = (int(100 * int(disk_size) / 100))
            print('Disk reserve value', reserve_size)
    return (disk_size, reserve_size)


def config_test(host, template_name, test_name, reserve_size):
    omni = omniscript.OmniScript()
    engine = omni.create_engine(host)
    engine.login('root', 'Spider8fly!')
    version = engine.get_status().product_version
    assert version
    template = omniscript.CaptureTemplate(template_name)
    template.general.name = test_name
    template.general.max_total_file_size = reserve_size
    capture = engine.create_capture(template)
    assert capture


# Comment out: y is not defined and reconnect is never called.
# Restart engine for replaced files to take effect:
# def reconnect(eng_obj):
# 		engine = eng_obj
# 		engine.restart()
# 		time.sleep(10)
# 		engine.login(y['eng_user'], y['eng_pwd'])
# 		maxwait = time.time() + 30 #30 seconds max wait
# 		while not engine.is_connected():
# 			engine.login(y['eng_user'], y['eng_pwd'])
# 			time.sleep(1)
# 			if time.time > maxwait:
# 				logging.info('Engine did not restart after 30 seconds')
# 				break
# 		logging.info('Restarted engine for replaced files to take effect')

def get_trex_stats(ports):
    print('Getting T-rex Stats!')
    host = '10.8.102.5'
    ports = ports
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, 22, 'root', 'wildpackets')
    stdin, stdout, stderr = ssh.exec_command('ls /tmp/')
    stdin.close()
    ls_ouput = stdout.read()
    print(ls_ouput)
    if len(ls_ouput) >= 2:
        stdin, stdout, stderr = ssh.exec_command('cat /tmp/output1.txt')
        stdin.close()
        output1 = stdout.read()
        stdin, stdout, stderr = ssh.exec_command('cat /tmp/output2.txt')
        stdin.close()
        output2 = stdout.read()
        myregex0 = re.compile(r'Expected-BPS\s+:\s+([0-9]+\.[0-9]+)[\s\S]*Active-flows\s+'
                              r':\s+([0-9]+)[\s\S]*Total-tx-pkt\s+:\s+([0-9]+)')
        stat_output1 = myregex0.search(output1)
        stat_output2 = myregex0.search(output2)
        if stat_output1 and stat_output2:
            Gbps_1 = (stat_output1.group(1))
            flows_1 = (stat_output1.group(2))
            pkts_1 = (stat_output1.group(3))
            Gbps_2 = (stat_output2.group(1))
            flows_2 = (stat_output2.group(2))
            pkts_2 = (stat_output2.group(3))
            Gbps = float(Gbps_1) + float(Gbps_2)
            tx_pkts = (int(pkts_1) + int(pkts_2))
            flows = (int(flows_1) + int(flows_2))
            print(Gbps)
            print(tx_pkts)
            print(flows)
            return Gbps, flows, tx_pkts
        if len(ls_ouput) == 1:
            myregex0 = re.compile(r'Expected-BPS\s+:\s+([0-9]+\.[0-9]+)[\s\S]*Active-flows\s'
                                  r'+:\s+([0-9]+)[\s\S]*Total-tx-pkt\s+:\s+([0-9]+)')
            stat_output1 = myregex0.search(output1)
            Gbps = (stat_output1.group(1))
            flows = (stat_output1.group(2))
            tx_pkts = (stat_output1.group(3))
            return Gbps, flows, tx_pkts
        else:
            print('no match')
    ssh.close()
    return


def get_replay_counts(host, ports):
    # this function gets the replay tx stats and multiplies it by the port values.
    # The port value is defined in the SUT file. This is used for 1 Gig 4 port captures via APCON.
    # Replay only provides stats for what it sends. Therefore if replay is connected in
    # to the APCON that mirrors out 4 ports, we need to have a port multiplier.
    print('IN GET REPLAY COUNTS')
    ports = ports
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, 22, 'root', 'wildpackets')
    stdin, stdout, stderr = ssh.exec_command('cat /tmp/output.txt')
    stdin.close()
    output = stdout.read()
    myregex = re.compile(r'Total\s+packets\s+Transmitted:\s+([0-9]+)\nTotal\s+bytes\s+Transmitted:'
                         r'\s+([0-9]+)\nTotal\s+seconds\s+spent\s+transmitting:\s+([0-9]+)')
    regex_output = myregex.search(output)
    if regex_output:
        packets_tx = (int(regex_output.group(1)) * int(ports))
        print('port count:',  ports)
        print('packets tx AFTER PORT multiplier:', packets_tx)
        bytes_tx = (int(regex_output.group(2)) * int(ports))  # 2 original
        seconds_tx = int(regex_output.group(3))
        print('REPLAY SECONDS TX VALUE:', seconds_tx)
        fps = int(packets_tx) / int(seconds_tx)  # original
        bytes_Bps = (int(bytes_tx) + int(packets_tx)*8) / int(seconds_tx)
        Mbits_rate = bytes_conversion(bytes_Bps)
        time.sleep(5)
        ssh.close()
        return packets_tx, seconds_tx, fps, Mbits_rate


def get_replay_counts_fbi(host, ports):
    print('IN GET REPLAY COUNTS')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, 22, 'root', 'wildpackets')
    stdin, stdout, stderr = ssh.exec_command('cat /tmp/output2.txt')
    stdin.close()
    output = stdout.read()
    regex = re.compile(r'Mbps:\s+([0-9]+)')
    regoutput = regex.search(output)
    myregex = re.compile(r'Total\s+packets\s+Transmitted:\s+([0-9]+)\nTotal\s+bytes\s+'
                         r'Transmitted:\s+([0-9]+)\nTotal\s+seconds\s+spent\s+transmitting:'
                         r'\s+([0-9]+)')
    regex_output = myregex.search(output)
    if regex_output and regoutput:
        replayMbps = regoutput.group(1)
        print('Replay Mbits output:', replayMbps)
        fps = int(regex_output.group(1)) / int((regex_output.group(3)))
        pkts_orginal = int(regex_output.group(1))
        print('original pkts:', pkts_orginal)
        packets_tx = (int(regex_output.group(1)) * int(ports))
        print('packets tx AFTER PORT multiplier:', packets_tx)
        bytes_tx = int(regex_output.group(2))
        seconds_tx = int(regex_output.group(3))
        bytes_Bps = (int(bytes_tx) + int(pkts_orginal)*8) / int(seconds_tx)
        Mbits_rate = bytes_conversion(bytes_Bps)
        time.sleep(5)
        ssh.close()
        return packets_tx, seconds_tx, fps, replayMbps, Mbits_rate


def get_tcreplay_counts(host, ports):
    print('IN GET TCPREPLAY COUNTS')
    ports = ports
    print('port count:', ports)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, 22, 'root', 'wildpackets')
    stdin, stdout, stderr = ssh.exec_command('cat /tmp/output.txt')
    stdin.close()
    output = stdout.read()
    myregex = re.compile(r'Total\s+packets\s+Transmitted:\s+([0-9]+)\nTotal\s+bytes\s'
                         r'+Transmitted:\s+([0-9]+)\nTotal\s+seconds\s+spent\s+transmitting:\s'
                         r'+([0-9]+)')
    regex_output = myregex.search(output)
    if regex_output:
        print(int(regex_output.group(1)))
        packets_tx = (int(regex_output.group(1)) * int(ports))
        print('packets tx AFTER PORT multiplier:', packets_tx)
        bytes_tx = (int(regex_output.group(2)) * int(ports))   # 2
        seconds_tx = int(regex_output.group(3))
        print('REPLAY SECONDS TX VALUE:', seconds_tx)
        fps = int(packets_tx) / int(seconds_tx)
        bytes_Bps = (int(bytes_tx) + int(packets_tx)*8) / int(seconds_tx)
        Mbits_rate = bytes_conversion(bytes_Bps)
        time.sleep(5)
        ssh.close()
        return packets_tx, seconds_tx, fps, Mbits_rate


def get_replay_counts_2(host, multiplier):
    # this function is for a capture that rx data from two separate replay feeds.
    # The Multiplier is used to calculate the
    multiplier = multiplier
    print('multiplier:', multiplier)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, 22, 'root', 'wildpackets')
    stdin, stdout, stderr = ssh.exec_command('cat /tmp/output1.txt', timeout=20)
    stdin.close()
    output1 = stdout.read()
    stdin, stdout, stderr = ssh.exec_command('cat /tmp/output2.txt', timeout=20)
    stdin.close()
    output2 = stdout.read()
    myregex = re.compile(r'Total\s+packets\s+Transmitted:\s+([0-9]+)\nTotal\s+bytes\s'
                         r'+Transmitted:\s+([0-9]+)\nTotal\s+seconds\s+spent\s+transmitting:\s'
                         r'+([0-9]+)')
    regex_output1 = myregex.search(output1)
    regex_output2 = myregex.search(output2)
    if regex_output1 and regex_output2:
        packets_tx_1 = (int(regex_output1.group(1)) * int(multiplier))  # Bridged captures
        packets_tx_2 = int(regex_output2.group(1))
        bytes_tx_1 = (int(regex_output1.group(2)) * int(multiplier))
        bytes_tx_2 = int(regex_output2.group(2))
        seconds_tx = int(regex_output1.group(3))
        fps_1 = int(packets_tx_1) / int(seconds_tx)
        fps_2 = int(packets_tx_2) / int(seconds_tx)
        bytes_Bps_1 = (int(bytes_tx_1) + int(packets_tx_1) * 8) / int(seconds_tx)
        bytes_Bps_2 = (int(bytes_tx_2) + int(packets_tx_2) * 8) / int(seconds_tx)
        Mbits_rate_1 = bytes_conversion(bytes_Bps_1)
        Mbits_rate_2 = bytes_conversion(bytes_Bps_2)
        packets_tx = int(packets_tx_1) + int(packets_tx_2)
        print('Collective 3 Capture Count:', packets_tx)
        time.sleep(2)
        ssh.close()
        return packets_tx, seconds_tx, fps_1, fps_2, Mbits_rate_1, Mbits_rate_2


def getPackets(eng_obj, flow='no'):
    # flow = no is an optional variable used for liveflow testing. if not passed in,
    # the default is no and flows dropped won't be returned
    print('getting packets\n')
    engine = eng_obj
    pkts_rx = 0
    cap_dropped = 0
    flows_dropped = 0
    for capture in engine.get_capture_list():
        capture.refresh()
        pkts_rx += capture.packets_filtered  # packets into the
        cap_dropped += capture.packets_dropped
        flows_dropped += capture.flows_dropped
        print('packets rx:', pkts_rx)
        print('packets dropped', cap_dropped)
        print('returning values to get_eng_stats function')
        if flow == 'yes':
            print('Flow Variable:', flow)
            return pkts_rx, cap_dropped, flows_dropped
        else:
            print('Flow Variable:', flow)
            return pkts_rx, cap_dropped


def getPacket_timestamp(eng_obj):
    print('in getPacketTimestamp')
    engine = eng_obj
    print(engine)
    for capture in engine.get_capture_list():
        print(capture)
        pkt_timestamp = capture.data_start_time
        pkt_end_timestamp = capture.data_stop_time
        assert pkt_end_timestamp
        return pkt_timestamp


def getPackets_ftl(eng_obj):
    print('getting packets\n')
    engine = eng_obj
    pkts_rx = 0
    pkts_flt = 0
    cap_dropped = 0
    for capture in engine.get_capture_list():
        capture.refresh()
        pkts_flt += capture.packets_filtered
        pkts_rx += capture.packets_received
        cap_dropped += capture.packets_dropped
        percent_flt = int(pkts_rx/pkts_flt)
        log.info('Packets RX:{0}'.format(pkts_rx))
        log.info('Packets filtered out:{0}'.format(pkts_flt))
        if percent_flt == 100 or percent_flt == 99:
            log.info('Percent filtered out:{0}%'.format(percent_flt))
        else:
            log.info('Percent filtered out:{0}%'.format(percent_flt))
    return pkts_rx, pkts_flt, percent_flt, cap_dropped


def replay_transmit(replay_adap, change_rate, tracefile, test_count):
    print('IN REPLAY FUNCTION\n')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect('10.8.102.34', 22, 'root', 'wildpackets')
    print('Test #:{0}'.format(test_count))
    # '-i ntxc1' make a variable self.nt_interface =
    print('Replay Bit Rate:{0} Mbps'.format(change_rate))
    stdin, stdout, stderr = ssh.exec_command('/opt/napatech/bin/Replay_WP3 -i {replay_adap} -r '
                                             f'{change_rate} -txs 30 -f '
                                             f'/opt/napatech/bin/{tracefile} > /tmp/output.txt &')
    stdin.close()
    output = stdout.read()
    assert output
    if stderr.read():
        print('replay error')
        print('disconnecting MAIN Script OS2')
        sys.exit
    stdin.close()
    stderr.close()
    stdout.close()
    ssh.close()
    return


def kill_replay_feeds(replay_host, replay_user, replay_password, kill_adapter):
    host = replay_host
    print(f'Host: {host}')
    print(f'Clearing Replay Feeds: {kill_adapter}')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, 22, replay_user, replay_password)
    stdin, stdout, stderr = ssh.exec_command('/opt/napatech/bin/KillFeeds -%s' % kill_adapter)
    stdin.close()
    stderr.close()
    stdout.close()
    ssh.close()
    return


def kill_replay_feeds_2(feed1, feed2):
    print('Clearing Replay Feeds!')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect('10.8.102.34', 22, 'root', 'wildpackets')
    # stdin, stdout, stderr = ssh.exec_command('/opt/napatech/bin/KillFeeds -adapter 1; '
    #                                          '/opt/napatech/bin/KillFeeds -adapter 2', '
    #                                          'timeout=10)
    stdin, stdout, stderr = ssh.exec_command(f'/opt/napatech/bin/KillFeeds -{feed1}; '
                                             f'/opt/napatech/bin/KillFeeds -{feed2}', timeout=10)
    stdin.close()
    output = stdout.read()
    print('Kill Feeds output' + output)
    stderr.close()
    stdout.close()
    time.sleep(5)
    return


def kill_trex_feeds():
    print('Clearing Trex feeds')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect('10.8.102.5', 22, 'root', 'wildpackets')
    stdin, stdout, _ = ssh.exec_command('ps -ef | grep ./_t-rex-64-o | grep -v grep')
    stdin.close()
    output = stdout.read()
    myregex0 = re.compile(r'root\s+([0-9]+)')
    pid_list = myregex0.findall(output)
    if pid_list:
        for pid in pid_list:
            print('trex pidid:' + pid)
            stdin, stdout, _ = ssh.exec_command('kill -9 %s' % pid)
            stdin.close()
    return


def eng_upgrade(host, version):
    LOG = open(r'C:\tmp\test.txt', 'a')
    LOG.write('Upgraded function\n\n')
    wrkdir = os.getcwd()
    print(wrkdir)
    # cmd = 'python %s -l debug -c -s -i %s %s' %(wrkdir + '\updateOEL.py', host, '9.1')
    # cmd = 'python %s -l debug -c -s -i %s %s' %(wrkdir + '\updateOEL.py', host, str(version))
    cmd = f'python {wrkdir}/updateOEL.py -l debug -c -s -i {host} {version}'
    print(cmd)
    LOG.write('past cmd varialbe\n\n')
    os.system(cmd)
    LOG.write('upgrade command called\n\n')


def drive_health(host):
    print('Drive Check')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, 22, 'root', 'Spider8fly!')
    stdin, stdout, stderr = ssh.exec_command('omnistatus -drives')
    stdin.close()
    drives = stdout.read()
    for match in re.findall(r'Reallocated_Sector_Ct\s+\d*\w\d{4}\s+\d+\s+\d+\s+\d+\s+\w+'
                            r'[a-zA-Z0-9-_]+\s+\w+\s+[a-zA-Z0-9-_]\s+(\d+)', drives):
        print(match)
        if int(match) > 0:
            print('Reallocated sectors found!\n')
            print('Bad sector count:{} - Exiting program.'.format(match))
            print('Reallocated sectors found. Exiting program!')
            sys.exit(0)
        else:
            print('Disks are healthy!')
            ssh.close()
    return


def restart_omnid(host):
    print('restart_omnid')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, 22, 'root', 'Spider8fly!')
    stdin, stdout, stderr = ssh.exec_command('service omnid restart')
    stdin.close()
    output = stdout.read()
    print(output)
    error = stderr.read()
    if error:
        print(error)
        sys.exit()
    ssh.close()
    return


def init_test_env2(engine):
    print('Initializing Test Environment')
    engine = engine
    flist = None
    print(engine)
    if engine:
        print('Checking for Captures Sessions')
        capture_list = engine.get_capture_list()
        if len(capture_list) > 0:
            print('Deleting Capture sessions & files')
            engine.delete_all_capture_sessions()
        flist = engine.get_file_list()
        pktlist = [f for f in flist if f.name[-4:] == '.npkt']
        for f in pktlist:
            print('filename' + f)
        if pktlist:
            print('packet list' + pktlist)
            engine.delete_file(pktlist)
        flist = engine.get_capture_list()
        if flist:
            for i in engine.get_capture_list():
                time.sleep(1)
                print('Deleting Capture:{0}'.format(i))
                engine.delete_capture(i)
                time.sleep(1)
                print('Captures Cleaned up!')
        else:
            print('NO Captures Present!')
    return engine


def file_cleanup(host):
    print('host:' + host)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, 22, 'root', 'Spider8fly!')
    host = host
    omni = omniscript.OmniScript()
    print('trying to connect via omniscript next')
    time.sleep(5)
    try:
        engine = omni.create_engine(host)
        engine.login('root', 'Spider8fly!')
        if not engine.is_connected():
            engine.login('root', 'spider8fly')
        if not engine.is_connected():
            print('Failed to connect with either "Spider8fly" or "spider8fly" password')
        print('past connect')
    except omniscript.omnierror.OmniError:
        print('Failed to connect with either "Spider8fly" or "spider8fly" password')
    if engine:
        print('engine object exists')
        filelist = engine.get_forensic_file_list()
        if filelist:
            print('filelist exist')
        engine.delete_file(filelist)
        time.sleep(5)
        print('syncing db')
        engine.sync_forensic_database()
        engine.disconnect()
    ssh.close()
    print('LEAVING FILE CLEANUP FUNCTION!\n\n')
    return


def delete_anyfile(host):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, 22, 'root', 'Spider8fly!')
    stdin, stdout, _ = ssh.exec_command('ls -l /var/lib/omni/data/ > /var/lib/omni/data/test.txt')
    stdin.close()
    stdin, stdout, _ = ssh.exec_command('cat /var/lib/omni/data/test.txt')
    output = stdout.read()
    myregex = re.compile(r'([0-9]+\.G)')
    myfile = myregex.search(output)
    print('file found:', myfile)
    if myfile:
        print('Deleting fallocate file:' + myfile.group(0))
        stdin, stdout, _ = ssh.exec_command(f'rm /var/lib/omni/data/{myfile.group(0)}')
        stdin.close()
    return


def get_disk_info(host):
    print('Getting disk partition info')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, 22, 'root', 'Spider8fly!')
    stdin, stdout, stderr = ssh.exec_command('echo "$(date),$(df -BG --output=used "'
                                             '"/var/lib/omni/data | grep -vi used)" | "'
                                             '"tee -a output9')
    # stdin, stdout, stderr = ssh.exec_command('echo "$(date),$(df -ah --output=used "
    #                               "/var/lib/omni/data | grep -vi used)" | tee -a output9')
    stdin.close()
    disk_output = stdout.read()
    print(disk_output)
    # ssh.close()
    return disk_output


def update_filters(eng, filter_file):
    print('Importing Filter file')
    myfilterlist = omniscript.read_filter_file(filter_file)
    eng.add_filter(myfilterlist)
    print('Done!')
    return


def passed_rates(TEST_1_RATE, TEST_2_RATE):
    print('In passed_rates function')
    print(TEST_1_RATE)
    print(TEST_2_RATE)
    passed_rates = {
        'TEST_1_RATE': '',    # Mbits_1 value
        'REPLAY_1_RATE': '',  # replay value
        'FPS_1': '',
        'TEST_2_RATE': '',
        'REPLAY_2_RATE': '',
        'FPS_2': ''
    }
    assert passed_rates
    # REPLAY_1_RATE and REPLAY_2_RATE are not defined in any script.
    return  # REPLAY_1_RATE, REPLAY_2_RATE


def size_conversion(bytes):
    # covert the CTD file size into an MB value
    units = 'MB'
    KB = bytes / 1024
    MB = KB / 1024
    MB = f'{MB} {units}'
    return MB


def bytes_conversion(bytes):
    # converts to bytes to Mbits f
    bits = bytes * 8
    kbits = bits / 1000
    Mbits = kbits / 1000
    print('IN bytes_conversion FUNCTION')
    print(f'Capture Results bytes_conversion function value: {Mbits}')
    return Mbits


def trex_rate(passed_trex_rate):
    # return the last element in the list which is the last passed trex rate
    print('IN TREX RATES')
    if len(passed_trex_rate) > 0:
        print('Passed Rate:' + passed_trex_rate)
        return passed_trex_rate[-1]
    return


def replay_rate(passed_replay_rate):
    # return the last element in the list which is the last passed replay rate
    if len(passed_replay_rate) > 0:
        # print('replay rate:' +  passed_replay_rate[-1])
        return passed_replay_rate[-1]
    return


def replay_Mbps(passed_replay_Mbps):
    print('IN REPLAY_MBPS FUNCTION ')
    if len(passed_replay_Mbps) > 0:
        print('passed_replay_Mbps' + (passed_replay_Mbps[-1]))
        return passed_replay_Mbps[-1]
    return


def final_rate(passed_rates):
    # return the last element in the list which is the last passed capture bit rate
    if len(passed_rates) > 0:
        return passed_rates[-1]
    return


def finalfps(passed_fps):
    # return the last element in the list which is the last passed FPS value
    if len(passed_fps) > 0:
        return passed_fps[-1]
    return


def final_duration(passed_duration):
    # return the last element in the list which is the last passed capture test duration
    if len(passed_duration) > 0:
        f_duration = str(passed_duration[-1]) + ' ' 'Seconds'
        return f_duration
    return


def drop_count(drop_pkts):
    if len(drop_pkts) > 0:
        return drop_pkts[-1]
    return 0


def final_packet(packet_count):
    if len(packet_count) > 0:
        return packet_count[-1]
    return 0


def final_percent(percent_count):
    if len(percent_count) > 0:
        return percent_count[-1]
    return 0


def percent_diff(a_cap_dropped, cap_pkt):
    if cap_pkt > 0:
        percent = (float(a_cap_dropped) / float(cap_pkt)*100)
        # percent_diff = 100 - (float(new_rate) / float(base_rate)*100)
        return percent
    return 0


def flow_percent_diff(spot_flow, trex_flows):
    if spot_flow > 0:
        percent = (float(trex_flows) / float(spot_flow)*100)
        print('Flow Percent Difference is:' + percent)
        return percent
    return 0


def get_adapters(ports):
    # pass self.ports
    print('In get_adapters function')
    adap_list = []
    print(f'Port passed in: {ports}')
    if ports == 1:
        adap_list = ['eth1']   # eth1
    elif ports == 2:
        adap_list = ['eth1', 'eth2']  # eth1', 'eth2
    elif ports == 3:
        adap_list = ['eth1', 'eth2', 'eth3']
    elif ports == 4:
        adap_list = ['Bridge']  # default is bro only for ports = 5
    print(adap_list)
    return adap_list

# get_disk_info('10.8.102.12')
# delete_anyfile('10.8.102.12')
