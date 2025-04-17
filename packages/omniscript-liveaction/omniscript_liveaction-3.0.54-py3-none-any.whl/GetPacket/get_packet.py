import sys
import omniscript
from omniscript.invariant import DECODE_HTML, ENGINE_FORMAT_PLAIN, ENGINE_FORMAT_HTML

# host = '192.168.7.201'
# user = 'gary'
# pwd = 'savvages'

host = '192.168.7.201'
user = 'gary'
pwd = 'savvages'

capture_name = 'Python Test Capture'
tab = 15

omni = omniscript.OmniScript()

engine = omni.create_engine(host)
if not engine.login(user, pwd):
    print('Failed to connect to the engine')
    sys.exit(1)

capt = engine.find_capture(capture_name)
if not capt:
    ct = omniscript.CaptureTemplate()

    al = engine.get_adapter_list()
    adpt = omniscript.find_adapter(al, 'eth0')
    if adpt is None:
        adpt = omniscript.find_adapter(al, 'eno1')
    if not adpt:
        print('Failed to find default adapter: eth0 or eno1')
        sys.exit(1)

    ct.set_adapter(adpt)
    ct.general.buffer_size = 1024 * 1024
    ct.general.name = capture_name
    ct.general.option_continuous_capture = True
    ct.general.option_capture_to_disk = True
    ct.general.option_start_capture = True
    ct.set_all(True)
    capt = engine.create_capture(ct)

if not capt:
    print('Failed to create capture.')
    sys.exit(1)

while capt.packets_filtered < 25:
    capt.refresh()

capt.stop()
capt.refresh()
if capt.packets_filtered < 25:
    print('Not enough packets.')
    sys.exit(1)

pkt_number = capt.first_packet + 5
p = capt.get_packet(pkt_number)
if p:
    print(f'Packet Number: {p.number}')
    print(f'{"Index":>{tab}}: {p.index}')
    if p.timestamp:
        print(f'{"Time Stamp":>{tab}}: {p.timestamp.iso_time()}')
    print(f'{"ProtoSpec":>{tab}}: {p.proto_spec}')
    print(f'{"Protocol Name":>{tab}}: {p.protocol_name()}')
    print(f'{"Application":>{tab}}: {p.application}')
    print(f'{"Flags":>{tab}}: {hex(p.flags)}')
    print(f'{"Flow Id":>{tab}}: {p.flow_id}')
    print(f'{"Status":>{tab}}: {hex(p.status)}')
    print(f'{"Length":>{tab}}: {p.packet_length}')

d = capt.get_packet_data(pkt_number)
print(d)

cp = capt.get_packet_decode(pkt_number)
print(cp)
ch = capt.get_packet_decode(pkt_number, DECODE_HTML)
print(ch)

fp = capt.first_packet + 1
# Get packets 0, 1, 2, 3, 10, 11, 20
pl = capt.get_packets([(fp+0,fp+3),(fp+10,fp+11),fp+20])
for pi in pl:
    print(f'Packet Number: {pi.number}')

es = engine.get_status()
if es:
    print(f'Engine Status: {es.name}')
    print(f'{"Adapter Count":>{tab}}: {es.adapter_count}')
    print(f'{"Capture Count":>{tab}}: {es.capture_count}')
    print(f'{"CPU Count":>{tab}}: {es.cpu_count}')
    print(f'{"CPU Type":>{tab}}: {es.cpu_type}')
    print(f'{"Data Folder":>{tab}}: {es.data_folder}')
    print(f'{"Engine Type":>{tab}}: {es.engine_type}')
    print(f'{"File Count":>{tab}}: {es.file_count}')
    print(f'{"File Version":>{tab}}: {es.file_version}')
    print(f'{"Filter Count":>{tab}}: {es.filter_count}')
    print(f'{"Host":>{tab}}: {es.host}, Port: {es.port}')
    print(f'{"Log Total Count":>{tab}}: {es.log_total_count}')
    print(f'{"Operating System":>{tab}}: {es.operating_system}')
    print(f'{"OS":>{tab}}: {es.os}')
    print(f'{"Platform":>{tab}}: {es.platform}')
    print(f'{"Product Version":>{tab}}: {es.product_version}')
