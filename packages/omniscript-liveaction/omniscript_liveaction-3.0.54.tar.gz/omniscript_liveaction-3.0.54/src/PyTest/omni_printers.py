# Copyright (c) LiveAction, Inc. 2022-2023. All rights reserved.
# Copyright (c) Savvius, Inc. 2013-2022. All rights reserved.
# Copyright (c) WildPackets, Inc. 2013-2014. All rights reserved.

from textwrap import TextWrapper as TW
from typing import List

from omniscript import (
    Adapter, AdapterInformation, Alarm, CaptureTemplate, Capabilities, ExpertDescription)

from omniscript.invariant import (
    NANOSECONDS_PER_SECOND, SECONDS_PER_DAY, SECONDS_PER_HOUR, SECONDS_PER_MINUTE, SummaryType)

adapter_type_name = ("0: Unknown", "1: NIC", "2: File", "3: Plugin")


def duration(value):
    if value is None:
        return 0, 0, 0, 0, 0
    v1 = value / NANOSECONDS_PER_SECOND
    nanoseconds = value % NANOSECONDS_PER_SECOND
    days = v1 / SECONDS_PER_DAY
    v2 = v1 % SECONDS_PER_DAY
    hours = v2 / SECONDS_PER_HOUR
    v3 = v2 % SECONDS_PER_HOUR
    minutes = v3 / SECONDS_PER_MINUTE
    seconds = v3 % SECONDS_PER_MINUTE
    return int(days), int(hours), int(minutes), int(seconds), int(nanoseconds)


def format_duration(*a, **kw):
    if isinstance(a, tuple) and a[0]:
        if len(a) == 1:
            days, hours, minutes, seconds, nanoseconds = duration(a[0])
        elif len(a) == 5:
            days, hours, minutes, seconds, nanoseconds = a
    elif isinstance(a, int):
        days, hours, minutes, seconds, nanoseconds = duration(a)
    elif isinstance(kw, dict) and len(kw):
        days = kw['d'] if 'd' in kw else kw['days'] if 'days' in kw else 0
        hours = kw['h'] if 'h' in kw else kw['hours'] if 'hours' in kw else 0
        minutes = kw['m'] if 'm' in kw else kw['minutes'] if 'minutes' in kw else 0
        seconds = kw['s'] if 's' in kw else kw['seconds'] if 'seconds' in kw else 0
        nanoseconds = kw['n'] if 'n' in kw else kw['nanoseconds'] if 'nanoseconds' in kw else 0
    else:
        days, hours, minutes, seconds, nanoseconds = 0, 0, 0, 0, 0

    if days:
        return f'{days} days, {hours} hours, {minutes} minutes {seconds}.{nanoseconds} seconds'
    elif hours:
        return f'{hours} hours, {minutes} minutes {seconds}.{nanoseconds} seconds'
    elif minutes:
        return f'{minutes} minutes {seconds}.{nanoseconds} seconds'
    elif seconds or nanoseconds:
        return f'{seconds}.{nanoseconds} seconds'
    else:
        return ""


def format_result(value: int) -> str:
    if value == 0:
        return '0'
    if value < 0:
        value += 1 << 32
        return f'0x{value:0x}'
    return f'0x{value:0X}'


def print_duration(*a, **kw):
    print(format_duration(*a, **kw))


def print_object(obj):
    if isinstance(obj, dict):
        print("{")
        for k, v in obj.items():
            if isinstance(v, dict):
                print(f"'{k}' : ")
                print_object(v)
            else:
                print(f"'{k}' : '{v}',")
        print("},")
    elif isinstance(obj, list):
        for i in obj:
            print(f"{i},")
    else:
        print(f"{obj},")


def print_access_control_policy(acp, tab=20):
    print(f'{"Id":>{tab}}: {acp.id}')


def print_access_control_list(acl, tab=20, class_names=None):
    if acl is None:
        print('No Access Control List')
        return
    print(f'{"Access Control List":>{tab}}:')
    if class_names:
        for acp in acl:
            print(
                f'{"Policy":>{tab}}: {acp.id} : {class_names[acp.id]}'
                f', Commands: [{", ".join(str(v["id"])+":"+v["title"] for v in acp.command_list)}]'
                f', Users: [{", ".join(v.name for v in acp.user_list)}]'
            )
    else:
        for acp in acl:
            print(
                f'{"Policy":>{tab}}: {acp.id}'
                f', Commands: [{", ".join(str(v) for v in acp.command_list)}]'
                f', Users: [{", ".join(v.name for v in acp.user_list)}]'
            )


def print_adapter(a: Adapter, tab=20):
    if a is None:
        print('No adapter')
        return
    print(f'Adapter: {a.name}')
    print(f'{"Id":>{tab}}: {a.adapter_id}')
    print(f'{"Features":>{tab}}: {a.features}')
    print(f'{"Type":>{tab}}: {adapter_type_name[a.adapter_type]}')
    print(f'{"Address":>{tab}}: {a.address}')
    print(f'{"Description":>{tab}}: {a.description}')
    print(f'{"Device Name":>{tab}}: {a.device_name}')
    print(f'{"Interface Features":>{tab}}: {a.interface_features}')
    print(f'{"Link Speed":>{tab}}: {a.link_speed:,}')
    # print(f'{"Media Type":>{tab}}: {omniscript.MEDIA_TYPE_NAMES[a.media_type]}')
    # print(f'{"Media Sub Type":>{tab}}: {omniscript.MEDIA_SUB_TYPE_NAMES[a.media_sub_type]}')
    print(f'{"OmniPeek API":>{tab}}: {a.wildpackets_api}')
    print()


def print_adapter_list(al: List[Adapter]):
    if al:
        for a in al:
            print_adapter(a)
    print()


def print_adapter_information(a: AdapterInformation, tab=20):
    if a is None:
        print('No adapter information')
        return
    print(f'Adapter: {a.name}')
    print(f'{"Adapter Type":>{tab}}: {a.adapter_type}')
    print(f'{"Address":>{tab}}: {a.address}')
    print(f'{"Channel List":>{tab}}: {a.channel_list}')
    print(f'{"Characteristics":>{tab}}: {a.characteristics}')
    print(f'{"Description":>{tab}}: {a.description}')
    print(f'{"Enumerator":>{tab}}: {a.enumerator}')
    print(f'{"Extended Description":>{tab}}: {a.extended_description}')
    print(f'{"Features":>{tab}}: {a.features}')
    print(f'{"Flags":>{tab}}: {a.flags}')
    print(f'{"Id":>{tab}}: {a.adapter_id}')
    print(f'{"Link Speed":>{tab}}: {a.link_speed}')
    print(f'{"Media Type":>{tab}}: {a.media_type}')
    print(f'{"Media Sub Type":>{tab}}: {a.media_sub_type}')
    print(f'{"Product Name":>{tab}}: {a.product_name}')
    print(f'{"Service Name":>{tab}}: {a.service_name}')
    print(f'{"Symbolic Link":>{tab}}: {a.symbolic_link}')
    print(f'{"Title":>{tab}}: {a.title}')
    print(f'{"Versions":>{tab}}: {a.versions}')
    print(f'{"Hidden":>{tab}}: {a.option_hidden}')
    print(f'{"Valid":>{tab}}: {a.option_valid}')
    print(f'{"Valid_advanced":>{tab}}: {a.option_valid_advanced}')
    print(f'{"Virtual":>{tab}}: {a.option_virtual}')
    print()


def print_adapter_information_list(al: List[AdapterInformation]):
    if al:
        for a in al:
            print_adapter_information(a)
    print()


def print_adapter_configuration(ac, tab=20):
    if ac is None:
        print('No adapter configuration')
        return
    fmt_d = '%%%ds: %%d' % tab
    fmt_s = '%%%ds: %%s' % tab
    print(fmt_s % ('Id', ac.id))
    print(fmt_s % ('Type', adapter_type_name[ac.adapter_type]))
    print(fmt_d % ('Link Speed', ac.link_speed))
    print(fmt_d % ('Default Link Speed', ac.default_link_speed))
    print(fmt_d % ('Ring Buffer Size', ac.ring_buffer_size))
    for id in ac.ids:
        print(fmt_s % ('Id', id))


def print_alarm(a: Alarm, tab=20):
    if a is None:
        print('No alarm')
        return
    print(f'Alarm: {a.name}')
    print(f'{"Id":>{tab}}: {a.id}')
    print(f'{"Created":>{tab}}: {a.created}')
    print(f'{"Modified":>{tab}}: {a.modified}')
    print(f'{"Track Type":>{tab}}: {a.tracker_type}')
    if a.tracker:
        t = a.tracker
        print(f'{"Statistics Tracker":>{tab}}:')
        print(f'{"History":>{tab+4}}: {t.history}')
        print(f'{"Type":>{tab+4}}: {t.type}')
        if t.summary:
            s = t.summary
            print(f'{"Summary":>{tab+4}}: Type: {s.type}, Flags: {s.flags}')
    if a.conditions:
        print(f'{"Conditions":>{tab}}:')
        i = 1
        for c in a.conditions:
            print(f'{"":>{tab+4}}  #{i}')
            print(f'{"Enabled":>{tab+4}}: {c.enabled}')
            print(f'{"Type":>{tab+4}}: {c.condition_type}')
            print(f'{"Duration":>{tab+4}}: {format_duration(c.duration)}')
            print(f'{"Comparison":>{tab+4}}: {c.comparison_type}')
            print(f'{"Value":>{tab+4}}: {c.value}')
            print(f'{"Severity":>{tab+4}}: {c.severity}')
            i += 1
    print()


def print_alarm_list(al: List[Alarm]):
    if al:
        for a in al:
            print_alarm(a)
    print()


def print_analysis_module(am, tab=20):
    if am is None:
        print('No Analysis Module')
        return
    print(f'Analysis Module: {am.name}')
    print(f'{"Id":>{tab}}: {am.id}')
    print(f'{"File Name":>{tab}}: {am.file_name}')
    print(f'{"Publisher":>{tab}}: {am.publisher}')
    print(f'{"Version":>{tab}}: {am.version}')
    print()


def print_analysis_module_list(aml):
    if aml:
        for am in aml:
            print_analysis_module(am)
    print()


def print_application(a, tab=20):
    if a is None:
        print('No application')
        return
    print(f'Application: {a.name}')
    print(f'{"Name":>{tab}}: {a.name}')
    print(f'{"category":>{tab}}: {a.category}')
    print(f'{"color":>{tab}}: {a.color}')
    print(f'{"description":>{tab}}: {a.description}')
    print(f'{"id_code":>{tab}}: {a.id_code}')
    print(f'{"productivity":>{tab}}: {a.productivity}')
    if a.reference:
        print(f'{"reference":>{tab}}: {a.reference}')
    print(f'{"risk":>{tab}}: {a.risk}')
    print()


def print_application_list(al):
    if al:
        for a in al:
            print_application(a)
    print()


def print_application_stat(application_stat, tab=20):
    if application_stat is None:
        print('No application statistics')
        return
    print(f'{"Application Statistic":>24}: {application_stat.name}')
    print(f'{"Bytes":>28}: {application_stat.bytes:,}')
    print(f'{"Color":>28}: {application_stat.color}')
    print(f'{"Duration":>28}: {format_duration(application_stat.duration)}')
    print(f'{"First Time":>28}: {application_stat.first_time}')
    print(f'{"Last Time":>28}: {application_stat.last_time}')
    print(f'{"Packets":>28}: {application_stat.packets:,}')
    print()


def print_application_stats(application_stats, tab=20):
    if application_stats is None:
        print('No Application Statistics')
        return
    print('Application Statistics')
    print(f'{"Duration":>20}: {format_duration(application_stats.duration)}')
    print(f'{"Reset Count":>20}: {application_stats.reset_count:,}')
    print(f'{"Time Limit Reached":>20}: {application_stats.time_limit_reached}')
    print(f'{"Total Bytes":>20}: {application_stats.total_bytes:,}')
    print(f'{"Total Packets":>20}: {application_stats.total_packets:,}')
    print(f'{"Applications":>20}: {len(application_stats.application_stats)}')
    for stat in application_stats.application_stats:
        print_application_stat(stat, tab=20)
    print()


def print_application_flow_stat(app_flow_stat, tab=20):
    if app_flow_stat is None:
        print('No Application Flow Statistics')
        return
    print(f'{"Application":>24}: {app_flow_stat.name}')
    print(f'{"Color":>28}: {app_flow_stat.color}')
    print(f'{"Flow Count":>28}: {app_flow_stat.flow_count}')
    print(f'{"Id Code":>28}: {app_flow_stat.id_code}')
    print(f'{"Id Name":>28}: {app_flow_stat.id_name}')
    print()


def print_application_flow_stats(app_flow_stats, tab=20):
    if app_flow_stats is None:
        print('No Application Flow Statistics')
        return
    print('Application Flow Statistics')
    print(f'{"Duration":>20}: {format_duration(app_flow_stats.duration)}')
    print(f'{"Total Bytes":>20}: {app_flow_stats.total_bytes:,}')
    print(f'{"Total Packets":>20}: {app_flow_stats.total_packets:,}')
    print(f'{"Applications":>20}: {len(app_flow_stats.application_flow_stats)}')
    for stat in app_flow_stats.application_flow_stats:
        print_application_flow_stat(stat, tab=20)
    print()


def print_audit_log_message(m, tab=20, verbose=True):
    if m is None:
        print('No Audit Log Message')
        return
    print(f'{"Id":>{tab}}: {m.id}')
    if verbose:
        print(f'{"Client":>{tab}}: {m.client}')
        print(f'{"Message":>{tab}}: {m.message}')
        print(f'{"Result":>{tab}}: {format_result(m.result)}')
        print(f'{"User":>{tab}}: {m.user}')
        print(f'{"Timestamp":>{tab}}: {m.timestamp}')
        print()


def print_audit_log(al, tab=20):
    if al is None:
        print('No Audit Log')
        return
    print(f'Audit Log for {al._engine.name}.')
    print(f'{"count":>{tab}}: {al.count}')
    print(f'{"total_count":>{tab}}: {al.total_count}')
    print(f'{"start_timestamp":>{tab}}: {al.start_timestamp}')
    print(f'{"end_timestamp":>{tab}}: {al.end_timestamp}')
    print(f'{"first_timestamp":>{tab}}: {al.first_timestamp}')
    print(f'{"last_timestamp":>{tab}}: {al.last_timestamp}')
    for m in al.message_list:
        print_audit_log_message(m, (tab+4))


def print_audit_log_indexes(al, tab=20):
    if al is None:
        print('No Audit Log')
        return
    fmt_d = '%%%ds: %%d' % tab
    fmt_s = '%%%ds: %%s' % tab
    print(str(al))
    print(fmt_d % ('Count', al.count))
    print(fmt_s % ('First', al.first))
    print(fmt_s % ('Last', al.last))
    for e in al.entries:
        print_audit_log_message(e, (tab+4), False)


def print_authentication_token(a, tab=20):
    if a is None:
        print('No authentication token')
        return
    print(f'{"Authentcaion Token Id":>{tab}}: {a.authentcaion_token_id}')
    print(f'{"Client":>{tab}}: {a.client}')
    print(f'{"Expiration Time":>{tab}}: {a.expiration_time or ""}')
    print(f'{"Label":>{tab}}: {a.label}')
    print(f'{"Last Activity Time":>{tab}}: {a.last_activity_time or ""}')
    print(f'{"User Domain":>{tab}}: {a.user_domain}')
    print(f'{"User Id":>{tab}}: {a.user_id}')
    print(f'{"User Information Id":>{tab}}: {a.user_information_id}')
    print(f'{"User Name":>{tab}}: {a.user_name}')
    print(f'{"Option Authentication":>{tab}}: {a.option_authentication}')
    print(f'{"Option Enabled":>{tab}}: {a.option_enabled}')
    print()


def print_authentication_token_list(al):
    if al:
        for a in al:
            print_authentication_token(a)
    print()


# def print_call_quality(quality, tab=20):
#     fmt_d = '%%%ds: %%d' % tab
#     fmt_s = '%%%ds: %%s' % tab
#     print(fmt_d % ('Quality Interval', quality.interval))
#     print(fmt_s % ('Start Time', quality.start_time or ""))
#     print(fmt_d % ('Codec Count', len(quality.codecs)))


def print_call_statistic(call, tab=20):
    print(f'{"":8}All Quality Distribution:')
    print(f'{"":12}{call.all_quality_distribution}')
    print(f'{"":8}Open Quality Distribution:')
    print(f'{"":12}{call.open_quality_distribution}')
    print(f'{"":8}Codec Quality Distribution: {len(call.codec_quality_list)}')
    for item in call.codec_quality_list:
        print(f'{"Interval":>20}: {item.interval:,}')
        print(f'{"Start":>20}: {item.start_time}')
        print(f'{"Samples":>20}: {len(item.sample_list):,}')
        for sample in item.sample_list:
            print(f'{"":20}{sample}')
    print(f'{"":8}Call Quality Utilization: {len(call.quality_utilization_list)}')
    for item in call.quality_utilization_list:
        print(f'{"Interval":>20}: {item.interval:,}')
        print(f'{"Start":>24}: {item.start_time}')
        print(f'{"Samples":>40}: {len(item.sample_list):,}')
        for sample in item.sample_list:
            print(f'{"":24}{sample}')
    print(f'{"":8}Utilization: {len(call.utilization_list)}')
    for item in call.utilization_list:
        print(f'{"Interval":>20}: {item.interval:,}')
        print(f'{"Start":>24}: {item.start_time}')
        print(f'{"Samples":>24}: {len(item.sample_list):,}')
        for sample in item.sample_list:
            print(f'{"":24}{sample}')


def print_call_utilization(sample, tab):
    print(f'{"bad":>{tab}}: {sample.bad}')
    print(f'{"poor":>{tab}}: {sample.poor}')
    print(f'{"fair":>{tab}}: {sample.fair}')
    print(f'{"good":>{tab}}: {sample.good}')
    if sample.unknown is not None:
        print(f'{"unknown":>{tab}}: {sample.good}')


def print_call_stats(call_stats, tab=20):
    if call_stats is None:
        print('No call statistic')
        return
    print('Call Statistics')
    print(f'{"":4}Calls: {len(call_stats.call_stats)}')
    for call in call_stats.call_stats:
        print_call_statistic(call, tab)
        print()
    print()


# def print_connected_user(c: ConnectedUser, tab=20):
#     if c is None:
#         print('No connected user')
#         return
#     print(f'Connected User: {c.name}')
#     print(f'{"Address":>{tab}}: {c.address}')
#     print(f'{"Port":>{tab}}: {c.port}')
#     print(f'{"Start Time":>{tab}}: {c.start_time or ""}')
#     print(f'{"End Time":>{tab}}: {c.end_time or ""}')
#     print()


# def print_connected_user_list(cl: List):
#     if cl:
#         for c in cl:
#             print_connected_user(c)
#     print()


def print_capture(c, tab=20):
    if c is None:
        print('No capture')
        return
    fmt_d = '%%%ds: %%d' % tab
    fmt_s = '%%%ds: %%s' % tab
    print('Capture: %s' % c.name)
    print(fmt_s % ('Id', c.id))
    print(fmt_s % ('Status', c.status))
    print(fmt_s % ('Comment', c.comment))
    print(fmt_s % ('Creator', c.creator))
    print(fmt_s % ('Creator SID', c.creator_sid))
    print(fmt_s % ('Logged on User SID', c.logged_on_user_sid))
    print(fmt_s % ('Last Modification Time', c.modification_time or ""))
    print(fmt_s % ('Last Modification', c.modification_type))
    print(fmt_s % ('Last Modified By', c.modified_by))
    print(fmt_s % ('Adapter', c.adapter))
    print(fmt_d % ('Adapter Type', c.adapter_type))
    print(fmt_d % ('Link Speed', c.link_speed))
    print(fmt_d % ('Media Type', c.media_type))
    print(fmt_d % ('Media Sub Type', c.media_sub_type))
    print(fmt_d % ('Buffer Size', c.buffer_size))
    print(fmt_d % ('Buffer Available', c.buffer_available))
    print(fmt_d % ('Buffer Used', c.buffer_used))
    print(fmt_d % ('Filter Mode', c.filter_mode))
    print(fmt_d % ('Graphs Count', c.graphs_count))
    print(fmt_s % ('Plugin List', c.plugin_list))
    print(fmt_s % ('Start Time', c.start_time or ""))
    print(fmt_s % ('Stop Time', c.stop_time or ""))
    print(fmt_s % ('Duration', format_duration(c.duration)))
    print(fmt_d % ('Reset Count', c.reset_count))
    print(fmt_d % ('Packets Received', c.packets_received))
    print(fmt_d % ('Packets Filtered', c.packets_filtered))
    print(fmt_d % ('Packet Count', c.packet_count))
    print(fmt_d % ('Analysis Dropped Packets', c.analysis_dropped_packets))
    print(fmt_d % ('Duplicate Packets Discarded', c.duplicate_packets_discarded))
    print(fmt_d % ('Packets Analyzed', c.packets_analyzed))
    print(fmt_d % ('Packets Dropped', c.packets_dropped))
    print(fmt_d % ('First Packet', c.first_packet))
    print(fmt_d % ('Alarms Info', c.alarms_info))
    print(fmt_d % ('Alarms Minor', c.alarms_minor))
    print(fmt_d % ('Alarms Major', c.alarms_major))
    print(fmt_d % ('Alarms Severe', c.alarms_severe))
    print(fmt_d % ('Trigger Count', c.trigger_count))
    print(fmt_s % ('Trigger Duration', format_duration(c.trigger_duration)))
    print(fmt_s % ('Option Alarms', c.option_alarms))
    print(fmt_s % ('Option CTD', c.option_ctd))
    print(fmt_s % ('Option Distributed', c.option_distributed))
    print(fmt_s % ('Option Expert', c.option_expert))
    print(fmt_s % ('Option Filters', c.option_filters))
    print(fmt_s % ('Option Graphs', c.option_graphs))
    print(fmt_s % ('Option Hidden', c.option_hidden))
    print(fmt_s % ('Option Indexing', c.option_indexing))
    print(fmt_s % ('Option Packet Buffer', c.option_packet_buffer))
    print(fmt_s % ('Option Spotlight', c.option_spotlight))
    print(fmt_s % ('Option Threateye', c.option_threateye))
    print(fmt_s % ('Option Timeline Stats', c.option_timeline_stats))
    print(fmt_s % ('Option Voice', c.option_voice))
    print(fmt_s % ('Option Web', c.option_web))
    print()
    print_adapter(c.adapter)
    print_media_info(c.media_information)
    print()


def print_capture_list(cl):
    if cl:
        for c in cl:
            print_capture(c)
    print()


def print_capture_session(cs, tab=20):
    if cs is None:
        print('No capture session')
        return
    print(f'{"Name":>{tab}}: {cs.name}')
    print(f'{"Session Id":>{tab}}: {cs.session_id}')
    print(f'{"Adapter Name":>{tab}}: {cs.adapter_name}')
    print(f'{"Adapter Address":>{tab}}: {cs.adapter_address}')
    print(f'{"Capture Flags":>{tab}}: {cs.capture_flags}')
    print(f'{"Capture Id":>{tab}}: {cs.capture_id}')
    print(f'{"Capture Id Alt":>{tab}}: {cs.alt_capture_id}')
    print(f'{"Capture State":>{tab}}: {cs.capture_state}')
    print(f'{"Capture Type":>{tab}}: {cs.capture_type}')
    print(f'{"Capture Units":>{tab}}: {cs.capture_units}')
    print(f'{"Dropped Packets":>{tab}}: {cs.dropped_packet_count}')
    print(f'{"Link Speed":>{tab}}: {cs.link_speed}')
    print(f'{"Media Type":>{tab}}: {cs.media_type}')
    print(f'{"Media SubType":>{tab}}: {cs.media_sub_type}')
    print(f'{"Owner":>{tab}}: {cs.owner}')
    print(f'{"Packet Count":>{tab}}: {cs.packet_count}')
    print(f'{"Session Start":>{tab}}: {cs.session_start_time or ""}')
    print(f'{"Start Time":>{tab}}: {cs.start_time or ""}')
    print(f'{"Storage Units":>{tab}}: {cs.storage_units}')
    print(f'{"Stop Time":>{tab}}: {cs.stop_time or ""}')
    print(f'{"Total Bytes":>{tab}}: {cs.total_byte_count}')
    print(f'{"Total Dropped":>{tab}}: {cs.total_dropped_packet_count}')
    print(f'{"Total Packets":>{tab}}: {cs.total_packet_count}')
    print()


def print_capture_session_list(csl):
    if csl:
        for cs in csl:
            print_capture_session(cs)
    print()


def print_capture_session_data(csd, tab=20):
    if csd is None:
        print('No capture session data')
        return
    print(f'{"Capture Session Name":>{tab}}: {csd._session.name}')
    print(f'{"Session Id":>{tab}}: {csd.session_id}')
    print(f'{"Data Type":>{tab}}: {csd.data_type}')
    print(f'{"Start Time":>{tab}}: {csd.start_time or ""}')
    print(f'{"End Time":>{tab}}: {csd.end_time or ""}')
    print(f'{"Sample Interval":>{tab}}: {csd.sample_interval}')
    if csd.data_list:
        print(f'{"Data":>{tab}}:')
        for c in csd.data_list:
            print(f'{"":>{tab}} {c.format()}')
    else:
        print(f'{"Data":>{tab}}: {csd.data_list}')
    print()


def print_capture_session_statistics(css, tab=20):
    if css is None:
        print('No capture session statistics')
        return
    print(f'{"Capture Session Name":>{tab}}: {css._session.name}')
    print(f'{"Session Id":>{tab}}: {css.session_id}')
    print(f'{"Data Type":>{tab}}: {css.statistic_type}')
    print(f'{"Start Time":>{tab}}: {css.start_time or ""}')
    print(f'{"End Time":>{tab}}: {css.end_time or ""}')
    if css.entry_list:
        print(f'{"Entry List":>{tab}}:')
        for c in css.entry_list:
            print(f'{"":>{tab}} {c.format()}')
    else:
        print(f'{"Entry List":>{tab}}: {css.entry_list}')
    print()


def string_adapter_settings(a):
    at = ['', 'NIC', 'File', 'Plugin']
    return f'{a.name} - {at[a.adapter_type]} Adapter'


def string_analysis_settings(a):
    s = []
    if a.option_alarms:
        s.append('Alarm')
    if a.option_analysis_modules:
        s.append('AnMods')
    if a.option_application:
        s.append('Apps')
    if a.option_compass:
        s.append('Compass')
    if a.option_country:
        s.append('Country')
    if a.option_error:
        s.append('Err')
    if a.option_expert:
        s.append('Expert')
    if a.option_network:
        s.append('Net')
    if a.option_size:
        s.append('Siz')
    if a.option_summary:
        s.append('Sum')
    if a.option_top_talker:
        s.append('TopTalk')
    if a.option_traffic_history:
        s.append('TrHist')
    if a.option_voice_video:
        s.append('VoiceVid')
    return ' '.join(s) if s else 'None'


def string_general_settings(g):
    s = []
    if g.option_file_age:
        s.append('Age')
    if g.option_continuous_capture:
        s.append('Continuous')
    if g.option_capture_to_disk:
        s.append('CTD')
    if g.option_deduplicate:
        s.append('DeDup')
    if g.option_priority_ctd:
        s.append('PriCTD')
    if g.option_intelligent_ctd:
        s.append('IntCTD')
    if g.option_slicing:
        s.append(f'Slice: {g.slice_length}')
    if g.option_start_capture:
        s.append('Start')
    if g.tap_timestamps > 0:
        tt = ['Default', 'Apcon', 'Anue', 'NetOptics', 'Gigamon']
        s.append(f'Timestamps:{tt[g.tap_timestamps]}')
    if g.option_timeline_stats:
        tl = []
        if g.option_timeline_app_stats:
            tl.append('App')
        if g.option_timeline_top_stats:
            tl.append('TopTalk')
        if g.option_timeline_voip_stats:
            tl.append('VoIP')
        s.append(f'TL:{",".join(tl)}')
    return ' '.join(s)


def string_indexing_settings(i):
    s = []
    if i.option_application:
        s.append('App')
    if i.option_country:
        s.append('Country')
    if i.option_ethernet:
        s.append('Eth')
    if i.option_ipv4:
        s.append('IPv4')
    if i.option_ipv6:
        s.append('IPv6')
    if i.option_mpls:
        s.append('MPLS')
    if i.option_port:
        s.append('Port')
    if i.option_protospec:
        s.append('ProtoSpec')
    if i.option_vlan:
        s.append('VLAN')
    return ' '.join(s) if s else 'None'


def string_voip_settings(v):
    return (f'Max Calls: {v.max_calls}, Notify: {v.option_notify}, '
            f'Severity: {v.severity}, Stop Analysis: {v.option_stop_analysis}')


def print_capture_template(ct, tab=20):
    if ct is None:
        print('No capture template')
        return
    if not isinstance(ct, CaptureTemplate):
        return
    print(str(ct))
    print(f'{"Adapter":>{tab}}: {string_adapter_settings(ct.adapter)}')
    print(f'{"Alarms":>{tab}}: {len(ct.alarms.alarms) if hasattr(ct, "alarms") else 0}')
    print(f'{"Analysis Modules":>{tab}}: '
          f'{len(ct.plugins.modules) if hasattr(ct, "plugins") else 0}')
    print(f'{"Analysis Settings":>{tab}}: '
          f'{string_analysis_settings(ct.analysis) if hasattr(ct, "analysis") else "0 enabled"}')
    print(f'{"Filter":>{tab}}: {"Yes" if ct.filter else "None"}')
    print(f'{"General":>{tab}}: {string_general_settings(ct.general)}')
    # print(f'{"Graphs":>{tab}}: {len(ct.graphs.graphs)}')
    print(f'{"Id":>{tab}}: {ct.id}')
    print(f'{"Indexing":>{tab}}: {string_indexing_settings(ct.indexing)}')
    print(f'{"Plugins Config":>{tab}}: {len(ct.plugins_config) if ct.plugins_config else 0}')
    print(f'{"Repeat Trigger":>{tab}}: None')
    # print(f'{"Start Trigger":>{tab}}: {ct.start_trigger.enabled}')
    print(f'{"Statistics":>{tab}} {ct.adapter.name}')
    # print(f'{"Stop Trigger":>{tab}}: {ct.statistics_output.enabled}')
    print(f'{"VoIP":>{tab}}: {string_voip_settings(ct.voip)}')
    if ct.general.option_spotlight_capture:
        print(f'{"Spotlight Capture":>{tab}}: Enabled')
    print()


def print_capture_template_list(ctl):
    if ctl:
        for ct in ctl:
            print_capture_template(ct)
    print()


def print_channel_scan_entry(e, tab=20):
    if e is None:
        print('No hardware options')
        return
    fmt_d = '%%%ds: %%d' % tab
    fmt_s = '%%%ds: %%s' % tab
    print(fmt_d % ('Channel Number', e.channel_number))
    print(fmt_d % ('Channel Frequency', e.channel_frequency))
    print(fmt_d % ('Channel Band', e.channel_band))
    print(fmt_d % ('Duration (ms)', e.duration))
    print(fmt_s % ('Enabled', e.enabled))
    print()


def print_conversation_stat(conversation_stat, tab=20):
    if conversation_stat is None:
        print('No conversation')
        return
    print(f'{"Bytes":>24}: {conversation_stat.bytes:,}')
    print(f'{"Destination":>24}: {conversation_stat.destination.address}')
    print(f'{"Duration":>24}: {format_duration(conversation_stat.duration)}')
    print(f'{"First Time":>24}: {conversation_stat.first_time}')
    print(f'{"Hierarchy":>24}: {conversation_stat.hierarchy}')
    print(f'{"Last Time":>24}: {conversation_stat.last_time}')
    print(f'{"Maximum Packet Size":>24}: {conversation_stat.maximum_packet_size:,}')
    print(f'{"Minimum Packet Size":>24}: {conversation_stat.minimum_packet_size:,}')
    print(f'{"Packets":>24}: {conversation_stat.packets:,}')
    print(f'{"Protocol":>24}: {conversation_stat.protocol}')
    print(f'{"Protocol Id":>24}: {conversation_stat.protocol_id}')
    print(f'{"Protocol Color":>24}: {conversation_stat.protocol_color}')
    print(f'{"Protocol Name":>24}: {conversation_stat.protocol_name}')
    print(f'{"Protocol Media":>24}: {conversation_stat.protocol_media_spec}')
    print(f'{"Source":>24}: {conversation_stat.source.address}')
    print()


def print_conversation_stats(conversation_stats, tab=20):
    if conversation_stats is None:
        print('No list of conversation stats')
        return
    print('Conversation Statistics')
    print(f'{"Duration":>20}: {format_duration(conversation_stats.duration)}')
    print(f'{"Reset Count":>20}: {conversation_stats.reset_count}')
    print(f'{"Time Limit":>20}: {conversation_stats.time_limit_reached}')
    print(f'{"Total Bytes":>20}: {conversation_stats.total_bytes:,}')
    print(f'{"Total Packets":>20}: {conversation_stats.total_packets:,}')
    print(f'{"Conversation Stats":>20}: {len(conversation_stats.conversation_stats)}')
    for stat in conversation_stats.conversation_stats:
        print_conversation_stat(stat, tab+4)
    print()


def print_country_stat(country_stat, tab=20):
    if country_stat is None:
        print('No country')
        return
    print(f'{"Country":>20}: {country_stat.name}')
    print(f'{"Bytes From":>24}: {country_stat.bytes_from:,}')
    print(f'{"Bytes To":>24}: {country_stat.bytes_to:,}')
    print(f'{"Code":>24}: {country_stat.code}')
    print(f'{"Duration":>24}: {format_duration(country_stat.duration)}')
    print(f'{"First Time From":>24}: {country_stat.first_time_from}')
    print(f'{"First Time To":>24}: {country_stat.first_time_to}')
    print(f'{"Last Time From":>24}: {country_stat.last_time_from}')
    print(f'{"Last Time To":>24}: {country_stat.last_time_to}')
    print(f'{"Packets From":>24}: {country_stat.packets_from:,}')
    print(f'{"Packets To":>24}: {country_stat.packets_to:,}')
    print()


def print_country_stats(country_stats, tab=20):
    if country_stats is None:
        print('No list of country stats')
        return
    print('Country Statistics')
    print(f'{"Duration":>20}: {format_duration(country_stats.duration)}')
    print(f'{"Total Bytes":>20}: {country_stats.total_bytes:,}')
    print(f'{"Total Packets":>20}: {country_stats.total_packets:,}')
    print(f'{"Country Stats":>20}: {len(country_stats.country_stats)}')
    for stat in country_stats.country_stats:
        print_country_stat(stat, tab+4)
    print()


def print_directory(d, tab=20):
    if d is None:
        print('No directory')
        return
    if d.parent:
        print(f'Directory: {d.name}')
        print(f'{"Parent":>{tab}}: {d.parent.name}')
    else:
        print('Directory: This is the Root directory.')
    if d.directory_list:
        print(f'{"Sub Directories":>{tab}}: {d.directory_list}')
    if d.file_list:
        print(f'{"Files":>{tab}}: {d.file_list}')
    print()


def print_capabilities(caps: Capabilities, class_names=None, cap_names=None, tab=20):
    if caps is None:
        print('No engine capabilities')
        return
    wrapper = TW(width=100, subsequent_indent=f'{" ":>{tab+2}}', break_on_hyphens=False)
    print('Engine Capabilities')
    if caps.maximum_capture_count is not None:
        print(f'{"Max Capture Count":>{tab}}: {caps.maximum_capture_count}')
    if isinstance(caps.administrator_default_list, list):
        print(f'{"Administrator Default":>{tab}}: '
              f'{".join(str(v) for v in caps.administrator_default_list)"}')
    if isinstance(caps.capability_list, list):
        new_ids = []
        for id in caps.capability_list:
            if id not in cap_names:
                new_ids.append(id)
        if new_ids:
            print('New Capabilities:')
            for id in new_ids:
                print(f'    {id}')
        if cap_names:
            name_list = [cap_names[cid] if cid in cap_names else f'{cid}'
                         for cid in caps.capability_list]
            print(f'{"Capability":>{tab}}: '
                  f'{wrapper.fill(", ".join(str(a) for a in name_list))}')
            for m in [n for n in name_list if '-' in n]:
                print(f'*** Missing capability name: {m}.')
        else:
            print(f'{"Capability":>{tab}}: '
                  f'{wrapper.fill(" ".join(str(a) for a in caps.capability_list))}')
    if isinstance(caps.packet_file_index_list, list):
        txt = '\n'.join(f'{" ":>{tab+2}}{a.id}: '
                        f'{a.name}' for a in caps.packet_file_index_list).strip()
        print(f'{"Packet File Index":>{tab}}: {txt}')
    if isinstance(caps.performance_item_list, list):
        txt = '\n'.join(f'{" ":>{tab+2}}{a.name}, Cost {a.cost}%, Limit {a.has_limit}'
                        for a in caps.performance_item_list).strip()
        print(f'{"Performance Item":>{tab}}: {txt}')
    if isinstance(caps.plugin_id_list, list):
        txt1 = wrapper.fill(" ".join(str(a) for a in caps.plugin_id_list))
        print(f'{"Plugin Id":>{tab}}: {txt1}')
    if isinstance(caps.plugin_information_list, list):
        txt = ('\n'.join(f'{" ":>{tab+2}}{a.name:<18} {a.version:<11}'
                         f'{" opt" if a.has_options else ""}'
                         f'{" ext" if a.has_extended_options else ""}'
                         f'{" sum" if a.has_packet_summary else ""}'
                         f'{" pkt" if a.has_process_packets else ""}'
                         f'{" sta" if a.has_summary_statistics else ""}'
                         f'{" adt" if a.is_adapter else ""}'
                         f'{" fil" if a.is_filter else ""}'
                         for a in caps.plugin_information_list).strip())
        print(f'{"Plugin Information":>{tab}}: {txt}')
    if isinstance(caps.policy_id_list, list):
        if class_names:
            name_list = [class_names[id] for id in class_names]
            print(f'{"User Policy Id":>{tab}}: '
                  f'{wrapper.fill(" ".join(name for name in name_list))}')
        else:
            print(f'{"User Policy Id":>{tab}}: '
                  f'{wrapper.fill(" ".join(str(a) for a in caps.policy_id_list))}')
    print()


def print_engine_settings(settings, tab=20, class_names=None, capability_names=None):
    if settings is None:
        print('No engine settings')
        return
    print('Engine Settings')
    print(f'{"Version":>{tab}}: {settings.version}')
    print(f'{"Type":>{tab}}: {settings.engine_type}')

    print(f'{"Is ACL Enabled":>{tab}}: {settings.is_acl_enabled}')
    print_access_control_list(settings.acl, tab, class_names)

    print(f'{"Capabilities":>{tab}}:{" None" if not settings.capabilities else ""}')
    if settings.capabilities:
        if capability_names:
            for i in settings.capabilities:
                print(f'{"":>{tab}} {i} : {capability_names[i]}')
        else:
            for i in settings.capabilities:
                print(f'{"":>{tab}} {i}')

    network = settings.network
    print(f'{"Network Settings:":>{tab}}')
    print(f'{"Agent Name":>{tab+4}}: {network.agent_name}')
    print(f'{"Connection Capacity":>{tab+4}}: {network.connection_capacity}')
    print(f'{"Connection Timeout":>{tab+4}}: {network.connection_timeout}')
    print(f'{"Data Root_Path":>{tab+4}}: {network.data_root_path}')
    print(f'{"IP Available":>{tab+4}}: {network.ip_available}')
    print(f'{"IP Selected":>{tab+4}}: {network.ip_selected}')
    print(f'{"Log_Records Adjustment":>{tab+4}}: {network.log_records_adjustment}')
    print(f'{"Log Records Maximum":>{tab+4}}: {network.log_records_maximum}')
    print(f'{"Port":>{tab+4}}: {network.port}')
    print(f'{"Alert Records Adjustment":>{tab+4}}: {network.security_alert_records_adjustment}')
    print(f'{"Alert Records Maximum":>{tab+4}}: {network.security_alert_records_maximum}')
    print(f'{"Event Records Adjustment":>{tab+4}}: {network.security_event_records_adjustment}')
    print(f'{"Event Records Maximum":>{tab+4}}: {network.security_event_records_maximum}')
    print(f'{"Is Auto Restart":>{tab+4}}: {network.is_auto_restart}')
    print(f'{"Is UDP Discovery":>{tab+4}}: {network.is_udp_discovery}')

    print(f'{"Runtime Locks:":>{tab}}')
    locks = settings.runtime_locks
    print(f'{"Adapter Locks":>{tab+4}}: '
          f'[{", ".join(str(v.id)+" "+str(v.user) for v in locks.adapter_lock_list)}]')
    print(f'{"Capture Locks":>{tab+4}}: '
          f'[{", ".join(str(v.id)+" "+str(v.user) for v in locks.capture_lock_list)}]')
    print(f'{" Filters Lock":>{tab+4}}: {locks.filters_lock}')
    print(f'{"Session Locks":>{tab+4}}: ['
          f'{", ".join("Max: "+str(v.maximum)+", "+str(v.user) for v in locks.session_lock_list)}]')

    security = settings.security
    print(f'{"Security Settings":>{tab}}: Use Auth Servers: {security.is_authentication_servers}')
    print(f'{"Admin Password":>{tab+4}}: {security.admin_password}')
    print(f'{"Syslog Destination":>{tab+4}}: {security.auditing_syslog_destination}')
    print(f'{"Authentication":>{tab+4}}: {security.authentication}')
    print(f'{"Compressioin Threshold":>{tab+4}}: {security.compression_threshold}')
    print(f'{"Radius":>{tab+4}}: {security.radius}')
    print(f'{"SSL Certificate":>{tab+4}}: {security.ssl_certificate}')
    print(f'{"Tacas+":>{tab+4}}: {security.tacas_plus}')
    print(f'{"User Password":>{tab+4}}: {security.user_password}')
    print(f'{"Is Auditing":>{tab+4}}: {security.is_auditing}')
    print(f'{"Is Auditing Syslog":>{tab+4}}: {security.is_auditing_syslog}')
    print(f'{"Is Auth Servers":>{tab+4}}: {security.is_authentication_servers}')
    print(f'{"Is Compression":>{tab+4}}: {security.is_compression}')
    print(f'{"Is Encrypted":>{tab+4}}: {security.is_encrypted}')
    print(f'{"Is SSL":>{tab+4}}: {security.is_ssl}')
    print(f'{"Use Encryption":>{tab+4}}: {security.use_encryption}')
    print(f'{"Use Impersonation":>{tab+4}}: {security.use_impersonation}')

    print(f'{"Auth Servers":>{tab+4}}: {len(security.authentication_server_list)}')
    for i in security.authentication_server_list:
        print(f'{"":>{tab}} {i}')
    print()


def print_engine_status(status, tab=20):
    if status is None:
        print('No engine status')
        return

    print(f'Engine Status: {status.name}')
    print(f'{"Adapter Count":>{tab}}: {status.adapter_count}')
    if status.address:
        print(f'{"Address":>{tab}}: {status.address}')
    if status.ip_address:
        print(f'{"IP Address":>{tab}}: {status.ip_address}')
    print(f'{"Alarm Count":>{tab}}: {status.alarm_count}')
    print(f'{"Alarm Modification Time":>{tab}}: {status.alarm_modification_time or ""}')
    print(f'{"Capture Count":>{tab}}: {status.capture_count}')
    print(f'{"Capture Info List":>{tab}}:')
    for ci in status.capture_info_list:
        print(f'{" ":>{tab-4}}{ci.id.format()}: allocated: {ci.allocated:,}, used: {ci.used:,}')
    print(f'{"Capture Session Count":>{tab}}: {status.capture_session_count}')
    print(f'{"CPU Count":>{tab}}: {status.cpu_count}')
    print(f'{"CPU Type":>{tab}}: {status.cpu_type}')
    print(f'{"custom_settings":>{tab}}: {status.custom_settings}')
    print(f'{"Data Directory":>{tab}}: {status.data_directory}')
    print(f'{"Data Drive Format":>{tab}}: {status.data_drive_format}')
    print(f'{"Decryption Key Count":>{tab}}: {status.decryption_key_count}')
    print(f'{"disk_reserved_space":>{tab}}: {status.disk_reserved_space:,}')
    print(f'{"Engine Type":>{tab}}: {status.engine_type}')
    print(f'{"File Count":>{tab}}: {status.file_count:,}')
    print(f'{"File Version":>{tab}}: {status.file_version}')
    print(f'{"Filter Count":>{tab}}: {status.filter_count:,}')
    print(f'{"Filter Modification Time":>{tab}}: {status.filters_modification_time or ""}')
    print(f'{"Forensic Search Count":>{tab}}: {status.forensic_search_count:,}')
    print(f'{"Forensic Search Reserved Space":>{tab}}: {status.forensic_search_reserved_space:,}')
    print(f'{"Graph Count":>{tab}}: {status.graph_count:,}')
    print(f'{"Hardware Profiile Count":>{tab}}: {status.hardware_profile_count:,}')
    print(f'{"Hardware Type":>{tab}}: {status.hardware_type}')
    print(f'{"Host":>{tab}}: {status.host}, Port: {status.port}')
    print(f'{"IP Address":>{tab}}: {status.ip_address}')
    print(f'{"IPMI Address":>{tab}}: {status.ipmi_address}')
    print(f'{"Is License Expired":>{tab}}: {status.is_license_expired}')
    print(f'{"Is Licensed":>{tab}}: {status.is_licensed}')
    print(f'{"Is Native Protospecs Enabled":>{tab}}: {status.is_native_protospecs_enabled}')
    print(f'{"License Expiration Date":>{tab}}: {status.license_expiration_date}')
    print(f'{"License Type":>{tab}}: {status.license_type}')
    print(f'{"Log Total Count":>{tab}}: {status.log_total_count:,}')
    print(f'{"Physical Memory Available":>{tab}}: {status.memory_available_physical:,}')
    print(f'{"Memory Total Physical":>{tab}}: {status.memory_total_physical:,}')
    print(f'{"Modification Time":>{tab}}: {status.modification_time or ""}')
    print(f'{"Name Table Count":>{tab}}: {status.name_table_count:,}')
    print(f'{"Name Table Modification Time":>{tab}}: {status.name_table_modification_time or ""}')
    print(f'{"Notification Count":>{tab}}: {status.notification_count:,}')
    print(f'{"Notifications Modification Time":>{tab}}: '
          f'{status.notifications_modification_time or ""}')
    print(f'{"Operating System":>{tab}}: {status.operating_system}')
    print(f'{"OS":>{tab}}: {status.os}')
    print(f'{"Platform":>{tab}}: {status.platform}')
    print(f'{"Product Version":>{tab}}: {status.product_version}')
    print(f'{"Protocol Translation Count":>{tab}}: {status.protocol_translation_count:,}')
    print(f'{"Protospecs Version":>{tab}}: {status.protospecs_version}')
    print(f'{"Security Events Total Count":>{tab}}: {status.security_events_total_count:,}')
    print(f'{"Serial Number":>{tab}}: {status.serial_number}')
    print(f'{"Total Storage Space":>{tab}}: {status.storage_total:,}')
    print(f'{"Storage Space Used":>{tab}}: {status.storage_used:,}')
    print(f'{"Storage Space Available":>{tab}}: {status.storage_available:,}')
    print(f'{"Time":>{tab}}: {status.time}')
    print(f'{"Time Zone Bias":>{tab}}: {status.time_zone_bias}')
    print(f'{"Uptime":>{tab}}: {format_duration(status.uptime)}')
    print(f'{"User_Domain":>{tab}}: {status.user_domain}')
    print(f'{"User_Id":>{tab}}: {status.user_id}')
    print(f'{"User_Name":>{tab}}: {status.user_name}')
    print()


def print_error_stat(error_stat, tab=20):
    if error_stat is None:
        print('No error')
        return
    print(f'{"Error Category":>{tab}}: {error_stat.category}')
    print(f'{"Packets":>{tab}}: {error_stat.packets:,}')
    print(f'{"Supported":>{tab}}: {error_stat.supported}')
    print()


def print_error_stats(error_stats, tab=20):
    if error_stats is None:
        print('No list of error stats')
        return
    print('Error Statistics')
    print(f'{"Last Value":>{tab}}: {error_stats.last_value:,}')
    for stat in error_stats.error_stats:
        print_error_stat(stat, tab+4)
    print()


def print_event_log_entry(e, tab=20, verbose=True):
    if e is None:
        print('No Event Log Entry')
        return
    print(f'{"Index":>{tab}}: {e.index}')
    if verbose:
        print(f'{"Message":>{tab}}: {e.message}')
        print(f'{"Severity":>{tab}}: {e.severity}')
        print(f'{"Timestamp":>{tab}} {e.timestamp}')
        if e.capture_id:
            print(f'{"Capture Id":>{tab}}: {str(e.capture_id)}')
        if e.source_id:
            print(f'{"Source Id":>{tab}}: {str(e.source_id)}')
        if e.source_key:
            print(f'{"Source Key":>{tab}}: {str(e.source_key)}')
        print()


def print_event_log(el, tab=20):
    if el is None:
        print('No Event Log')
        return
    print(str(el))
    print(f'{"Count":>{tab}}: {el.count}')
    print(f'{"Informational":>{tab}}: {el.informational}')
    print(f'{"Minor":>{tab}}: {el.minor}')
    print(f'{"Major":>{tab}}: {el.major}')
    print(f'{"Severe":>{tab}}: {el.severe}')
    print(f'{"First":>{tab}}: {el.first}')
    print(f'{"Last":>{tab}}: {el.last}')
    for e in el.entries:
        print_event_log_entry(e, (tab+4))


def print_event_log_indexes(el, tab=20):
    if el is None:
        print('No Event Log')
        return
    print(str(el))
    print(f'{"Count":>{tab}}: {el.count}')
    print(f'{"Informational":>{tab}}: {el.informational}')
    print(f'{"Minor":>{tab}}: {el.minor}')
    print(f'{"Major":>{tab}}: {el.major}')
    print(f'{"Severe":>{tab}}: {el.severe}')
    print(f'{"First":>{tab}}: {el.first}')
    print(f'{"Last":>{tab}}: {el.last}')
    for e in el.entries:
        print_event_log_entry(e, (tab+4), False)


def print_expert_result(er, tab=20):
    if er is None:
        print('No expert result')
        return
    fmt_d = '%%%ds: %%d' % tab
    fmt_s = '%%%ds: %%s' % tab
    print('Expert Result: %s' % er.table)
    print(fmt_d % ('Rows', len(er.rows)))
    print(fmt_d % ('First Index', er.first_index))
    print(fmt_s % ('Time', er.time))
    cols = min(len(er.columns), 4)
    print(fmt_s % ('', '\t'.join(er.columns[:cols])))
    for row in er.rows:
        print(fmt_s % ('', ' '.join(str(i[1]) for i in row.items()[:cols])))


def print_expert_result_list(erl):
    if erl:
        for er in erl:
            print_expert_result(er)
    print()


def print_expert_description(ed=ExpertDescription, tab=20):
    if not ed:
        return
    print(f'{"Name":>{tab}}: {ed.name}, Message: {ed.message}')
    print(f'{"Id":>{tab+8}}: {ed.id}')
    print(f'{"Has":>{tab+8}}: '
          f'Conf: {"T" if ed.has_configure else "F"}, '
          f'MinSamp: {"T" if ed.has_minimum_sample_period else "F"}, '
          f'Sens: {"T" if ed.has_sensitivity else "F"}, '
          f'Val: {"T" if ed.has_value else "F"}, '
          f'Assist: {"T" if ed.has_value_assist else "F"}')
    print(f'{"Group":>{tab+8}}: {ed.group if ed.group else "-"}, '
          f'SubGroup: {ed.sub_group if ed.sub_group else "-"}')
    print(f'{"Protocol Layer":>{tab+8}}: {ed.layer}, Problem: {ed.problem_id}')
    print(f'{"Value":>{tab+8}}: Min: {ed.value_minimum}, Max: {ed.value_maximum}, '
          f'Units: {ed.value_units if ed.value_units else "-"}')
    print(f'{"Value Assist":>{tab+8}}: L: {ed.value_assist_left}, R: {ed.value_assist_right}, '
          f'Format: {ed.value_display_format if ed.value_display_format else "-"}, '
          f'Mult: {ed.value_display_multiplier}, Log: {ed.has_value_assist_log_scale}')
    print(f'{"Sample Period":>{tab+8}}: Min: {ed.minimum_sample_period_minimum}, '
          f'Max: {ed.minimum_sample_period_maximum}, '
          f'Units: {ed.minimum_sample_period_units}')
    print()


def print_expert_description_list(edl, tab=20):
    if not isinstance(edl, list):
        return
    print(f'{"Description List":>{tab}}:')
    for d in edl:
        print_expert_description(d, tab)


def print_protocol_name_list(pl, tab=20):
    if not pl:
        print('No Protocol Name list')
        return
    print('Protocol Name List:')
    for p in pl:
        print(f'{"Id":>{tab}}: {p.id}, Name: {p.name}')
    print()


def print_wireless_policy(wp, tab=20):
    print(f'{"Accept":>{tab}}: Auth: {wp.accept_authentication_list}, '
          f'Chan: {wp.accept_channel_family_list}, '
          f'Enc: {wp.accept_encryption_protocol_list}, '
          f'ESSID: {wp.accept_essid_name_list}')
    protocol_list = wp.authentication_protocol_list
    print(f'{"Auth Protocols":>{tab}}: '
          f'{" ".join(f"{p.protocol.label()}, {p.enabled}" for p in protocol_list)}')
    print(f'{"Encryption Protocols":>{tab}}: '
          f'{" ".join(f"{p.protocol.label()}, {p.enabled}" for p in wp.encryption_protocol_list)}')
    print(f'{"ESSID":>{tab}}: '
          f'{" ".join(f"{p.name}, {p.enabled}" for p in wp.essid_name_list)}')
    ids = wp.vendor_id_list
    print(f'{"Vendor":>{tab}}: '
          f'{" ".join(f"{p.address}, AP: {p.is_access_point}, Cli: {p.is_client}" for p in ids)}')


def print_expert_settings(es, tab=20):
    print('Expert Settings:')
    print(f'{"Maximum Streams":>{tab}}: {es.maximum_stream_count}')
    print_wireless_policy(es.wireless_policy, tab)
    print()


def print_expert_event(ev, tab=20):
    print(f'{"Expert Event":>{tab}}: {ev.name}')
    if ev.default:
        print(f'{"Default":>{tab + 4}}: {ev.default}')
    lst = [(k, v) for k, v in ev.label_map.items()]
    lst.sort()
    for k, v in lst:
        print(f'{k:>{tab + 4}}: {v}')


def print_expert_event_list(lst, tab=20):
    if not lst:
        print('No Expert Event List')
        return
    print('Expert Event Label List')
    for e in lst:
        print_expert_event(e, tab)


def print_expert_preferences(ep, tab=20):
    if ep is None:
        print('No expert preferences')
        return
    print('Expert Preferences')
    print_expert_description_list(ep.description_list, tab)
    print_protocol_name_list(ep.protocol_name_list, tab)
    print_expert_settings(ep.settings, tab)
    if ep.default_settings:
        print_expert_settings(ep.default_settings, tab)
    print_expert_event_list(ep.event_label_list, tab)
    print()


def print_file_adapter(fa, tab=20):
    if fa is None:
        print('No file adapter')
        return
    fmt_d = '%%%ds: %%d' % tab
    fmt_s = '%%%ds: %%s' % tab
    print('File Adapter: %s' % fa.filename)
    print(fmt_s % ('Limit', fa.limit))
    print(fmt_d % ('Mode', fa.mode))
    print(fmt_d % ('Speed', fa.speed))


def print_filter(f, tab=20):
    if f is None:
        print('No filter')
        return
    print('Filter: %s' % f.name)
    print(f'{"Id":>{tab}}: {f.id}')
    print(f'{"Comment":>{tab}}: {f.comment}')
    print(f'{"Created":>{tab}}: {f.created or ""}')
    print(f'{"Modified":>{tab}}: {f.modified or ""}')
    text = f.criteria.to_string(int(tab/4))
    print(f'{"Criteria":>{tab}}: {text.lstrip()}')


def print_filter_list(fl):
    if fl:
        for f in fl:
            print_filter(f)
    print()


def print_forensic_file(ff, tab=20):
    if ff is None:
        print('No forensic file')
        return
    fmt_d = '%%%ds: %%d' % tab
    fmt_dd = '%%%ds: %%d, %%s: %%d' % tab
    fmt_s = '%%%ds: %%s' % tab
    fmt_ss = '%%%ds: %%s, %%s: %%s' % tab
    print('Forensic File: %s' % ff.name)
    print(fmt_s % ('Path', ff.path))
    print(fmt_d % ('Status', ff.status))
    print(fmt_d % ('Index', ff.file_index))
    print(fmt_s % ('Session Id', ff.session_id))
    print(fmt_d % ('Size', ff.size))
    print(fmt_dd % ('Media Type', ff.media_type, 'Sub Type', ff.media_sub_type))
    print(fmt_ss % ('Adapter', ff.adapter_name, 'Address', ff.adapter_address))
    print(fmt_d % ('Link Speed', ff.link_speed))
    print(fmt_s % ('Capture', ff.capture_name))
    print(fmt_s % ('Capture Id', ff.capture_id))
    print(fmt_d % ('Count', ff.packet_count))
    print(fmt_d % ('Dropped', ff.dropped_packet_count))
    print(fmt_s % ('Start', ff.start_time or ""))
    print(fmt_s % ('End', (ff.end_time or "- - -")))
    print(fmt_d % ('Timezone Bias', ff.time_zone_bias))
    print()


def print_forensic_file_list(ffl):
    if ffl:
        for ff in ffl:
            print_forensic_file(ff)
    print()


def print_forensic_search(fs, tab=20):
    if fs is None:
        print('No forensic search')
        return
    fmt_d = '%%%ds: %%d' % tab
    fmt_dd = '%%%ds: %%d, %%s: %%d' % tab
    fmt_s = '%%%ds: %%s' % tab
    print('Forensic Search: %s' % fs.name)
    print(fmt_s % ('Id', fs.id))
    print(fmt_s % ('Adapter', fs.adapter))
    print(fmt_s % ('Capture Name', fs.capture_name))
    print(fmt_s % ('Session Id', fs.session_id))
    print(fmt_s % ('Creator', fs.creator))
    print(fmt_s % ('Creator SID', fs.creator_sid))
    print(fmt_s % ('Duration', format_duration(fs.duration)))
    print(fmt_d % ('Status', fs.status))
    print(fmt_d % ('First Packet', fs.first_packet))
    print(fmt_d % ('Link Speed', fs.link_speed))
    print(fmt_s % ('Load Progress', fs.load_progress))
    print(fmt_s % ('Load Percent', fs.load_percent))
    print(fmt_dd % ('Media Info: Type:', fs.media_information.media_type, 'Subtype',
                    fs.media_information.media_sub_type))
    print(fmt_dd % ('            Domain:', fs.media_information.domain, 'Link Speed',
                    fs.media_information.link_speed))
    print(fmt_d % ('Media Type', fs.media_type))
    print(fmt_d % ('Media Sub Type', fs.media_sub_type))
    print(fmt_s % ('Modified By', fs.modified_by))
    print(fmt_s % ('Modification Type', fs.modification_type))
    print(fmt_d % ('Open Result', fs.open_result))
    print(fmt_d % ('Packet Count', fs.packet_count))
    print(fmt_d % ('Percent Progress', fs.percent_progress))
    print(fmt_d % ('Process % Progress', fs.process_percent_progress))
    print(fmt_s % ('Process Progress', fs.process_progress))
    print(fmt_s % ('Progress', fs.progress))
    print(fmt_s % ('Start Time', fs.start_time or ""))
    print(fmt_s % ('Stop Time', fs.stop_time or ""))
    print(fmt_s % ('Option Expert', fs.option_expert))
    print(fmt_s % ('Option Graphs', fs.option_graphs))
    print(fmt_s % ('Option Indexing', fs.option_indexing))
    print(fmt_s % ('Option Log', fs.option_log))
    print(fmt_s % ('Option Packet Buffer', fs.option_packet_buffer))
    print(fmt_s % ('Option Voice', fs.option_voice))
    print(fmt_s % ('Option Web', fs.option_web))
    print()


def print_forensic_search_list(fsl):
    if fsl:
        for fs in fsl:
            print_forensic_search(fs)
    print()


def print_forensic_template(ft, tab=25):
    if ft is None:
        print('No forensic template')
        return
    fmt_d = '%%%ds: %%d' % tab
    fmt_s = '%%%ds: %%s' % tab
    print('Forensic Template: %s' % ft.name)
    print(fmt_s % ('Id', ft.session_id))
    print(fmt_s % ('Adapter', ft.adapter_name))
    print(fmt_s % ('Capture', ft.capture_name))
    print(fmt_s % ('End Time', ft.end_time or ""))
    print(fmt_s % ('File Name', ft.filename))
    print(fmt_d % ('Filter Mode', ft.filter_mode))
    print(fmt_d % ('Graph Interval', ft.graph_interval))
    print(fmt_d % ('Limit', ft.limit))
    print(fmt_d % ('Limit Size', ft.limit_size))
    print(fmt_d % ('Media Type', ft.media_type))
    print(fmt_d % ('Media Sub Type', ft.media_sub_type))
    print(fmt_s % ('Start Time', ft.start_time or ""))
    print(fmt_s % ('Option Error', ft.option_error))
    print(fmt_s % ('Option Expert', ft.option_expert))
    print(fmt_s % ('Option Graphs', ft.option_graphs))
    print(fmt_s % ('Option Histort', ft.option_history))
    print(fmt_s % ('Option Log', ft.option_log))
    print(fmt_s % ('Option Network', ft.option_network))
    print(fmt_s % ('Option Packets', ft.option_packets))
    print(fmt_s % ('Option Plugins', ft.option_plugins))
    print(fmt_s % ('Option Size', ft.option_size))
    print(fmt_s % ('Option Summary', ft.option_summary))
    print(fmt_s % ('Option Top Talkers', ft.option_top_talkers))
    print(fmt_s % ('Option Voice', ft.option_voice))
    print(fmt_s % ('Option Web', ft.option_web))
    print(fmt_s % ('Option Wireless Channel', ft.option_wireless_channel))
    print(fmt_s % ('Option Wireless Node', ft.option_wireless_node))
    if ft.node_limits is not None:
        print(fmt_s % ('Option Node Limits', ft.is_node_limits_enabled()))
    if ft.protocol_limits is not None:
        print(fmt_s % ('Option Protocol Limits', ft.is_protocol_limits_enabled()))
    if ft.is_node_protocol_detail_limits_enabled():
        print(fmt_s % ('Option Node/Protocol Detail Limits',
                       ft.is_node_protocol_detail_limits_enabled()))
    if ft.files is not None:
        for f in ft.files:
            print(fmt_s % ('File', f))
    if ft.filter:
        print(ft.filter.to_string(0))


def print_forensic_template_list(ftl):
    if ftl:
        for ft in ftl:
            print_forensic_template(ft)
    print()


def print_graph_template(gt, tab=20):
    if gt is None:
        print('No graph template')
        return
    print(f'{"Name":>{tab}}: {gt.name}')
    print(f'{"Id":>{tab}}: {gt.id}')
    print(f'{"Graph Id":>{tab}}: {gt.graph_id}')
    print()


def print_graph_template_list(gtl):
    if gtl:
        for gt in gtl:
            print_graph_template(gt)
    print()


def print_history_stat(history_stat, tab=20):
    if history_stat is None:
        print('No history')
        return
    print(f'{"Interval":>{tab}}: {history_stat.interval}')
    print(f'{"Start Time":>{tab}}: {history_stat.start_time}')
    print(f'{"Samples":>{tab}}: {len(history_stat.sample_list):,}')
    for sample in history_stat.sample_list:
        print(f'{sample:{tab+4}}')
    print()


def print_history_stats(history_stats, tab=20):
    if history_stats is None:
        print('No list of history stats')
        return
    print('History Statistics')
    for stat in history_stats.history_stats:
        print_history_stat(stat, tab+4)
    print()


def print_wireless_hardware_options(w, scan=True, tab=20):
    if w is None:
        print('No wireless hardware options')
        return
    fmt_d = '%%%ds: %%d' % tab
    fmt_s = '%%%ds: %%s' % tab
    print(fmt_d % ('Channel Number', w.channel_number))
    print(fmt_d % ('Channel Frequency', w.channel_frequency))
    print(fmt_d % ('Channel Band', w.channel_band))
    print(fmt_s % ('ESSID', w.essid))
    print(fmt_s % ('BSSID', w.bssid))
    if w.key_set:
        ks = w.key_set
        if ks.name:
            print(fmt_s % ('Name', ks.name))
        print(fmt_d % ('Algorithm', ks.algorithm))
        for k in ks.keys:
            print(fmt_s % ('Key', k[1]))
    if scan and w.channel_scanning:
        print(fmt_d % ('Channel Scanning Entries: ', len(w.channel_scanning)))
        for e in w.channel_scanning:
            print_channel_scan_entry(e, tab)
    print()


def print_hardware_options(hwo, scan=True, tab=20):
    if hwo is None:
        print('No hardware options')
        return
    fmt_d = '%%%ds: %%d' % tab
    fmt_s = '%%%ds: %%s' % tab
    print('Hardware Options: %s' % hwo.name)
    print(fmt_s % ('Id', hwo.id))
    print(fmt_s % ('Comment', hwo.comment))
    print(fmt_d % ('Color', hwo.color))
    print(fmt_s % ('Created', hwo.created))
    print(fmt_s % ('Modified', hwo.modified))
    # if isinstance(hwo, HardwareOp.WirelessHardwareOptions):
    #     print_wireless_hardware_options(hwo, scan, tab)
    print()


def print_hardware_options_list(hwol, scan=True):
    if hwol:
        for hwo in hwol:
            print_hardware_options(hwo, scan)
    print()


def print_liveflow_configuration(lf, tab=20):
    if lf is None:
        print(('No LiveFlow Configuration'))
        return
    print('LiveFlow Configuration')
    print(f'{"Version":>{tab}}: {lf.version}')
    print(f'{"Output":>{tab}}:')
    if lf.output is not None:
        print(f'{"Records":>{tab}}: {len(lf.output.record_list)}')
        for record in lf.output.record_list:
            print(f'{"":>{tab+4}}{record}')
    print(f'{"Preferences":>{tab}}:')
    print(f'{"debug_logging":>{tab+4}}: {lf.preferences.debug_logging}')
    print(f'{"decryption_enabled":>{tab+4}}: {lf.preferences.decryption_enabled}')
    print(f'{"dns_analysis":>{tab+4}}: {lf.preferences.dns_analysis}')
    print(f'{"enforce_tcp_3way_handshake":>{tab+4}}: {lf.preferences.enforce_tcp_3way_handshake}')
    print(f'{"flow_id":>{tab+4}}: {lf.preferences.flow_id}')
    print(f'{"hashtable_size":>{tab+4}}: {lf.preferences.hashtable_size}')
    print(f'{"hostname_analysis":>{tab+4}}: {lf.preferences.hostname_analysis}')
    print(f'{"https_port":>{tab+4}}: {lf.preferences.https_port}')
    print(f'{"ipfix":>{tab+4}}: {lf.preferences.ipfix}')
    print(f'{"latency_enabled":>{tab+4}}: {lf.preferences.latency_enabled}')
    print(f'{"quality_enabled":>{tab+4}}: {lf.preferences.quality_enabled}')
    print(f'{"retransmissions_enabled":>{tab+4}}: {lf.preferences.retransmissions_enabled}')
    print(f'{"rtp_enabled":>{tab+4}}: {lf.preferences.rtp_enabled}')
    print(f'{"rtp_packets_disabled":>{tab+4}}: {lf.preferences.rtp_packets_disabled}')
    print(f'{"signaling_packet_window":>{tab+4}}: {lf.preferences.signaling_packet_window}')
    print(f'{"tcp_handshake_timeout":>{tab+4}}: {lf.preferences.tcp_handshake_timeout}')
    print(f'{"tcp_orphan_timeout":>{tab+4}}: {lf.preferences.tcp_orphan_timeout}')
    print(f'{"tcp_packets_disabled":>{tab+4}}: {lf.preferences.tcp_packets_disabled}')
    print(f'{"tcp_post_close_timeout":>{tab+4}}: {lf.preferences.tcp_post_close_timeout}')
    print(f'{"tcp_wait_timeout":>{tab+4}}: {lf.preferences.tcp_wait_timeout}')
    print(f'{"tls_analysis":>{tab+4}}: {lf.preferences.tls_analysis}')
    print(f'{"tls_packet_window":>{tab+4}}: {lf.preferences.tls_packet_window}')
    print(f'{"udp_packets_disabled":>{tab+4}}: {lf.preferences.udp_packets_disabled}')
    print(f'{"udp_wait_timeout":>{tab+4}}: {lf.preferences.udp_wait_timeout}')
    print(f'{"vlan_enabled":>{tab+4}}: {lf.preferences.vlan_enabled}')
    print(f'{"voip_quality_percent":>{tab+4}}: {lf.preferences.voip_quality_percent}')
    print(f'{"web_enabled":>{tab+4}}: {lf.preferences.web_enabled}')


def print_liveflow_context(lf, tab=20):
    if lf is None:
        print(('No LiveFlow Context'))
        return
    print('LiveFlow Context')
    if lf.analysis:
        print(f'{"Analysis":>{tab}}:')
        print(f'{"decryption_enabled":>{tab+4}}: {lf.analysis.decryption_enabled}')
        print(f'{"dhcp_enabled":>{tab+4}}: {lf.analysis.dhcp_enabled}')
        print(f'{"dns_enabled":>{tab+4}}: {lf.analysis.dns_enabled}')
        print(f'{"eta_distribution_entropy_enabled":>{tab+4}}: '
              f'{lf.analysis.eta_distribution_entropy_enabled}')
        print(f'{"hostname_enabled":>{tab+4}}: {lf.analysis.hostname_enabled}')
        print(f'{"latency_enabled":>{tab+4}}: {lf.analysis.latency_enabled}')
        print(f'{"mpls_vlan_vxlan_enabled":>{tab+4}}: {lf.analysis.mpls_vlan_vxlan_enabled}')
        print(f'{"rtp_enabled":>{tab+4}}: {lf.analysis.rtp_enabled}')
        print(f'{"tcp_3way_handshake_enabled":>{tab+4}}: {lf.analysis.tcp_3way_handshake_enabled}')
        print(f'{"tcp_quality_enabled":>{tab+4}}: {lf.analysis.tcp_quality_enabled}')
        print(f'{"tcp_retransmissions_enabled":>{tab+4}}: '
              f'{lf.analysis.tcp_retransmissions_enabled}')
        print(f'{"tls_enabled":>{tab+4}}: {lf.analysis.tls_enabled}')
        print(f'{"web_enabled":>{tab+4}}: {lf.analysis.web_enabled}')
    if lf.license:
        print(f'{"License":>{tab}}:')
        print(f'{"active_flow_count_limit":>{tab+4}}: {lf.license.active_flow_count_limit}')
        print(f'{"custom_settings_count":>{tab+4}}: {lf.license.custom_settings_count}')
        print(f'{"liveflow_enabled":>{tab+4}}: {lf.license.liveflow_enabled}')
        print(f'{"threateye_enabled":>{tab+4}}: {lf.license.threateye_enabled}')
    if lf.output:
        print(f'{"Output":>{tab}}:')
        print(f'{"avc_enabled":>{tab+4}}: {lf.output.avc_enabled}')
        print(f'{"sna_enabled":>{tab+4}}: {lf.output.sna_enabled}')
        print(f'{"financial_services_enabled":>{tab+4}}: {lf.output.financial_services_enabled}')
        print(f'{"fnf_enabled":>{tab+4}}: {lf.output.fnf_enabled}')
        print(f'{"medianet_enabled":>{tab+4}}: {lf.output.medianet_enabled}')
        print(f'{"platform_enabled":>{tab+4}}: {lf.output.platform_enabled}')
        print(f'{"signaling_dn_enabled":>{tab+4}}: {lf.output.signaling_dn_enabled}')
        print(f'{"threateye_enabled":>{tab+4}}: {lf.output.threateye_enabled}')
    print(f'{"target_count":>{tab}}: {lf.target_count}')


def print_liveflow_status(lf, tab=20):
    if lf is None:
        print(('No LiveFlow Status'))
        return
    print('LiveFlow Status')
    for k, v in lf.__dict__.items():
        print(f'{k:>{tab + 12}}: {v}')


def print_media_info(mi, tab=20):
    if mi is None:
        print(('No media information'))
        return
    fmt_d = '%%%ds: %%d' % tab
    print(fmt_d % ('Media Type', mi.media_type))
    print(fmt_d % ('Media Subtype', mi.media_sub_type))
    print(fmt_d % ('Domain', mi.domain))
    print(fmt_d % ('Link Speed', mi.link_speed))
    print()


def print_name_table(nt, tab=20):
    if nt:
        print('NameTable:')
        print(f'{"Last Modified":>{tab}}: {nt.modified}')
        print('Name List:')
        tab += 4
        for n in nt.name_list:
            print(f'{"Name":>{tab}}: {n.name}')
            print(f'{"Entry":>{tab}}: {n.entry}')
            print(f'{"Entry Type":>{tab}}: {n.entry_type}')
            print(f'{"Group":>{tab}}: {n.group}')
            print(f'{"Modified":>{tab}}: {n.modified}')
            print(f'{"Used":>{tab}}: {n.used}')
            print(f'{"Color":>{tab}}: {n.color}')
            print()
    else:
        print('No Name Table.')


def print_channel_stat(channel_stat, tab=20):
    if channel_stat is None:
        print('No network statistic')
        return
        print(f'{"Time":>32}: {channel_stat.time}')
        print(f'{"Broadcast Bytes":>36}: {channel_stat.broadcast_bytes:,}')
        print(f'{"Broadcast Packets":>36}: {channel_stat.broadcast_packets:,}')
        print(f'{"Multicast Bytes":>36}: {channel_stat.multicast_bytes:,}')
        print(f'{"Multicast Packets":>36}: {channel_stat.multicast_packets:,}')
        print(f'{"Total Bytes":>36}: {channel_stat.total_bytes:,}')
        print(f'{"Total Packets":>36}: {channel_stat.total_packets:,}')
        print()


def print_channel_stats(channel_stats, tab=20):
    if channel_stats is None:
        print('No network channel statistics')
        return
    print(f'{"Channel":>24}: {channel_stats.channel:,}')
    print(f'{"Broadcast Bytes":>28}: {channel_stats.broadcast_bytes:,}')
    print(f'{"Broadcast Packets":>28}: {channel_stats.broadcast_packets:,}')
    print(f'{"Multicast Bytes":>28}: {channel_stats.multicast_bytes:,}')
    print(f'{"Multicast Packets":>28}: {channel_stats.multicast_packets:,}')
    print(f'{"Total Bytes":>28}: {channel_stats.total_bytes:,}')
    print(f'{"Total Packets":>28}: {channel_stats.total_packets:,}')
    print(f'{"Channel Stats":>28}: {len(channel_stats.channel_stats)}')
    for stat in channel_stats.channel_stats:
        print(f'{"Time":>32}: {stat.time}')
        print(f'{"Broadcast Bytes":>36}: {stat.broadcast_bytes:,}')
        print(f'{"Broadcast Packets":>36}: {stat.broadcast_packets:,}')
        print(f'{"Multicast Bytes":>36}: {stat.multicast_bytes:,}')
        print(f'{"Multicast Packets":>36}: {stat.multicast_packets:,}')
        print(f'{"Total Bytes":>36}: {stat.total_bytes:,}')
        print(f'{"Total Packets":>36}: {stat.total_packets:,}')
        print()


def print_network_stat(network_stat, tab=20):
    if network_stat is None:
        print('No network statistic')
        return
    print(f'{"Time":>24}: {network_stat.time}')
    print(f'{"Broadcast Bytes":>28}: {network_stat.broadcast_bytes:,}')
    print(f'{"Broadcast Packets":>28}: {network_stat.broadcast_packets:,}')
    print(f'{"Multicast Bytes":>28}: {network_stat.multicast_bytes:,}')
    print(f'{"Multicast Packets":>28}: {network_stat.multicast_packets:,}')
    print(f'{"Total Bytes":>28}: {network_stat.total_bytes:,}')
    print(f'{"Total Packets":>28}: {network_stat.total_packets:,}')
    print()


def print_network_stats(network_stats, tab=20):
    if network_stats is None:
        print('No network statistics')
        return
    print('Network Statistics')
    print(f'{"Duration":>20}: {format_duration(network_stats.duration)}')
    print(f'{"Broadcast Bytes":>20}: {network_stats.broadcast_bytes:,}')
    print(f'{"Broadcast Packets":>20}: {network_stats.broadcast_packets:,}')
    print(f'{"Multicast Bytes":>20}: {network_stats.multicast_bytes:,}')
    print(f'{"Multicast Packets":>20}: {network_stats.multicast_packets:,}')
    print(f'{"Total Bytes":>20}: {network_stats.total_bytes:,}')
    print(f'{"Total Packets":>20}: {network_stats.total_packets:,}')
    print(f'{"Network Stats":>20}: {len(network_stats.network_stats)}')
    for stat in network_stats.network_stats:
        print_network_stat(stat)
    print(f'{"Channels":>20}: {len(network_stats.channel_list)}')
    for channel in network_stats.channel_list:
        print_channel_stats(channel, tab)
    print()


def print_node_stat(node_stat, tab=20):
    if node_stat is None:
        print('No node statistics')
        return
    print(f'{"Node Statistic":>{tab}}: {node_stat.name}')
    print(f'{"Node":>30}: {node_stat.name}')
    print(f'{"Broadcast Bytes":>34}: {node_stat.broadcast_bytes:,}')
    print(f'{"Broadcast Packets":>34}: {node_stat.broadcast_packets:,}')
    print(f'{"Bytes Received":>34}: {node_stat.bytes_received:,}')
    print(f'{"Bytes Sent":>34}: {node_stat.bytes_sent:,}')
    print(f'{"Color":>34}: {node_stat.color}')
    print(f'{"City":>34}: {node_stat.city}')
    print(f'{"Country":>34}: {node_stat.country}')
    print(f'{"Country Code":>34}: {node_stat.country_code}')
    print(f'{"Duration":>34}: {format_duration(node_stat.duration)}')
    print(f'{"First Time Received":>34}: {node_stat.first_time_received}')
    print(f'{"First Time Sent":>34}: {node_stat.first_time_sent}')
    print(f'{"Last Time Received":>34}: {node_stat.last_time_received}')
    print(f'{"Last Time Sent":>34}: {node_stat.last_time_sent}')
    print(f'{"Latitude":>34}: {node_stat.latitude:.4f}')
    print(f'{"Longitude":>34}: {node_stat.longitude:.4f}')
    print(f'{"Max Packet Size Received":>34}: {node_stat.maximum_packet_size_received:,}')
    print(f'{"Max Packet Size Sent":>34}: {node_stat.maximum_packet_size_sent:,}')
    print(f'{"Media Spec":>34}: {node_stat.media_spec}')
    print(f'{"Min Packet Size Received":>34}: {node_stat.minimum_packet_size_received:,}')
    print(f'{"Min Packet Size Sent":>34}: {node_stat.minimum_packet_size_sent:,}')
    print(f'{"Multicast Bytes":>34}: {node_stat.multicast_bytes:,}')
    print(f'{"Multicast Packets":>34}: {node_stat.multicast_packets:,}')
    print(f'{"Packets Received":>34}: {node_stat.packets_received:,}')
    print(f'{"Packets Sent":>34}: {node_stat.packets_sent:,}')
    print(f'{"Trust":>34}: {node_stat.trust}')
    print()


def print_node_stats(node_stats, tab=20):
    if node_stats is None:
        print('No Node Statistics')
        return
    print('Node Statistics')
    print(f'{"Duration":>20}: {format_duration(node_stats.duration)}')
    print(f'{"Reset Count":>20}: {node_stats.reset_count:,}')
    print(f'{"Time Limit Reached":>20}: {node_stats.time_limit_reached}')
    print(f'{"Total Bytes":>20}: {node_stats.total_bytes:,}')
    print(f'{"Total Packets":>20}: {node_stats.total_packets:,}')
    print(f'{"Node Stats":>20}: {len(node_stats.node_stats)}')
    for node_stat in node_stats.node_stats:
        print_node_stat(node_stat)
    print()


def print_packet(p, tab=22):
    if p is None:
        print('No packet')
        return
    print(f'Packet Number: {p.number}')
    print(f'{"Index":>{tab}}: {p.index}')
    if p.timestamp:
        print(f'{"Time Stamp":>{tab}}: {p.timestamp}')
    # print(f'{"ProtoSpec":>{tab}}: {p.proto_spec}')
    # print(f'{"ProtoSpec Name":>{tab}}: {p.protocol_name()}')
    print(f'{"Application":>{tab}}: {p.application}')
    # print(f'{"Flags":>{tab}}: {hex(p.flags)}')
    print(f'{"Flow Id":>{tab}}: {p.flow_id}')
    print(f'{"Status":>{tab}}: {hex(p.status)}')
    print(f'{"Length":>{tab}}: {p.packet_length}')

    print(f'{"Address 1":>{tab}}: {p.address_1}')
    print(f'{"Address 2":>{tab}}: {p.address_2}')
    print(f'{"Application":>{tab}}: {p.application}')
    print(f'{"Application Id":>{tab}}: {p.application_id}')
    print(f'{"Application Color":>{tab}}: {p.application_color}')
    print(f'{"Data":>{tab}}: {p.data}')
    print(f'{"Data Rate":>{tab}}: {p.data_rate}')
    print(f'{"Date":>{tab}}: {p.date or ""}')
    print(f'{"Delta Time":>{tab}}: {p.delta_time or ""}')
    print(f'{"Destination":>{tab}}: {p.destination}')
    print(f'{"Destination City":>{tab}}: {p.destination_city}')
    print(f'{"Destination Country":>{tab}}: Code: {p.destination_country.code} '
          f'Name: {p.destination_country.name}')
    print(f'{"Destination Latitude":>{tab}}: {p.destination_latitude}')
    print(f'{"Destination Logical":>{tab}}: {p.destination_logical}')
    print(f'{"Destination Longitude":>{tab}}: {p.destination_longitude}')
    print(f'{"Destination Physical":>{tab}}: {p.destination_physical}')
    print(f'{"Destination Port":>{tab}}: {p.destination_port}')
    print(f'{"Expert":>{tab}}: {p.expert}')
    print(f'{"Filter":>{tab}}: {p.filter}')
    print(f'{"Flags":>{tab}}: {p.flags}')
    print(f'{"Flow_id":>{tab}}: {p.flow_id}')
    print(f'{"Index":>{tab}}: {p.index}')
    print(f'{"Ip Identifier":>{tab}}: {p.ip_identifier}')
    print(f'{"Ip Length":>{tab}}: {p.ip_length}')
    print(f'{"Ip TTL":>{tab}}: {p.ip_ttl}')
    print(f'{"MCS":>{tab}}: {p.mcs}')
    print(f'{"Mpls":>{tab}}: {p.mpls}')
    print(f'{"Number":>{tab}}: {p.number}')
    print(f'{"Packet Length":>{tab}}: {p.packet_length}')
    print(f'{"Protocol":>{tab}}: {p.protocol}')
    print(f'{"Relative Time":>{tab}}: {p.relative_time or ""}')
    print(f'{"Size Bar":>{tab}}: {p.size_bar}')
    print(f'{"Source":>{tab}}: {p.source}')
    print(f'{"Source City":>{tab}}: {p.source_city}')
    print(f'{"Source Country":>{tab}}: Code: {p.source_country.code} Name: {p.source_country.name}')
    print(f'{"Source Latitude":>{tab}}: {p.source_latitude}')
    print(f'{"Source Logical":>{tab}}: {p.source_logical}')
    print(f'{"Source Longitude":>{tab}}: {p.source_longitude}')
    print(f'{"Source Physical":>{tab}}: {p.source_physical}')
    print(f'{"Source Port":>{tab}}: {p.source_port}')
    print(f'{"Spatial Atreams":>{tab}}: {p.spatial_streams}')
    print(f'{"Status":>{tab}}: {p.status}')
    print(f'{"Summary":>{tab}}: {p.summary}')
    print(f'{"Summary Aource":>{tab}}: {p.summary_source}')
    print(f'{"Timestamp":>{tab}}: {p.timestamp}')
    print(f'{"Vlan":>{tab}}: {p.vlan}')

    print('  Wireless:')
    print(f'{"Address 3":>{tab+2}}: {p.address_3}')
    print(f'{"Address 4":>{tab+2}}: {p.address_4}')
    print(f'{"Band":>{tab+2}}: {p.band}')
    print(f'{"Bssid":>{tab+2}}: {p.bssid}')
    print(f'{"Flags 80211":>{tab+2}}: {p.flags80211}')
    print(f'{"Frequency":>{tab+2}}: {p.frequency}')
    print(f'{"Full Duplex Channel":>{tab+2}}: {p.full_duplex_channel}')
    print(f'{"Noise dBm":>{tab+2}}: {p.noise_dbm}')
    print(f'{"Receiver":>{tab+2}}: {p.receiver}')
    print(f'{"Noise Strength":>{tab+2}}: {p.noise_strength}')
    print(f'{"Signal dBm":>{tab+2}}: {p.signal_dbm}')
    print(f'{"Signal Strength":>{tab+2}}: {p.signal_strength}')
    print(f'{"Transmitter":>{tab+2}}: {p.transmitter}')
    print(f'{"WAN Direction":>{tab+2}}: {p.wan_direction}')
    print(f'{"Wireless Channel":>{tab+2}}: {p.wireless_channel}')
    print()


def print_packet_list(pl):
    if pl:
        for p in pl:
            print_packet(p)
    print()


def print_protocol(p, tab=20):
    if not p:
        print('No protocol')
        return
    print(f'Protocol: {p.name}')
    print(f'{"Color":>{tab}}: {p.color}')
    print(f'{"Description":>{tab}}: {p.description}')
    print(f'{"Hierarchy Name":>{tab}}: {p.hierarchy_name}')
    print(f'{"Id":>{tab}}: {p.id}')
    print(f'{"Long Name":>{tab}}: {p.long_name}')
    print()


def print_protocol_list(pl):
    if not pl:
        print('No protocol list')
        return
    for p in pl:
        print_protocol(p)
    print()


def print_protocol_stat(protocol_stat, print_empty=True, tab=20):
    if protocol_stat is None:
        print('No protocol statistic')
        return
    if not print_empty and protocol_stat.bytes == 0:
        return
    print(f'{"Protocol Statistic":>{tab}}: {protocol_stat.name}')
    print(f'{"Name":>28}: {protocol_stat.name}')
    print(f'{"Protocol":>24}: {protocol_stat.protocol}')
    print(f'{"Bytes":>28}: {protocol_stat.bytes:,}')
    print(f'{"Color":>28}: {protocol_stat.color}')
    print(f'{"Duration":>28}: {format_duration(protocol_stat.duration)}')
    print(f'{"First Time":>28}: {protocol_stat.first_time}')
    print(f'{"Id Code":>28}: {protocol_stat.id_code}')
    print(f'{"Last Time":>28}: {protocol_stat.last_time}')
    print(f'{"Media Spec":>28}: {protocol_stat.media_spec}')
    print(f'{"Packets":>28}: {protocol_stat.packets:,}')
    print()


def print_protocol_stats(protocol_stats, tab=20):
    if protocol_stats is None:
        print('No Protocal Statistics')
        return
    print('Protocol Statistics')
    print(f'{"Duration":>20}: {format_duration(protocol_stats.duration)}')
    print(f'{"Reset Count":>20}: {protocol_stats.reset_count:,}')
    print(f'{"Time Limit Reached":>20}: {protocol_stats.time_limit_reached}')
    print(f'{"Total Bytes":>20}: {protocol_stats.total_bytes:,}')
    print(f'{"Total Packets":>20}: {protocol_stats.total_packets:,}')
    print(f'{"":>20}: {len(protocol_stats.protocol_stats)}')
    for stat in protocol_stats.protocol_stats:
        print_protocol_stat(stat, False)
    print()
    for protocol in protocol_stats.protocol_stats:
        print_protocol_stat(protocol, False)
    print()


def print_protocol_by_id_stat(protocol_by_id_stat, print_empty=True, tab=20):
    if protocol_by_id_stat is None:
        print('No Protocol By Id statistic')
        return
    if not print_empty and protocol_by_id_stat.bytes == 0:
        return
    print(f'{"Protocol By IdStatistic":>{tab}}: {protocol_by_id_stat.name}')
    print(f'{"Name":>28}: {protocol_by_id_stat.name}')
    print(f'{"Protocol":>24}: {protocol_by_id_stat.protocol}')
    print(f'{"Bytes":>28}: {protocol_by_id_stat.bytes:,}')
    print(f'{"Color":>28}: {protocol_by_id_stat.color}')
    print(f'{"Duration":>28}: {format_duration(protocol_by_id_stat.duration)}')
    print(f'{"First Time":>28}: {protocol_by_id_stat.first_time}')
    print(f'{"Id Code":>28}: {protocol_by_id_stat.id_code}')
    print(f'{"Last Time":>28}: {protocol_by_id_stat.last_time}')
    print(f'{"Media Spec":>28}: {protocol_by_id_stat.media_spec}')
    print(f'{"Packets":>28}: {protocol_by_id_stat.packets:,}')
    print()


def print_protocol_by_id_stats(protocol_by_id_stats, tab=20):
    if protocol_by_id_stats is None:
        print('No Protocal By Id Statistics')
        return
    print('Protocol Statistics')
    print(f'{"Duration":>20}: {format_duration(protocol_by_id_stats.duration)}')
    print(f'{"Reset Count":>20}: {protocol_by_id_stats.reset_count:,}')
    print(f'{"Time Limit Reached":>20}: {protocol_by_id_stats.time_limit_reached}')
    print(f'{"Total Bytes":>20}: {protocol_by_id_stats.total_bytes:,}')
    print(f'{"Total Packets":>20}: {protocol_by_id_stats.total_packets:,}')
    print(f'{"":>20}: {len(protocol_by_id_stats.protocol_stats)}')
    for stat in protocol_by_id_stats.protocol_stats:
        print_protocol_stat(stat, False)
    print()
    for protocol in protocol_by_id_stats.protocol_by_id_stats:
        print_protocol_stat(protocol, False)
    print()


def print_remote_engine(re, tab=20):
    if not re:
        print('No remote engine')
        return
    print(f'Remote Engine: {re.name}')
    print(f'{"group":>{tab+2}}: {re.group}')
    print(f'{"host":>{tab+2}}: {re.host}')
    print(f'{"id":>{tab+2}}: {re.id}')
    print(f'{"last_login":>{tab+2}}: {re.last_login or ""}')
    print(f'{"latitude":>{tab+2}}: {re.latitude}')
    print(f'{"longitude":>{tab+2}}: {re.longitude}')
    print(f'{"password":>{tab+2}}: {"********" if re.password else ""}')
    print(f'{"remote_name":>{tab+2}}: {re.remote_name}')
    print(f'{"user_name":>{tab+2}}: {re.user_name}')
    print()


def print_remote_engine_list(lst, tab=20):
    if not lst:
        print('No remote engine list.')
        return
    for r in lst:
        print_remote_engine(r, tab)


def print_size_stat(size_stat, tab=20):
    if size_stat is None:
        print('No size')
        return
    print(f'{"Size Name":>{tab}}: {size_stat.name}')
    print(f'{"Range":>{tab}}: {size_stat.minimum} to {size_stat.maximum}')
    print(f'{"Packets":>{tab}}: {size_stat.packets:,}')
    print()


def print_size_stats(size_stats, tab=20):
    if size_stats is None:
        print('No list of size stats')
        return
    print('Size Statistics')
    for stat in size_stats.size_stats:
        print_size_stat(stat, tab+4)
    print()


def print_summary_stat(summary_stat, tab: int = 40):
    if summary_stat is None:
        print('No Summary Statistic')
        return
    if summary_stat.value is not None:
        if (summary_stat.value_type == SummaryType.PACKETS
                or summary_stat.value_type == SummaryType.BYTES
                or summary_stat.value_type == SummaryType.INT):
            print(f'{summary_stat.name:>{tab}}: {summary_stat.value:,}')
        elif summary_stat.value_type == SummaryType.DOUBLE:
            print(f'{summary_stat.name:>{tab}}: {summary_stat.value:,.4f}')
        elif summary_stat.value_type == SummaryType.DURATION:
            print(f'{summary_stat.name:>{tab}}: {format_duration(summary_stat.value)}')
        else:
            print(f'{summary_stat.name:>{tab}}: {summary_stat.value}')


def print_summary_snapshot(snapshot, current: bool, tab: int = 20):
    if snapshot is None:
        print('No summary snapshot')
        return
    print(f'{"Snapshot":>{tab}}: {snapshot.name or snapshot.id}'
          f'{" Current Snapshot" if current else ""}')
    for stat in snapshot.summary_stats:
        print_summary_stat(stat, max(tab + 4, 40))


def print_summary_stats(summary_stats, tab: int = 20):
    if summary_stats is None:
        print('No Summary Statistics')
        return
    print('Summary Statistics:')
    print(f'{"Duration":>{tab}}: {format_duration(summary_stats.duration)}')
    print(f'{"Total Bytes":>{tab}}: {summary_stats.total_bytes:,}')
    print(f'{"Total Packets":>{tab}}: {summary_stats.total_packets:,}')
    for snapshot in summary_stats.summary_snapshots:
        print_summary_snapshot(snapshot, (snapshot.id == summary_stats.current_id), tab + 4)
        print()


def print_summary_stats_current(summary_stats, tab: int = 20):
    if summary_stats is None:
        print('No Summary Statistics')
        return
    current_summary_snapshot = summary_stats.get_current_snapshot()
    if current_summary_snapshot is not None:
        print('Current Summary Statistic Snapshot:')
        print(f'{"Duration":>40}: {format_duration(summary_stats.duration)}')
        print(f'{"Total Bytes":>40}: {summary_stats.total_bytes:,}')
        print(f'{"Total Packets":>40}: {summary_stats.total_packets:,}')
        for stat in current_summary_snapshot.summary_stats:
            print_summary_stat(stat)
        print()


def print_user(user, tab=20):
    if user is None:
        print('No user')
        return
    print(f'{" ":>{tab}}{str(user)}')


def print_user_list(lst, tab=20):
    if not lst:
        print('No user list.')
        return
    print(f'{"User List:":>{tab}}')
    for u in lst:
        print_user(u, tab)
    print()
