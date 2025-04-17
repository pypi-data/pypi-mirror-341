import datetime
import pytest
import six

from omniscript.eventlog import EventLogEntry
from omniscript.expertpreferences import ExpertPreferences
from omniscript.invariant import (
    DatabaseOperation, EmailScheme, PeekResult, Severity, DIAGNOSTICS_COMMANDS,
    NOTIFICATION_SOURCES)
from omniscript.omnierror import OmniError
from omniscript.notifications import SendEmailRequest, SendNotificationRequest


def check_array_of_objects(o):
    if isinstance(o, list):
        for i in o:
            if i is None:
                return False
        return True
    else:
        return False


def check_optional_array_of_objects(o):
    if o is None:
        return True
    if isinstance(o, list):
        for i in o:
            if i is None:
                return False
        return True
    else:
        return False


@pytest.fixture(scope="module")
def adapters(engine):
    """Adapters"""
    return engine.get_adapter_list()


@pytest.mark.api
def test_get_adapters(adapters):
    """Verifies the adapters can be retrieved."""
    assert check_array_of_objects(adapters), 'Error in getting adapters'


@pytest.fixture(scope="module")
def adapters_info(engine):
    """Adapter infos"""
    return engine.get_adapter_information_list()


@pytest.mark.api
def test_get_adapter_infos(adapters_info):
    """Verifies the adapter infos can be retrieved."""
    assert check_array_of_objects(adapters_info), 'Error in getting adapter infos'


@pytest.fixture(scope="module")
def applications(engine):
    """Applications"""
    return engine.get_application_list()


@pytest.mark.api
def test_get_applications(applications):
    """Verifies the applications can be retrieved."""
    assert check_array_of_objects(applications), 'Error in getting applications'


@pytest.fixture(scope="module")
def countries(engine):
    """Countries"""
    return engine.get_country_list()


@pytest.mark.api
def test_get_countries(countries):
    """Verifies the countries can be retrieved."""
    assert check_array_of_objects(countries), 'Error in getting countries'


@pytest.mark.api
@pytest.mark.skip('Invasive procedure')
def test_database_index(engine):
    """Verifies the database can be indexed."""
    passed = True
    try:
        engine.file_database_operation(DatabaseOperation.INDEX)
    except OmniError:
        passed = False
    assert passed, 'Error in indexing database'


@pytest.mark.api
@pytest.mark.skip('Invasive procedure')
def test_database_maintenance(engine):
    """Verifies the database can be maintained."""
    passed = True
    try:
        engine.file_database_operation(DatabaseOperation.MAINTENANCE)
    except OmniError:
        passed = False
    assert passed, 'Error in maintaining database'


@pytest.mark.api
@pytest.mark.skip('Invasive procedure')
def test_database_sync(engine):
    """Verifies the database can be synced."""
    passed = True
    try:
        engine.file_database_operation(DatabaseOperation.SYNC)
    except OmniError:
        passed = False
    assert passed, 'Error in syncing database'


@pytest.fixture(scope="module")
def engine_capabilities(engine):
    """Engine capabilities."""
    return engine.get_capabilities()


@pytest.mark.api
def test_get_engine_capabilities(engine_capabilities):
    """Verifies the engine capabilities can be retrieved."""
    # def check_plugins_info(pluginsInfo):
    #     if isinstance(pluginsInfo, list):
    #         for pi in pluginsInfo:
    #             if pi is None:
    #                 return False
    #             if pi.defaultOptions is not None:
    #                 if (not check_array_of_objects(pi.defaultOptions.optionList)
    #                     or pi.features is None):
    #                     return False
    #         return True
    #     return False

    assert (engine_capabilities is not None
            and check_optional_array_of_objects(engine_capabilities.administrator_default_list)
            and check_array_of_objects(engine_capabilities.capability_list)
            and check_array_of_objects(engine_capabilities.packet_file_index_list)
            and check_array_of_objects(engine_capabilities.performance_item_list)
            and check_optional_array_of_objects(engine_capabilities.plugin_id_list)
            and check_optional_array_of_objects(engine_capabilities.plugin_information_list)
            and check_array_of_objects(engine_capabilities.policy_id_list)), (
        'Error in getting engine capabilitie,s')


@pytest.fixture(scope="module")
def connected_users(engine):
    """Users connected to the engine."""
    return engine.get_connected_user_list()


@pytest.mark.api
def test_get_engine_connected_users(connected_users):
    """Verifies the engine connected users can be retrieved."""
    assert connected_users is not None and check_array_of_objects(connected_users), (
        'Error in getting engine connected users')


@pytest.mark.api
@pytest.mark.skip('Skipping create directory test since there is no way to remove it later')
def test_create_directory(engine):
    """Verifies a new directory can be created."""
    assert engine.create_directory('/tmp/my_new_directory'), 'Error in creating directory'


@pytest.mark.api
@pytest.mark.skip('Skipping create file test since there is no way to remove it later')
def test_create_file(engine):
    """Verifies a new file can be created."""
    assert engine.create_file('/tmp/my_file'), 'Error in creating file'


@pytest.mark.api
@pytest.mark.skip('Temporarily skipping for performance')
def test_diagnostics(engine):
    """Verifies the engine diagnostics can be run."""
    for command in DIAGNOSTICS_COMMANDS:
        result = engine.diagnostics(command, True)
        assert isinstance(result, six.string_types), (
            f'Error in getting engine diagnostics for command {command}')


@pytest.fixture(scope="module")
def engine_directory_list(engine):
    """Engine directory list."""
    return engine.get_directory('/var/lib/omni/data', True, True)


@pytest.mark.api
def test_get_engine_directory_list(engine_directory_list):
    """Verifies the engine directory list can be retrieved."""
    assert engine_directory_list is not None, 'Error in getting engine directory list'


@pytest.fixture(scope="module")
def engine_list(engine):
    """Engine list."""
    return engine.get_remote_engine_list()


@pytest.mark.api
@pytest.mark.order(13)
@pytest.mark.skip('Disabling all test.')
def test_get_engine_list(engine_list):
    """Verifies the engine list can be retrieved."""
    assert engine_list is not None and check_array_of_objects(engine_list.engines), (
        'Error in getting engine list')


@pytest.mark.api
@pytest.mark.order(14)
@pytest.mark.skip('Disabling all test.')
def test_set_engine_list(engine, engine_list):
    """Verifies the engine list can be set."""
    new_engine_list = engine.set_engine_list(engine_list)
    assert new_engine_list is not None and check_array_of_objects(new_engine_list.engines), (
        'Error in setting engine list')


@pytest.mark.api
@pytest.mark.order(15)
@pytest.mark.skip('Disabling all test. Deletes engine list.')
def test_delete_engine_list(engine, engine_list):
    """Verifies the engine list can be deleted."""
    delete_response = engine.delete_engine_list()
    new_engine_list = engine.set_engine_list(engine_list)
    assert (delete_response is not None
            and new_engine_list is not None
            and check_array_of_objects(new_engine_list.engines)), (
        'Error in deleting engine list')


@pytest.mark.api
@pytest.mark.order(16)
@pytest.mark.skip('Disabling all test.')
def test_get_engine(engine, engine_list):
    """Verifies an engine can be retrieved."""
    for engine_list_item in engine_list.engines:
        response = engine.get_engine(engine_list_item.id)
        assert response is not None, f'Error in getting engine with id "{engine_list_item.id}"'


# @pytest.fixture(scope="module")
# def new_engines():
#     """New engines."""
#     engines = []
#     engines.append(EngineCollectionItem({
#         'group': '',
#         'host': '10.8.100.141',
#         'id': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFF0',
#         'latitude': 37.931,
#         'longitude': -122.027,
#         'name': 'LiveAction Walnut Creek',
#         'remoteName': '',
#         'username': 'admin',
#         'password': 'password'
#     }))
#     return engines


# @pytest.mark.api
# @pytest.mark.order(17)
# @pytest.mark.skip('Disabling all test.')
# def test_add_engine(engine, new_engines):
#     """Verifies an engine can be added."""
#     for new_engine in new_engines:
#         assert engine.set_engine(new_engine) is not None, (
#             f'Error in adding engine with id "{new_engine.id}"')


# @pytest.mark.api
# @pytest.mark.order(18)
# @pytest.mark.skip('Disabling all test.')
# def test_modify_engine(engine, new_engines):
#     """Verifies an engine can be modified."""
#     for new_engine in new_engines:
#         modified_engine = new_engine
#         modified_engine.name += ' (Modified)'
#         assert engine.set_engine(modified_engine) is not None, (
#             f'Error in modifying engine with id "{modified_engine.id}"')


# @pytest.mark.api
# @pytest.mark.order(19)
# @pytest.mark.skip('Disabling all test. Deletes engine.')
# def test_delete_engine(engine, new_engines):
#     """Verifies an engine can be deleted."""
#     for new_engine in new_engines:
#         assert engine.delete_engine(new_engine.id) is not None, (
#             f'Error in deleting engine with id "{new_engine.id}"')


@pytest.fixture(scope="module")
def engine_expert_prefs(engine):
    """Engine Expert preferences."""
    return engine.get_expert_preferences()


@pytest.mark.api
@pytest.mark.order(20)
@pytest.mark.skip('Disabling all test.')
def test_get_engine_expert_prefs(engine_expert_prefs):
    """Verifies the Expert preferences can be retrieved."""
    def check_channel_family(o):
        if isinstance(o, list):
            for i in o:
                if i is None or not check_array_of_objects(i.items):
                    return False
            return True
        return False

    def check_expert_settings_group(o):
        if (o is None or o.policy is None
                or o.policy.authentication is None
                or not check_array_of_objects(o.policy.authentication.items)
                or o.policy.channel is None
                or not check_channel_family(o.policy.channel.channelFamily)
                or o.policy.encryption is None
                or not check_array_of_objects(o.policy.encryption.items)
                or o.policy.essId is None
                or not check_array_of_objects(o.policy.essId.items)
                or o.policy.vendorId is None
                or not check_array_of_objects(o.policy.vendorId.items)
                or not check_array_of_objects(o.problems)):
            return False
        return True

    def check_string_table(o):
        if isinstance(o, list):
            for i in o:
                if i is None or not check_array_of_objects(i.values):
                    return False
            return True
        else:
            return False

    assert (engine_expert_prefs is not None
            and check_array_of_objects(engine_expert_prefs.descriptions)
            and check_array_of_objects(engine_expert_prefs.layers)
            and engine_expert_prefs.settings is not None
            and check_expert_settings_group(engine_expert_prefs.settings.current)
            and check_expert_settings_group(engine_expert_prefs.settings._default)
            and check_string_table(engine_expert_prefs.stringTable)), (
        'Error in getting engine Expert preferences')


@pytest.mark.api
@pytest.mark.order(21)
@pytest.mark.skip('Disabling all test.')
def test_set_engine_expert_prefs(engine, engine_expert_prefs):
    """Verifies the Expert preferences can be set."""
    request = ExpertPreferences({})
    request.settings = engine_expert_prefs.settings
    assert engine.set_expert_prefs(request) is not None, (
        'Error in setting engine Expert preferences')


@pytest.mark.api
@pytest.mark.skip('Temporarily skipping so engine does not restart')
def test_engine_restart(engine):
    """Verifies the engine service can be restarted."""
    assert engine.engine_restart() is not None, 'Error in restarting engine service'


@pytest.fixture(scope="module")
def engine_settings(engine):
    """Engine settings."""
    return engine.get_settings()


@pytest.mark.api
@pytest.mark.order(22)
@pytest.mark.skip('Disabling all test.')
def test_get_engine_settings(engine_settings):
    """Verifies the engine settings can be retrieved."""
    def check_acl_policies(o):
        if isinstance(o, list):
            for i in o:
                if (i is None
                        or not check_array_of_objects(i.commands)
                        or not check_array_of_objects(i.users)):
                    return False
            return True
        return False

    def check_adapter_or_capture_locks(o):
        if isinstance(o, list):
            for i in o:
                if i is None or not check_array_of_objects(i.lock):
                    return False
            return True
        return False

    assert (engine_settings is not None
            and engine_settings.acl is not None
            and check_acl_policies(engine_settings.acl.policies)
            and engine_settings.network is not None
            and engine_settings.runtimeLock is not None
            and check_adapter_or_capture_locks(engine_settings.runtimeLock.adapterLocks)
            and check_adapter_or_capture_locks(engine_settings.runtimeLock.captureLocks)
            and check_array_of_objects(engine_settings.runtimeLock.sessionLocks)
            and engine_settings.security is not None
            and engine_settings.security.authentication is not None
            and engine_settings.security.authenticationServers is not None
            and check_array_of_objects(engine_settings.security.authenticationServers.servers)
            and engine_settings.security.sslCertificate is not None), (
        'Error in getting engine settings')


@pytest.mark.api
@pytest.mark.order(23)
@pytest.mark.skip('Disabling all test.')
def test_set_engine_settings(engine, engine_settings):
    """Verifies the engine settings can be set."""
    response = engine.set_engine_settings(engine_settings)
    assert response is not None and response.result == PeekResult.OK, (
        'Error in setting engine settings')


@pytest.mark.api
@pytest.mark.skip('Disabling all test.')
def test_get_support(engine):
    """Verifies the engine support information can be retrieved."""
    assert engine.get_support_information() is not None, (
        'Error in getting engine support information')


@pytest.fixture(scope="module")
def user_list(engine):
    """Engine user list."""
    return engine.get_user_list()


@pytest.mark.api
def test_get_user_list(user_list):
    """Verifies the engine user list can be retrieved."""
    assert (user_list is not None
            and check_array_of_objects(user_list)), (
        'Error in getting engine user list')


@pytest.mark.api
def test_get_version(engine):
    """Verifies the engine version can be retrieved."""
    assert engine.get_version() is not None, 'Error in getting engine version'


@pytest.fixture(scope="module")
def events(engine):
    """Events"""
    return engine.get_event_log()


@pytest.mark.api
def test_get_events(events):
    """Verifies the events can be retrieved."""
    assert events is not None and check_array_of_objects(events.entries), 'Error in getting events'


@pytest.fixture(scope="module")
def new_events():
    """New events."""
    newEvents = []
    newEvents.append(EventLogEntry({
        'contextId': 'FFFFFFFF-FFFF-FFFF-EEEE-FFFFFFFFFFF1',
        'longMessage': 'Test: long description 1',
        'severity': Severity.INFORMATIONAL,
        'shortMessage': 'Test: short description 1',
        'sourceId': 'FFFFFFFF-FFFF-FFFF-EEEE-FFFFFFFFFFF1',
        'sourceKey': 0,
        'timestamp': f'{datetime.datetime.now().isoformat()}Z',
    }))
    newEvents.append(EventLogEntry({
        'contextId': 'FFFFFFFF-FFFF-FFFF-EEEE-FFFFFFFFFFF2',
        'longMessage': 'Test: long description 2',
        'severity': Severity.MAJOR,
        'shortMessage': 'Test: short description 2',
        'sourceId': 'FFFFFFFF-FFFF-FFFF-EEEE-FFFFFFFFFFF2',
        'sourceKey': 0,
        'timestamp': f'{datetime.datetime.now().isoformat()}Z',
    }))
    newEvents.append(EventLogEntry({
        'contextId': 'FFFFFFFF-FFFF-FFFF-EEEE-FFFFFFFFFFF3',
        'longMessage': 'Test: long description 3',
        'severity': Severity.MINOR,
        'shortMessage': 'Test: short description 3',
        'sourceId': 'FFFFFFFF-FFFF-FFFF-EEEE-FFFFFFFFFFF3',
        'sourceKey': 0,
        'timestamp': f'{datetime.datetime.now().isoformat()}Z',
    }))
    newEvents.append(EventLogEntry({
        'contextId': 'FFFFFFFF-FFFF-FFFF-EEEE-FFFFFFFFFFF4',
        'longMessage': 'Test: long description 4',
        'severity': Severity.SEVERE,
        'shortMessage': 'Test: short description 4',
        'sourceId': 'FFFFFFFF-FFFF-FFFF-EEEE-FFFFFFFFFFF4',
        'sourceKey': 0,
        'timestamp': f'{datetime.datetime.now().isoformat()}Z',
    }))
    return newEvents


@pytest.mark.api
@pytest.mark.order(11)
@pytest.mark.skip('Disabling all test.')
def test_add_events(engine, new_events):
    """Verifies the events can be added."""
    assert (engine.add_events(new_events[0]) is not None
            and engine.add_events(new_events[1:]) is not None), (
        'Error in adding events')


@pytest.mark.api
@pytest.mark.order(12)
@pytest.mark.skip('Disabling all test. Deletes events.')
def test_delete_events(engine, new_events):
    """Verifies the events can be deleted."""
    passed = True
    try:
        for event_item in new_events:
            engine.delete_event_log(event_item.capture_id)
    except OmniError:
        passed = False
    assert passed, 'Error in deleting events'


@pytest.fixture(scope="module")
def configuration(engine):
    """LiveFlow configuration."""
    return engine.get_liveflow_configuration()


@pytest.fixture(scope="module")
def liveflow_context(engine):
    """LiveFlow context."""
    return engine.get_liveflow_context()


@pytest.fixture(scope="module")
def liveflow_status(engine):
    """LiveFlow status."""
    return engine.get_liveflow_status()


@pytest.mark.api
@pytest.mark.order(1)
@pytest.mark.skip('Disabling all test.')
def test_get_liveflow_configuration(configuration):
    """Verifies the LiveFlow configuration can be retrieved."""
    assert (configuration is not None
            and configuration.preferences is not None
            and configuration.preferences.ipfix is not None), (
        'Error in getting LiveFlow configuration')


@pytest.mark.api
@pytest.mark.order(2)
@pytest.mark.skip('Disabling all test.')
def test_get_liveflow_configuration_services(configuration):
    """Verifies the services in LiveFlow configuration."""
    if configuration is not None:
        for service in configuration.services:
            assert service is not None, 'Error in LiveFlow configuration services'


@pytest.mark.api
@pytest.mark.order(3)
@pytest.mark.skip('Disabling all test.')
def test_get_liveflow_configuration_wan_mac_list(configuration):
    """Verifies the router map in LiveFlow configuration."""
    if (configuration is not None and configuration.preferences is not None
            and configuration.preferences.ipfix is not None):
        for wan_mac_list_item in configuration.preferences.ipfix.wan_mac_list:
            assert wan_mac_list_item is not None, 'Error in LiveFlow configuration router map'


@pytest.mark.api
@pytest.mark.order(4)
@pytest.mark.skip('Disabling all test.')
def test_set_liveflow_configuration(engine, configuration):
    """Verifies the LiveFlow configuration can be set."""
    assert engine.set_liveflow_configuration(configuration) is not None, (
        'Error in setting LiveFlow configuration')


@pytest.mark.api
@pytest.mark.skip('Disabling all test.')
def test_get_liveflow_context(liveflow_context):
    """Verifies LiveFlow context can be retrieved."""
    assert liveflow_context is not None and liveflow_context.license is not None, (
        'Error in getting LiveFlow context')


@pytest.mark.api
@pytest.mark.skip('Disabling all test.')
def test_get_liveflow_status(liveflow_status):
    """Verifies LiveFlow status can be retrieved."""
    assert liveflow_status is not None and liveflow_status.recordsSent is not None, (
        'Error in getting LiveFlow status')


@pytest.mark.api
@pytest.mark.skip('Disabling all test.')
def test_get_liveflow_status_hash_table(liveflow_status):
    """Verifies hash table in LiveFlow status."""
    if liveflow_status is not None:
        for hashTable in liveflow_status.hashTable:
            assert hashTable is not None, 'Error in LiveFlow status hash table'


@pytest.mark.api
@pytest.mark.skip('Disabling all test.')
def test_get_liveflow_configuration_context_match(configuration, liveflow_context):
    """Compares LiveFlow configuration and LiveFlow context."""
    if (configuration is not None and liveflow_context is not None
            and configuration.preferences is not None
            and configuration.preferences.ipfix is not None):
        assert (configuration.preferences.hostname_analysis == liveflow_context.hostnameAnalysis
                or configuration.preferences.ipfix.avc_enabled == liveflow_context.ipfixAVCOutput
                or configuration.preferences.ipfix.fnf_enabled == liveflow_context.ipfixFNFOutput
                or (configuration.preferences.ipfix.medianet_enabled
                    == liveflow_context.ipfixMediaNetOutput)
                or (configuration.preferences.ipfix.signaling_dn_enabled
                    == liveflow_context.ipfixSignalingDNOutput)
                or configuration.preferences.latency_enabled == liveflow_context.latencyAnalysis
                or configuration.preferences.rtp_enabled == liveflow_context.rtpAnalysis
                or (configuration.preferences.enforce_tcp_3way_handshake
                    == liveflow_context.tcp3WayHandshakeEnforcement)
                or configuration.preferences.quality_enabled == liveflow_context.tcpQualityAnalysis
                or (configuration.preferences.retransmissions_enabled
                    == liveflow_context.tcpRetransmissionsAnalysis)
                or configuration.preferences.tls_analysis == liveflow_context.tlsAnalysis
                or configuration.preferences.decryption_enabled == liveflow_context.tlsDecryption
                or configuration.preferences.vlan_enabled == liveflow_context.vlanVxlanMplsAnalysis
                or configuration.preferences.web_enabled == liveflow_context.webAnalysis), (
            'Error in comparing LiveFlow configuration and LiveFlow context')


def actions_check(actions):
    for action in actions:
        if action is None:
            return False
    return True


@pytest.fixture(scope="module")
def notifications_notifications(engine):
    """Notifications on the capture engine."""
    return engine.get_notifications()


@pytest.fixture(scope="module")
def new_notifications():
    """New notifications."""
    disabledSources = []
    for source in NOTIFICATION_SOURCES:
        disabledSources.append(source)

    severities = []
    for severity in Severity:
        severities.append({'enabled': True, 'severity': severity})

    newNotifications = []

    # Email
    newNotifications.append({
        'authentiation': False,
        'clearPassword': '',
        'clsid': 'FF13FDFE-31BA-40DD-AB8A-77A85C3A439A',
        'disabledSources': disabledSources,
        'id': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFF0',
        'name': 'OS_Test_Email',
        'password': '',
        'port': 25,
        'recipient': 'someone@yahoo.com',
        'scheme': EmailScheme.SMTP,
        'sender': 'someone@yahoo.com',
        'server': 'smtp.somewhere.com',
        'severities': severities,
        'username': ''
    })
    # Execute
    newNotifications.append({
        'arguments': '',
        'clsid': '0D8DFB6C-237C-4ADE-8C37-E215D4F8CF00',
        'command': 'version',
        'directory': '/tmp',
        'disabledSources': disabledSources,
        'id': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFF1',
        'name': 'OS_Test_Execute',
        'severities': severities
    })
    # Log
    newNotifications.append({
        'clsid': 'B2DA6C79-C270-4988-8A20-995A0BB7A1CE',
        'disabledSources': disabledSources,
        'id': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFF2',
        'name': 'OS_Test_Log',
        'severities': severities
    })
    # SNMP Trap
    newNotifications.append({
        'clsid': 'ED19F042-0A45-44A6-9C47-E2A9D696881C',
        'community': 'public',
        'disabledSources': disabledSources,
        'id': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFF3',
        'name': 'OS_Test_SNMPTrap',
        'recipient': 'someone@yahoo.com',
        'severities': severities
    })
    # syslog
    newNotifications.append({
        'clsid': '5D3B11A5-993F-4B18-B603-F1799AD3736E',
        'destination': 'someone@yahoo.com',
        'disabledSources': disabledSources,
        'id': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFF4',
        'name': 'OS_Test_SysLog',
        'severities': severities
    })
    # Text Log
    newNotifications.append({
        'clsid': 'EF21EA89-80C3-4801-98F6-544677CF12D0',
        'currentFileCount': 1,
        'deleteFileCount': 0,
        'disabledSources': disabledSources,
        'fileCount': 1,
        'fileCountsEnabled': False,
        'fileName': 'notify',
        'fileNameAppend': '',
        'fileNameExtension': 'log',
        'filePath': '/tmp',
        'fileSize': 1,
        'fileSizesEnabled': False,
        'finished': False,
        'id': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFF5',
        'name': 'OS_Test_TextLog',
        'severities': severities,
        'totalFileSizes': 1
    })

    return newNotifications


@pytest.mark.api
@pytest.mark.order(5)
def test_get_notifications(notifications_notifications):
    """Verifies the notifications can be retrieved."""
    assert (notifications_notifications is not None
            and isinstance(notifications_notifications.actions, list)
            and actions_check(notifications_notifications.actions)
            and isinstance(notifications_notifications.modificationTime, six.string_types)), (
        'Error in getting notifications')


@pytest.mark.api
@pytest.mark.order(6)
def test_get_notification(engine, notifications_notifications):
    """Verifies a notification can be retrieved."""
    for action in notifications_notifications.actions:
        response = engine.get_notification(action.id)
        assert (response is not None
                and isinstance(response.actions, list)
                and actions_check(response.actions)
                and isinstance(response.modificationTime, six.string_types)), (
            f'Error in getting notification "{action.id}"')


@pytest.mark.api
@pytest.mark.order(7)
@pytest.mark.skip('Disabling all test.')
def test_set_notifications(engine, notifications_notifications):
    """Verifies the notifications can be set."""
    assert engine.set_notifications(notifications_notifications) is not None, (
        'Error in setting notifications')


@pytest.mark.api
@pytest.mark.order(8)
@pytest.mark.skip('Disabling all test.')
def test_add_notifications(engine, new_notifications):
    """Verifies a notification can be added."""
    for notification in new_notifications:
        assert engine.set_notification(notification['id'], notification) is not None, (
            'Error in adding notifications')


@pytest.mark.api
@pytest.mark.order(9)
@pytest.mark.skip('Disabling all test.')
def test_modify_notifications(engine, new_notifications):
    """Verifies a notification can be modified."""
    for notification in new_notifications:
        modifiedNotification = notification
        modifiedNotification['name'] += ' (Modified)'
        assert engine.set_notification(modifiedNotification['id'],
                                       modifiedNotification) is not None, (
            'Error in modifying notifications')


@pytest.mark.api
@pytest.mark.order(10)
@pytest.mark.skip('Disabling all test.')
def test_delete_notifications(engine, new_notifications):
    """Verifies notifications can be deleted."""
    for notification in new_notifications:
        assert engine.delete_notification(notification['id']) is not None, (
            'Error in deleting notifications')


@pytest.mark.api
@pytest.mark.skip('Skipping email')
def test_send_email(engine):
    """Verifies emails can be set."""
    email = {
        'body': 'This is a test email body.',
        'password': '',
        'port': 587,
        'recipients': '',
        'scheme': EmailScheme.SMTP_TLS,
        'sender': '',
        'server': '',
        'subject': 'This is a test email subject',
        'useAuthentication': False,
        'username': ''
    }
    assert engine.send_email(SendEmailRequest(email)) is not None, 'Error in sending emails'


@pytest.fixture(scope="module")
def test_notifications():
    """Test notifications."""
    testNotifications = {
        'notifications': [
            {
                'context': '00000000-0000-0000-0000-000000000000',
                'longMessage': 'Test: long description 1',
                'severity': Severity.INFORMATIONAL,
                'shortMessage': 'Test: short description 1',
                'source': '00000000-0000-0000-0000-000000000000',
                'sourceKey': 0,
                'timestamp': f'{datetime.datetime.now().isoformat()}Z',
            },
            {
                'context': '00000000-0000-0000-0000-000000000000',
                'longMessage': 'Test: long description 2',
                'severity': Severity.INFORMATIONAL,
                'shortMessage': 'Test: short description 2',
                'source': '00000000-0000-0000-0000-000000000000',
                'sourceKey': 0,
                'timestamp': f'{datetime.datetime.now().isoformat()}Z',
            }
        ]
    }
    return testNotifications


@pytest.mark.api
def test_send_notifications(engine, test_notifications):
    """Verifies notifications can be set."""
    assert engine.send_notifications(SendNotificationRequest(test_notifications)) is None, (
        'Error in sending notifications')
