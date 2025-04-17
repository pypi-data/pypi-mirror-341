import paramiko
import omniscript


class TestReporter(object):
    def __init__(self, host, file_name):
        self.autoresults_dic1t = {}
        # self.autoresults_dict2 = {
        #     "ADAPTER_NAME":  "",
        #     "ADAPTER_INTF": "",
        #     "ADAPTER_FIRMWARE":  ""
        #     }

        self.host = host
        print("host:" + self.host)
        self.port = 6367
        # self.interface = adap_list
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.load_system_host_keys()
        try:
            self.ssh.connect(self.host, 22, 'root', 'Spider8fly!')
        except paramiko.AuthenticationException:
            print('trying next password!')
            try:
                self.ssh.connect(self.host, 22, 'admin', 'admin')
            except Exception:
                print('Failed to connect with default password')
        self.file_name1 = open(file_name, 'a+')

    def __del__(self):
        if self.file_name1 is not None:
            self.file_name1.close()
        if self.ssh is not None:
            self.ssh.close()

    def EngineInfo(self):
        # Get information about a remote OmniEngine i.e. IP, Name,Memmory, diskspace,
        # CPU, RAID, OS and Omnistatus info.
        print('IN EngineInfo!')
        credentials = [
            ('root', 'Spider8fly!'),
            ('admin', 'admin'),
            ('tsadmin', 'Spider8fly!')
        ]
        self.omni = omniscript.OmniScript()
        self.engine = self.omni.create_engine(self.host)
        for c in credentials:
            if self.engine.login(c[0], c[1]):
                break
        if not self.engine.is_connected:
            print('Failed to connect with either "Spider8fly!", "Spider8fly" or "admin" passwords')
            raise Exception('Faile to connect to engine.')

        stdin, stdout, stderr = self.ssh.exec_command('lsb_release -a |grep Description')
        stdin.close()
        os = stdout.read().strip('\n')
        print('os:' + os)

        stdin, stdout, stderr = self.ssh.exec_command("dpkg -s omni|grep -E 'Version'")
        stdin.close()
        build = stdout.read().strip('\n')
        print('build:' + build)

        stdin, stdout, stderr = self.ssh.exec_command("cat /proc/meminfo | grep MemTotal")
        stdin.close()
        mem = stdout.read().strip('\n')
        print(f'MEM {mem}')

        stdin, stdout, stderr = self.ssh.exec_command(
            'cat /proc/cpuinfo | grep "model name" | head -1')
        stdin.close()
        cpu = stdout.read().strip('\n')
        print('CPU {cpu}')

        print("GETTING RAID INFO")
        stdin, stdout, stderr = self.ssh.exec_command('lspci | grep RAID | tail -n 1')
        stdin.close()
        raid = stdout.read().strip('\n')
        print(f'RAID_NAME: {raid}')

        print('GETTING Hard DRIVE INFO')
        stdin, stdout, stderr = self.ssh.exec_command(
            'lshw -class disk | grep product | sed s/product://ig | tail -n 1')
        stdin.close()
        hdrive = stdout.read().strip('\n')
        print('HDD_MANU {hdrive}')

        print('closing test reporter file!')
        self.file_name1.close()
        self.engine.disconnect()

        autoresults_dict1 = {
            'ENGINE_IP': self.host,
            'ENGINE_BUILD': build,
            'ENGINE_OS': os
        }
        autoresults_dict1.update({
            'MEMORY': mem,
            'CPU': cpu,
            'RAID_NAME': raid,
            'HDD_MANU': hdrive
        })
        self.engine.disconnect()
        return autoresults_dict1

        # def AdapterInfo(self):
        #     # delete the eth5 foo and uncomment out line 117
        #     for adap in self.interface:
        #         print(f'Adapter in interface_list: {adap}')
        #         if adap == 'enp101s0f0' or adap == 'eno1np0':
        #             self.autoresults_dict2.update({
        #                     'ADAPTER_NAME': adap,
        #                     'ADAPTER_INTF': 'Gibabit',
        #                     'ADAPTER_FIRMWARE': 'N/A'
        #             })
        #             print(self.autoresults_dict2)
        #             if adap == 'enp101s0f0' or 'enp101s0f1':
        #                 #stdin, stdout, stderr = self.ssh.exec_command(
        #                 # "lspci -s `cat /sys/class/net/dna0/info/pciebnbr | xargs "
        #               # "printf '%x'`:.0 | "
        #                 # "sed 's/.*:\\s\\+\\(.*\\)/\\1/'")
        #                 stdin, stdout, _ = self.ssh.exec_command(
        #                     "lspci -s `cat /sys/class/net/dna0/info/pciebnbr | xargs "
        #                     "printf '%x'`:.0 "
        #                     "|sed 's/.*:\\s\\+\\(.*\\)/\\1/'")
        #                 stdin.close()
        #                 Type = stdout.read().strip('\n')
        #                 print(f'Type: {Type}')
        #                 self.autoresults_dict2.update({
        #                     'ADAPTER_NAME': (self.autoresults_dict2.get("ADAPTER_NAME") +
        #                                     f'{Type} '),
        #                     'ADAPTER_INTF': (self.autoresults_dict2.get("ADAPTER_INTF") +
        #                                     '10-Gibabit ')
        #                 })
        #             else:
        #                 print("failed to mach an Adapter!")
        #         # print "Dict2" ,self.autoresults_dict2
        #     return self.autoresults_dict2

    def HardWareInfo(self):
        Dict1 = {}
        # Dict2 = {}
        Dict1 = self.EngineInfo()
        # Dict2 = self.AdapterInfo()
        # Dict2.update(Dict1)
        # print(Dict1)

        if self.file_name1 is not None:
            self.file_name1.close()
        if self.ssh is not None:
            self.ssh.close()
        return Dict1


# test = TestReporter(host = '10.8.100.3', adap_list=["ens1f1"], file_name = 'test.txt') #
# # test.EngineInfo()
# # # # # test.ssh.close()
# test.AdapterInfo()
# # # test.HardWareInfo()
