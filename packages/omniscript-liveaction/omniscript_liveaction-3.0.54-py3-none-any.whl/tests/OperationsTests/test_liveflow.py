import pytest
from omniscript.liveflow import LiveFlow


@pytest.fixture(scope="module")
def liveflow(engine):
    """LiveFlow interface"""
    return LiveFlow(engine)


@pytest.fixture(scope="module")
def configuration(liveflow):
    """LiveFlow configuration."""
    return liveflow.get_liveflow_configuration()


@pytest.fixture(scope="module")
def liveflow_context(liveflow):
    """LiveFlow context."""
    return liveflow.get_liveflow_context()


@pytest.fixture(scope="module")
def liveflow_status(liveflow):
    """LiveFlow status."""
    return liveflow.get_liveflow_status()


@pytest.mark.api
@pytest.mark.order(1)
def test_get_liveflow_configuration(configuration):
    """Verifies the LiveFlow configuration can be retrieved."""
    assert (configuration is not None
            and configuration.preferences is not None
            and configuration.preferences.ipfix is not None), (
        'Error in getting LiveFlow configuration')


@pytest.mark.api
@pytest.mark.order(2)
def test_get_liveflow_configuration_services(configuration):
    """Verifies the services in LiveFlow configuration."""
    if configuration is not None:
        for service in configuration.services:
            assert service is not None, 'Error in LiveFlow configuration services'


@pytest.mark.api
@pytest.mark.order(3)
def test_get_liveflow_configuration_wan_mac_list(configuration):
    """Verifies the router map in LiveFlow configuration."""
    if (configuration is not None
            and configuration.preferences is not None
            and configuration.preferences.ipfix is not None):
        for wan_mac_list_item in configuration.preferences.ipfix.wan_mac_list:
            assert wan_mac_list_item is not None, 'Error in LiveFlow configuration router map'


@pytest.mark.api
@pytest.mark.order(4)
def test_set_liveflow_configuration(liveflow, configuration):
    """Verifies the LiveFlow configuration can be set."""
    assert liveflow.set_liveflow_configuration(
        configuration) is not None, 'Error in setting LiveFlow configuration'


@pytest.mark.api
def test_get_liveflow_context(liveflow_context):
    """Verifies LiveFlow context can be retrieved."""
    assert (liveflow_context is not None
            and liveflow_context.license is not None), 'Error in getting LiveFlow context'


@pytest.mark.api
def test_get_liveflow_status(liveflow_status):
    """Verifies LiveFlow status can be retrieved."""
    assert (liveflow_status is not None
            and liveflow_status.recordsSent is not None), 'Error in getting LiveFlow status'


@pytest.mark.api
def test_get_liveflow_status_hash_table(liveflow_status):
    """Verifies hash table in LiveFlow status."""
    if liveflow_status is not None:
        for hashTable in liveflow_status.hashTable:
            assert hashTable is not None, 'Error in LiveFlow status hash table'


@pytest.mark.api
@pytest.mark.skip('Disabling all test.')
def test_get_liveflow_configuration_context_match(configuration, liveflow_context):
    """Compares LiveFlow configuration and LiveFlow context."""
    if (configuration is not None
            and liveflow_context is not None
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
