"""LiveFlow class.
"""
# Copyright (c) LiveAction, Inc. 2022. All rights reserved.
# Copyright (c) Savvius, Inc. 2013-2019. All rights reserved.
# Copyright (c) WildPackets, Inc. 2013-2014. All rights reserved.

import json

from .invariant import EngineOperation as EO
from .invariant import LiveFlowFlowDirection, LiveFlowRecordType, LiveFlowTargetType
from .omniaddress import EthernetAddress
from .omnierror import OmniError
from .helpers import (
    load_native_props_from_list, load_props_from_dict, OmniScriptEncoder, repr_array)


class OmniEngine(object):
    pass


class Ipfix_15(object):
    """The Ipfix class has the attributes of LiveFlow IPFIX
    preferences.
    """

    active_flow_refresh_interval = 60
    """Indicates the time interval (in seconds) in which LiveFlow
    generates data records.
    """

    avc_enabled = True
    """Whether LiveFlow should generate AVC IPFIX records."""

    flowdir_enabled = True
    """Indicates whether the flowDirection key is sent in unidirectional
    IPFIX records indicating the flow direction:
    0 = ingress, 1 = egress.
    """

    fnf_enabled = True
    """Whether LiveFlow should generate FNF IPFIX records."""

    max_payload = 1500
    """The MTU of IPFIX packets."""

    medianet_enabled = True
    """Whether LiveFlow should generate MediaNet IPFIX records."""

    options_template_refresh_interval = 600
    """Indicates the time interval (in seconds) in which LiveFlow
    generates IPFIX option template records.
    """

    signaling_dn_enabled = True
    """Whether LiveFlow should generate Signaling DN IPFIX records."""

    template_refresh_interval = 600
    """Indicates the time interval (in seconds) in which LiveFlow
    generates IPFIX template records."""

    target_address = '127.0.0.1'
    """Indicates the location of the server instance receiving IPFIX
    records from LiveFlow:
    Option #1: An IP address,
    Option #2: An IP address and port in the following form:
    ip_address:port.
    """

    wan_mac_list = []
    """The LiveFlow router mappings."""

    _prop_list = [
        'active_flow_refresh_interval',
        'avc_enabled',
        'flowdir_enabled',
        'fnf_enabled',
        'max_payload',
        'medianet_enabled',
        'signaling_dn_enabled',
        'options_template_refresh_interval',
        'template_refresh_interval',
        'target_address'
    ]

    def __init__(self, props):
        self.active_flow_refresh_interval = Ipfix_15.active_flow_refresh_interval
        self.avc_enabled = Ipfix_15.avc_enabled
        self.flowdir_enabled = Ipfix_15.flowdir_enabled
        self.fnf_enabled = Ipfix_15.fnf_enabled
        self.medianet_enabled = Ipfix_15.medianet_enabled
        self.max_payload = Ipfix_15.max_payload
        self.options_template_refresh_interval = Ipfix_15.options_template_refresh_interval
        self.signaling_dn_enabled = Ipfix_15.signaling_dn_enabled
        self.target_address = Ipfix_15.target_address
        self.template_refresh_interval = Ipfix_15.template_refresh_interval
        self._load(props)

    def __repr__(self):
        return f'{self.__class__.__name__}({{{self._render()}}})'

    def __str__(self):
        return f'{self.__class__.__name__}({self._render()})'

    def _load(self, props):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            load_native_props_from_list(self, props, Ipfix_15._prop_list)
            wan_mac_list = props.get('wan_mac_list')
            if isinstance(wan_mac_list, list):
                self.wan_mac_list = []
                for v in wan_mac_list:
                    self.wan_mac_list.append(WanMac(v))

    def _render(self) -> str:
        return (
            f'active_flow_refresh_interval: {self.active_flow_refresh_interval}, '
            f'avc_enabled: {self.avc_enabled}, '
            f'flowdir_enabled: {self.flowdir_enabled}, '
            f'fnf_enabled: {self.fnf_enabled}, '
            f'max_payload: {self.max_payload}, '
            f'medianet_enabled: {self.medianet_enabled}, '
            f'options_template_refresh_interval: {self.options_template_refresh_interval}, '
            f'signaling_dn_enabled: {self.signaling_dn_enabled}, '
            f'target_address: "{self.target_address}", '
            f'template_refresh_interval: {self.template_refresh_interval}'
            f'wan_mac_list: [{repr_array(self.wan_mac_list)}]'
        )

    def _store(self, sort: bool = False):
        props = {k: getattr(self, k) for k in Ipfix_15._prop_list}
        return props if not sort else dict(sorted(props.items()))


class Ipfix_18(object):
    """The Ipfix class has the attributes of LiveFlow IPFIX
    preferences.
    """

    max_payload = 1500
    """The MTU of IPFIX packets."""

    options_template_refresh_interval = 600
    """Indicates the time interval (in seconds) in which LiveFlow
    generates IPFIX option template records.
    """

    template_refresh_interval = 600
    """Indicates the time interval (in seconds) in which LiveFlow
    generates IPFIX template records."""

    _prop_list = [
        'max_payload',
        'options_template_refresh_interval',
        'template_refresh_interval'
    ]

    def __init__(self, props):
        self.max_payload = Ipfix_18.max_payload
        self.options_template_refresh_interval = Ipfix_18.options_template_refresh_interval
        self.template_refresh_interval = Ipfix_18.template_refresh_interval
        self._load(props)

    def __repr__(self):
        return (
            f'{self.__class__.__name__}({{'
            f'max_payload: {self.max_payload}, '
            f'options_template_refresh_interval: {self.options_template_refresh_interval}, '
            f'template_refresh_interval: {self.template_refresh_interval}'
            f'}})'
        )

    def __str__(self):
        return (
            f'{self.__class__.__name__}('
            f'max_payload: {self.max_payload}, '
            f'options_template_refresh_interval: {self.options_template_refresh_interval}, '
            f'template_refresh_interval: {self.template_refresh_interval}'
            f')'
        )

    def _load(self, props):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            load_native_props_from_list(self, props, Ipfix_18._prop_list)

    def _store(self, sort: bool = False):
        props = {k: getattr(self, k) for k in Ipfix_18._prop_list}
        return props if not sort else dict(sorted(props.items()))


class LiveFlowTarget(object):
    """The LiveFlow Output Target."""

    enabled = False
    """Whether this target should actively generate records."""

    format = ''
    """The format of the records sent to this target: ipfix, json,
    msgpack.
    """

    target_id = 0
    """Identifier for this target."""

    name = ''
    """Name of the target."""

    transport_protocol = LiveFlowTargetType.NONE
    """The transport protocol: kafka, tcp, udp, websocket."""

    def __init__(self):
        self.enabled = LiveFlowTarget.enabled
        self.format = LiveFlowTarget.format
        self.target_id = LiveFlowTarget.target_id
        self.name = LiveFlowTarget.name
        self.target_id = LiveFlowTarget.target_id

    def _load(self, props):
        if isinstance(props, dict):
            enabled = props.get('enabled')
            if enabled is not None:
                self.enabled = bool(enabled)
            format = props.get('format')
            if format is not None:
                self.format = format
            id = props.get('id')
            if id is not None:
                self.target_id = int(id)
            self.name = props.get('name')
            self.transport_protocol = props.get('transport_protocol')

    def _store(self) -> dict:
        props = {
            'enabled': self.enabled,
            'format': self.format,
            'id': self.target_id,
            'name': self.name,
            'transport_protocol': self.transport_protocol
        }
        return props


class LiveFlowKafkaTarget(LiveFlowTarget):
    """The LiveFlow Output Kafka Target."""

    address = ''
    """Indicates the location of the server instance receiving the
    records LiveFlow records.
    An IP address with an optional port number: ip_address:port
    The default port of 2055.
    """
    max_batch_size = 0

    def __init__(self, props: dict = None):
        super(LiveFlowKafkaTarget, self).__init__()
        self.address = LiveFlowKafkaTarget.address
        self.max_batch_size = LiveFlowKafkaTarget.max_batch_size
        self._load(props)

    def _load(self, props: dict):
        super(LiveFlowKafkaTarget, self)._load(props)
        if isinstance(props, dict):
            self.address = props.get('address')
            batch_size = props.get('max_batch_size')
            if batch_size is not None:
                self.max_batch_size = int(batch_size)

    def _store(self, sort: bool = False) -> dict:
        props = super(LiveFlowKafkaTarget, self)._store()
        props['address'] = self.address
        props['max_batch_size'] = self.max_batch_size
        return props if not sort else dict(sorted(props.items()))


class LiveFlowTCPTarget(LiveFlowTarget):
    """The LiveFlow Output TCP Target."""

    address = ''
    """Indicates the location of the server instance receiving the
    records LiveFlow records.
    An IP address with an optional port number: ip_address:port
    The default port of 2055.
    """

    def __init__(self, props: dict = None):
        super(LiveFlowTCPTarget, self).__init__()
        self.address = LiveFlowTCPTarget.address
        self._load(props)

    def _load(self, props: dict):
        super(LiveFlowTCPTarget, self)._load(props)
        if isinstance(props, dict):
            self.address = props.get('address')

    def _store(self, sort: bool = False) -> dict:
        props = super(LiveFlowTCPTarget, self)._store()
        props['address'] = self.address
        return props if not sort else dict(sorted(props.items()))


class LiveFlowUDPTarget(LiveFlowTarget):
    """The LiveFlow Output UPD Target."""

    address = ''
    """Indicates the location of the server instance receiving the
    records LiveFlow records.
    An IP address with an optional port number: ip_address:port
    The default port of 2055.
    """

    def __init__(self, props: dict = None):
        super(LiveFlowUDPTarget, self).__init__()
        self.address = LiveFlowUDPTarget.address
        self._load(props)

    def _load(self, props: dict):
        super(LiveFlowUDPTarget, self)._load(props)
        if isinstance(props, dict):
            self.address = props.get('address')

    def _store(self, sort: bool = False) -> dict:
        props = super(LiveFlowUDPTarget, self)._store()
        props['address'] = self.address
        return props if not sort else dict(sorted(props.items()))


class LiveFlowWebSocketTarget(LiveFlowTarget):
    """The LiveFlow Output Web Socket Target."""

    api_key = ''
    """The authentication key for the websocket transport protocol.
    Must be between 32 and 64 characters (inclusive).
    """

    compression_enabled = False
    """Whether LiveFlow should compress records."""

    max_batch_size = 0
    """Indicates the maximum number of bytes in a batch of records prior
    to compression.
    """

    ssl_host = ''
    """The SSL Host."""

    ssl_uri = ''
    """The SSL URI."""

    def __init__(self, props: dict = None):
        super(LiveFlowWebSocketTarget, self).__init__()
        self.api_key = LiveFlowWebSocketTarget.api_key
        self.compression_enabled = LiveFlowWebSocketTarget.compression_enabled
        self.max_batch_size = LiveFlowWebSocketTarget.max_batch_size
        self.ssl_host = LiveFlowWebSocketTarget.ssl_host
        self.ssl_uri = LiveFlowWebSocketTarget.ssl_uri
        self._load(props)

    def _load(self, props: dict):
        super(LiveFlowWebSocketTarget, self)._load(props)
        if isinstance(props, dict):
            self.api_key = props.get('api_key')
            compression = props.get('compression_enabled')
            if compression is not None:
                self.compression_enabled = bool(compression)
            batch_size = props.get('max_batch_size')
            if batch_size is not None:
                self.max_batch_size = int(batch_size)
            self.ssl_host = props.get('ssl_host')
            self.ssl_uri = props.get('ssl_uri')

    def _store(self, sort: bool = False) -> dict:
        props = super(LiveFlowWebSocketTarget, self)._store()
        props['api_key'] = self.api_key
        props['compression_enabled'] = self.compression_enabled
        props['max_batch_size'] = self.max_batch_size
        props['ssl_host'] = self.ssl_host
        props['ssl_uri'] = self.ssl_uri
        return props if not sort else dict(sorted(props.items()))


class LiveFlowRecord(object):
    """The LiveFlow Preferences Output record."""

    record_type = LiveFlowRecordType.NONE
    """The type of recourd: AVC, Financial Service, FNF, Signal DN,
    SNA.
    """

    target_list = None
    """A list of target ids that should generate this record type."""

    def __init__(self):
        self.record_type = LiveFlowRecord.record_type
        self.target_list = LiveFlowRecord.target_list

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}({{'
            f'record_type: {self.record_type.label()}, '
            f'target_list: {self.target_list}'
            f'}})'
        )

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'record_type: {self.record_type.label()}, '
            f'target_list: {self.target_list}'
            f')'
        )

    def _load(self, props: dict):
        if isinstance(props, dict):
            record_type = props.get('type')
            if record_type:
                index = LiveFlowRecordType._json.index(record_type)
                self.record_type = LiveFlowRecordType._value2member_map_[index]
            targets = props.get('targets')
            if isinstance(targets, list):
                self.target_list = [int(t) for t in targets]

    def _store(self) -> dict:
        props = {
            'targets': [target for target in self.target_list],
            'type': self.record_type.json()
        }
        return props


class LiveFlowAVCRecord(LiveFlowRecord):
    """The LiveFlow Preferences Output avc record."""

    record_type = LiveFlowRecordType.AVC
    """This is a AVC LiveFlow Record"""

    flow_direction = LiveFlowFlowDirection.INGRESS
    """Indicates whether the flowDirection key is sent in unidirectional
    records indicating the flow direction:
    egress  : LiveFlowFlowDirection.EGRESS (1)
    ingress : LiveFlowFlowDirection.INGRESS (0)
    """

    def __init__(self, props: dict = None):
        super(LiveFlowAVCRecord, self).__init__()
        self.flow_direction = LiveFlowAVCRecord.flow_direction
        self._load(props)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({{{self._render()}}})'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self._render()})'

    def _load(self, props: dict):
        super(LiveFlowAVCRecord, self)._load(props)
        if isinstance(props, dict):
            flow_dir = props.get('flowdir_enabled')
            if flow_dir is not None:
                self.flow_direction = (LiveFlowFlowDirection.EGRESS if flow_dir else
                                       LiveFlowFlowDirection.INGRESS)

    def _render(self) -> str:
        return (
            f'record_type: {self.record_type.label()}, '
            f'flow_direction: {self.flow_direction.label()}, '
            f'target_list: {self.target_list}'
        )

    def _store(self, sort: bool = False) -> dict:
        props = super(LiveFlowAVCRecord, self)._store()
        # props[type] = LiveFlowRecordType.AVC.lable()
        props['flowdir_enabled'] = bool(self.flow_direction.value)
        return props if not sort else dict(sorted(props.items()))


class LiveFlowFinancialServicesRecord(LiveFlowRecord):
    """The LiveFlow Preferences Output Financial Service record."""

    record_type = LiveFlowRecordType.FINANCIAL_SERVICES
    """This is a Financial Services LiveFlow Record"""

    def __init__(self, props: dict = None):
        super(LiveFlowFinancialServicesRecord, self).__init__()
        super(LiveFlowFinancialServicesRecord, self)._load(props)

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}({{'
            f'record_type: {self.record_type.label()}, '
            f'target_list: {self.target_list}'
            f'}})'
        )

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'record_type: {self.record_type.label()}, '
            f'target_list: {self.target_list}'
            f')'
        )

    def _store(self, sort: bool = False) -> dict:
        props = super(LiveFlowFinancialServicesRecord, self)._store()
        # props[type] = LiveFlowRecordType.AVC.lable()
        return props if not sort else dict(sorted(props.items()))


class LiveFlowFNFRecord(LiveFlowRecord):
    """The LiveFlow Preferences Output fnf record."""

    record_type = LiveFlowRecordType.FNF
    """This is a FNF LiveFlow Record"""

    flow_direction = LiveFlowFlowDirection.INGRESS
    """Indicates whether the flowDirection key is sent in unidirectional
    records indicating the flow direction:
    egress  : LiveFlowFlowDirection.EGRESS (1)
    ingress : LiveFlowFlowDirection.INGRESS (0)
    """

    flow_time_interval_enabled = False
    """Whether flow time is relative to intervals (true) or flow
    packets (false).
    """

    def __init__(self, props: dict = None):
        super(LiveFlowFNFRecord, self).__init__()
        self.flow_direction = LiveFlowFNFRecord.flow_direction
        self.flow_time_interval_enabled = LiveFlowFNFRecord.flow_time_interval_enabled
        self._load(props)

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}({{'
            f'record_type: {self.record_type.label()}, '
            f'flow_direction: {self.flow_direction.label()}, '
            f'flow_time_interval_enabled: {self.flow_time_interval_enabled}, '
            f'target_list: {self.target_list}'
            f'}})'
        )

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'record_type: {self.record_type.label()}, '
            f'flow_direction: {self.flow_direction.label()}, '
            f'flow_time_interval_enabled: {self.flow_time_interval_enabled}, '
            f'target_list: {self.target_list}'
            f')'
        )

    def _load(self, props: dict):
        super(LiveFlowFNFRecord, self)._load(props)
        if isinstance(props, dict):
            flow_dir = props.get('flowdir_enabled')
            if flow_dir is not None:
                self.flow_direction = (LiveFlowFlowDirection.EGRESS if flow_dir else
                                       LiveFlowFlowDirection.INGRESS)
            time_interval = props.get('flow_time_interval')
            if isinstance(time_interval, bool):
                self.flow_time_interval_enabled = bool(time_interval)

    def _store(self, sort: bool = False) -> dict:
        props = super(LiveFlowFNFRecord, self)._store()
        # props[type] = LiveFlowRecordType.FNF.lable()
        props['flow_time_interval'] = self.flow_time_interval_enabled
        props['flowdir_enabled'] = bool(self.flow_direction)
        return props if not sort else dict(sorted(props.items()))


class LiveFlowMediaNetRecord(LiveFlowRecord):
    """The LiveFlow Preferences Output MediaNet record."""

    record_type = LiveFlowRecordType.MEDIANET
    """This is a Media Net LiveFlow Record"""

    flow_direction = LiveFlowFlowDirection.INGRESS
    """Indicates whether the flowDirection key is sent in unidirectional
    records indicating the flow direction:
    egress  : LiveFlowFlowDirection.EGRESS (1)
    ingress : LiveFlowFlowDirection.INGRESS (0)
    """

    def __init__(self, props: dict = None):
        super(LiveFlowMediaNetRecord, self).__init__()
        self.flow_direction = LiveFlowMediaNetRecord.flow_direction
        self._load(props)

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}({{'
            f'record_type: {self.record_type.label()}, '
            f'flow_direction: {self.flow_direction.label()}, '
            f'target_list: {self.target_list}'
            f'}})'
        )

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'record_type: {self.record_type.label()}, '
            f'flow_direction: {self.flow_direction.label()}, '
            f'target_list: {self.target_list}'
            f')'
        )

    def _load(self, props: dict):
        super(LiveFlowMediaNetRecord, self)._load(props)
        if isinstance(props, dict):
            flow_dir = props.get('flowdir_enabled')
            if flow_dir is not None:
                self.flow_direction = (LiveFlowFlowDirection.EGRESS if flow_dir else
                                       LiveFlowFlowDirection.INGRESS)

    def _store(self, sort: bool = False) -> dict:
        props = super(LiveFlowMediaNetRecord, self)._store()
        # props[type] = LiveFlowRecordType.MEDIANET.lable()
        props['flowdir_enabled'] = bool(self.flow_direction)
        return props if not sort else dict(sorted(props.items()))


class LiveFlowPlatformRecord(LiveFlowRecord):
    """The LiveFlow Preferences Platform Platform record."""

    record_type = LiveFlowRecordType.PLATFORM
    """This is a Platform LiveFlow Record"""

    flow_direction = LiveFlowFlowDirection.INGRESS
    """Indicates whether the flowDirection key is sent in unidirectional
    records indicating the flow direction:
    egress  : LiveFlowFlowDirection.EGRESS (1)
    ingress : LiveFlowFlowDirection.INGRESS (0)
    """

    def __init__(self, props: dict = None):
        super(LiveFlowPlatformRecord, self).__init__()
        self.flow_direction = LiveFlowPlatformRecord.flow_direction
        self._load(props)

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}({{'
            f'record_type: {self.record_type.label()}, '
            f'flow_direction: {self.flow_direction.label()}, '
            f'target_list: {self.target_list}'
            f'}})'
        )

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'record_type: {self.record_type.label()}, '
            f'flow_direction: {self.flow_direction.label()}, '
            f'target_list: {self.target_list}'
            f')'
        )

    def _load(self, props: dict):
        super(LiveFlowPlatformRecord, self)._load(props)
        if isinstance(props, dict):
            flow_dir = props.get('flowdir_enabled')
            if flow_dir is not None:
                self.flow_direction = (LiveFlowFlowDirection.EGRESS if flow_dir else
                                       LiveFlowFlowDirection.INGRESS)

    def _store(self, sort: bool = False) -> dict:
        props = super(LiveFlowPlatformRecord, self)._store()
        # props[type] = LiveFlowRecordType.PLATFORM.lable()
        props['flowdir_enabled'] = bool(self.flow_direction)
        return props if not sort else dict(sorted(props.items()))


class LiveFlowSignalingDNRecord(LiveFlowRecord):
    """The LiveFlow Preferences Output Signaling DN record."""

    record_type = LiveFlowRecordType.SIGNALING_DN
    """This is a Signaling DN LiveFlow Record"""

    def __init__(self, props: dict = None):
        super(LiveFlowSignalingDNRecord, self).__init__()
        super(LiveFlowSignalingDNRecord, self)._load(props)

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}({{'
            f'record_type: {self.record_type.label()}, '
            f'target_list: {self.target_list}'
            f'}})'
        )

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'record_type: {self.record_type.label()}, '
            f'target_list: {self.target_list}'
            f')'
        )

    def _store(self, sort: bool = False) -> dict:
        props = super(LiveFlowSignalingDNRecord, self)._store()
        # props[type] = LiveFlowRecordType.SIGNALING_DN.lable()
        return props if not sort else dict(sorted(props.items()))


class LiveFlowSNARecord(LiveFlowRecord):
    """The LiveFlow Preferences Output SNA record."""

    record_type = LiveFlowRecordType.SNA
    """This is a SNA LiveFlow Record"""

    byte_distribution_enabled = False
    """Whether LiveFlow should perform byte distribution analysis."""

    first_data_packet_enabled = False
    """Whether LiveFlow should include the payload of the first packet
    of a flow in the records.
    """

    split_enabled = False
    """Whether LiveFlow should perform SPLT analysis."""

    def __init__(self, props: dict = None):
        super(LiveFlowSNARecord, self).__init__()
        self.byte_distribution_enabled = LiveFlowSNARecord.byte_distribution_enabled
        self.first_data_packet_enabled = LiveFlowSNARecord.first_data_packet_enabled
        self.split_enabled = LiveFlowSNARecord.split_enabled
        self._load(props)

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}({{'
            f'record_type: {self.record_type.label()}, '
            f'byte_distribution_enabled: {self.byte_distribution_enabled}, '
            f'first_data_packet_enabled: {self.first_data_packet_enabled}, '
            f'split_enabled: {self.split_enabled}, '
            f'target_list: {self.target_list}'
            f'}})'
        )

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'record_type: {self.record_type.label()}, '
            f'byte_distribution_enabled: {self.byte_distribution_enabled}, '
            f'first_data_packet_enabled: {self.first_data_packet_enabled}, '
            f'split_enabled: {self.split_enabled}, '
            f'target_list: {self.target_list}'
            f')'
        )

    def _load(self, props: dict):
        super(LiveFlowSNARecord, self)._load(props)
        if isinstance(props, dict):
            byte_dist = props.get('byte_distribution_enabled')
            if isinstance(byte_dist, bool):
                self.byte_distribution_enabled = bool(byte_dist)
            first_packet = props.get('first_data_pkt_enabled')
            if isinstance(first_packet, bool):
                self.first_data_packet_enabled = bool(first_packet)
            split = props.get('splt_enabled')
            if isinstance(split, bool):
                self.split_enabled = bool(split)

    def _store(self, sort: bool = False) -> dict:
        props = super(LiveFlowSNARecord, self)._store()
        # props[type] = LiveFlowRecordType.SNA.lable()
        props['byte_distribution_enabled'] = self.byte_distribution_enabled
        props['first_data_pkt_enabled'] = self.first_data_packet_enabled
        props['splt_enabled'] = self.split_enabled
        return props if not sort else dict(sorted(props.items()))


class LiveFlowConfigurationOutput(object):
    record_list = None
    target_list = None

    def __init__(self, props: dict):
        self.record_list = LiveFlowConfigurationOutput.record_list
        self.target_list = LiveFlowConfigurationOutput.target_list
        self._load(props)

    def _load(self, props):
        if isinstance(props, dict):
            record_types = props.get('record_types')
            if isinstance(record_types, list):
                self.record_list = []
                for record in record_types:
                    record_type = record.get('type')
                    if record_type == LiveFlowRecordType.AVC.json():
                        self.record_list.append(LiveFlowAVCRecord(record))
                    elif record_type == LiveFlowRecordType.FINANCIAL_SERVICES.json():
                        self.record_list.append(
                            LiveFlowFinancialServicesRecord(record))
                    elif record_type == LiveFlowRecordType.FNF.json():
                        self.record_list.append(LiveFlowFNFRecord(record))
                    elif record_type == LiveFlowRecordType.MEDIANET.json():
                        self.record_list.append(LiveFlowMediaNetRecord(record))
                    elif record_type == LiveFlowRecordType.PLATFORM.json():
                        self.record_list.append(LiveFlowPlatformRecord(record))
                    elif record_type == LiveFlowRecordType.SIGNALING_DN.json():
                        self.record_list.append(LiveFlowSignalingDNRecord(record))
                    elif record_type == LiveFlowRecordType.SNA.json():
                        self.record_list.append(LiveFlowSNARecord(record))
                    else:
                        # TODO: Log the unknown type
                        pass
            targets = props.get('targets')
            if isinstance(targets, list):
                self.target_list = []
                for target in targets:
                    target_type = target.get('transport_protocol')
                    if target_type == LiveFlowTargetType.KAFKA.json():
                        self.target_list.append(LiveFlowKafkaTarget(target))
                    elif target_type == LiveFlowTargetType.TCP.json():
                        self.target_list.append(LiveFlowTCPTarget(target))
                    elif target_type == LiveFlowTargetType.UDP.json():
                        self.target_list.append(LiveFlowUDPTarget(target))
                    elif target_type == LiveFlowTargetType.WEBSOCKET.json():
                        self.target_list.append(LiveFlowWebSocketTarget(target))

    def _store(self, sort: bool = False) -> dict:
        props = {
            'record_types': [record._store(sort) for record in self.record_list],
            'targets': [target._store(sort) for target in self.target_list]
        }
        return props if not sort else dict(sorted(props.items()))


class WanMac(object):
    """The WanMac class has the attributes of a LiveFlow router
    map entry.
    """

    if_index = 1
    """The if index of an adapter."""

    if_name = ''
    """The interface name of an adapter."""

    ethernet_address = None
    """The Ethernet Address of an adapter."""

    mpls_label = ''
    """The MPLS Label."""

    vlan_id = 0
    """The VLAN Identifier."""

    vxlan_network_id = 0
    """The VXLAN network identifier."""

    _wan_mac_dict = {
        'ifidx': 'if_index',
        'ifname': 'if_name',
        'mac': 'ethernet_address',
        'mpls_label': 'mpls_label',
        'vlan_id': 'vlan_id',
        'vxlan_vni': 'vxlan_network_id'
    }

    def __init__(self, props):
        self.if_index = WanMac.if_index
        self.if_name = WanMac.if_name
        self.ethernet_address = WanMac.ethernet_address
        self.mpls_label = WanMac.mpls_label
        self.vlan_id = WanMac.vlan_id
        self.vxlan_network_id = WanMac.vxlan_network_id
        self._load(props)

    def __repr__(self):
        return (
            f'{self.__class__.__name__}({{'
            f'if_index: {self.if_index}, '
            f'if_name: "{self.if_name}", '
            f'ethernet_address: {self.ethernet_address}',
            f'mpls_label: "{self.mpls_label}"',
            f'vlan_id: {self.vlan_id}',
            f'vxlan_network_id: {self.vxlan_network_id}'
            f'}})'
        )

    def __str__(self):
        return (
            f'{self.__class__.__name__}('
            f'if_index: {self.if_index}, '
            f'if_name: "{self.if_name}", '
            f'ethernet_address: {self.ethernet_address}',
            f'mpls_label: "{self.mpls_label}"',
            f'vlan_id: {self.vlan_id}',
            f'vxlan_network_id: {self.vxlan_network_id}'
            f')'
        )

    def _load(self, props):
        """Set attributes from a dictionary."""
        load_props_from_dict(self, props, WanMac._wan_mac_dict)
        if isinstance(props, dict):
            eth_addr = props.get('mac')
            if eth_addr:
                self.ethernet_address = EthernetAddress(eth_addr)

    def _store(self):
        props = {
            'ifidx': self.if_index,
            'ifname': self.if_name,
            'mac': self.ethernet_address.format(),
            'mpls_label': self.mpls_label,
            'vlan_id': self.vlan_id,
            'vxlan_vni': self.vxlan_network_id
        }
        return props


class LiveFlowPreferences(object):
    """The LiveFlowPreferences class has the attributes of LiveFlow
    preferences.
    """

    active_flow_refresh_interval = 0
    """Indicates the time interval (in seconds) in which LiveFlow
    generates data records.
    """

    config_check_interval = 1000
    """The time interval (in milliseconds) at which LiveFlow should
    check for updates in the configuration file.
    """

    debug_logging = 0
    """Indicates how much debug logging to display in the log files:
    0 = None, 1 = Low, 2 = Medium, 3 = High, 4 = Verbose.
    """

    decryption_enabled = False
    """Whether LiveFlow performs decryption for HTTPS packets."""

    dhcp_analysis = False
    """Whether LiveFlow performs analysis for DHCP packets."""

    dns_analysis = False
    """Whether LiveFlow perform dns analysis."""

    eta_debug_logging = False
    """Whether LiveFlow should display ETA records in the log file for
    encrypted traffic analysis.
    """

    enforce_tcp_3way_handshake = False
    """Whether LiveFlow requires a 3-way handshake (SYN, SYN-ACK, ACK)
    for a TCP flow in order for it to be included in processing and
    analyzing.
    """

    flow_id = 0
    """The starting flow id."""

    hashtable_size = 0
    """Indicates the total number of active flows expected at any one
    time per stream (a value of 0 indicates that LiveFlow will
    auto-determine the correct value).
    """

    hostname_analysis = True
    """Whether LiveFlow performs hostname analysis."""

    https_port = 443
    """The HTTPS port."""

    ipfix = None
    """IPFIX preferences."""

    latency_enabled = True
    """Whether LiveFlow performs latency analysis."""

    quality_enabled = True
    """Whether LiveFlow performs TCP quality analysis."""

    retransmissions_enabled = True
    """Whether LiveFlow performs TCP retransmission analysis."""

    rtp_enabled = True
    """Whether LiveFlow performs RTP analysis."""

    rtp_packets_disabled = False
    """Whether LiveFlow ignores RTP packets."""

    signaling_packet_window = 0
    """Indicates how many packets per SIP flow should be run through the
    SIP analysis; LiveFlow will analyze the first number of indicated
    packets and then ignore the rest that follow (0 = unlimited).
    """

    tcp_handshake_timeout = 2000
    """Indicates the maximum amount of time (in milliseconds) to allow
    between packets in a TCP flow while waiting for a 3-Way handshake to
    complete before considering the current flow complete and starting a
    new flow (ignored if enforce_tcp_3way_handshake key is false).
    """

    tcp_orphan_timeout = 60000
    """Indicates the maximum amount of time (in milliseconds) to allow
    between packets in a TCP flow after receiving a 3-Way handshake (if
    the enforce_tcp_3way_handshake key is true) and before the flow has
    begun to close (before a FIN is seen) before considering the current
    flow complete and starting a new flow.
    """

    tcp_packets_disabled = False
    """Whether LiveFlow ignores TCP packets."""

    tcp_post_close_timeout = 1000
    """Indicates the maximum amount of time (in milliseconds) to keep a
    flow in the hash table after it has been completed.
    """

    tcp_wait_timeout = 3000
    """Indicates the maximum amount of time (in milliseconds) to allow
    between packets in a TCP flow while waiting for the flow to close
    (after the first FIN is seen) before considering the current flow
    complete and starting a new flow.
    """

    tls_analysis = True
    """Whether LiveFlow performs TLS analysis."""

    tls_packet_window = 16
    """Indicates how many packets per HTTPS flow should be looked at for
    TLS information.
    """

    udp_packets_disabled = False
    """Whether LiveFlow ignores UDP packets."""

    udp_wait_timeout = 3000
    """Indicates the maximum amount of time (in milliseconds) to allow
    between packets in a UDP flow before considering the current flow
    complete and starting a new flow.
    """

    vlan_enabled = True
    """Whether LiveFlow performs VLAN/VXLAN/MPLS analysis."""

    voip_quality_percent = 25
    """Represents a percentage indicating how strongly to weight the
    average VoIP quality score vs the worst VoIP quality score when
    computing the MOS score (0 means the score is based completely on
    the worst score, and 100 means that the score is based completely on
    the average).
    """

    wan_mac_list = None
    """List of WanMac items."""

    web_enabled = False
    """Whether LiveFlow performs web analysis."""

    # Legacy

    # flow_time_ipfix = False
    # """Whether IPFIX flow time is relative to IPFIX intervals (True) or
    # flow packets (False).
    # """

    _preferences_prop_list = [
        'active_flow_refresh_interval',
        'config_check_interval',
        'debug_logging',
        'decryption_enabled',
        'dhcp_analysis',
        'dns_analysis',
        'enforce_tcp_3way_handshake',
        'flow_id',
        'hashtable_size',
        'hostname_analysis',
        'https_port',
        'latency_enabled',
        'quality_enabled',
        'retransmissions_enabled',
        'rtp_enabled',
        'rtp_packets_disabled',
        'signaling_packet_window',
        'tcp_handshake_timeout',
        'tcp_orphan_timeout',
        'tcp_packets_disabled',
        'tcp_post_close_timeout',
        'tcp_wait_timeout',
        'tls_analysis',
        'tls_packet_window',
        'udp_packets_disabled',
        'udp_wait_timeout',
        'vlan_enabled',
        'voip_quality_percent',
        'web_enabled'
    ]

    def __init__(self, props):
        self.active_flow_refresh_interval = LiveFlowPreferences.active_flow_refresh_interval
        self.config_check_interval = LiveFlowPreferences.config_check_interval
        self.debug_logging = LiveFlowPreferences.debug_logging
        self.decryption_enabled = LiveFlowPreferences.decryption_enabled
        self.dhcp_analysis = LiveFlowPreferences.dhcp_analysis
        self.dns_analysis = LiveFlowPreferences.dns_analysis
        self.enforce_tcp_3way_handshake = LiveFlowPreferences.enforce_tcp_3way_handshake
        self.eta_debug_logging = LiveFlowPreferences.eta_debug_logging
        self.flow_id = LiveFlowPreferences.flow_id
        self.hashtable_size = LiveFlowPreferences.hashtable_size
        self.hostname_analysis = LiveFlowPreferences.hostname_analysis
        self.https_port = LiveFlowPreferences.https_port
        self.ipfix = LiveFlowPreferences.ipfix
        self.latency_enabled = LiveFlowPreferences.latency_enabled
        self.quality_enabled = LiveFlowPreferences.quality_enabled
        self.retransmissions_enabled = LiveFlowPreferences.retransmissions_enabled
        self.rtp_enabled = LiveFlowPreferences.rtp_enabled
        self.rtp_packets_disabled = LiveFlowPreferences.rtp_packets_disabled
        self.signaling_packet_window = LiveFlowPreferences.signaling_packet_window
        self.tcp_handshake_timeout = LiveFlowPreferences.tcp_handshake_timeout
        self.tcp_orphan_timeout = LiveFlowPreferences.tcp_orphan_timeout
        self.tcp_packets_disabled = LiveFlowPreferences.tcp_packets_disabled
        self.tcp_post_close_timeout = LiveFlowPreferences.tcp_post_close_timeout
        self.tcp_wait_timeout = LiveFlowPreferences.tcp_wait_timeout
        self.tls_analysis = LiveFlowPreferences.tls_analysis
        self.tls_packet_window = LiveFlowPreferences.tls_packet_window
        self.udp_packets_disabled = LiveFlowPreferences.udp_packets_disabled
        self.udp_wait_timeout = LiveFlowPreferences.udp_wait_timeout
        self.vlan_enabled = LiveFlowPreferences.vlan_enabled
        self.voip_quality_percent = LiveFlowPreferences.voip_quality_percent
        self.wan_mac_list = []
        self.web_enabled = LiveFlowPreferences.web_enabled
        self._load(props)

    def __repr__(self):
        return f'{self.__class__.__name__}({{{self._render()}}})'

    def __str__(self):
        return f'{self.__class__.__name__}({self._render()})'

    def _load(self, props):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            load_native_props_from_list(self, props, LiveFlowPreferences._preferences_prop_list)
            encrypted_traffic = props.get('encrypted_traffic_analysis')
            if isinstance(encrypted_traffic, dict):
                eta_debug_logging = encrypted_traffic.get('eta_debug_logging')
                if eta_debug_logging is not None:
                    self.eta_debug_logging = bool(eta_debug_logging)
            ipfix = props.get('ipfix')
            if isinstance(ipfix, dict):
                self.ipfix = Ipfix_18(ipfix)
            wan_mac_list = props.get('wan_mac_list')
            if isinstance(wan_mac_list, list):
                self.wan_mac_list = [WanMac(wan_mac) for wan_mac in wan_mac_list]

    def _render(self) -> str:
        return (
            f'active_flow_refresh_interval: {self.active_flow_refresh_interval}, '
            f'config_check_interval: {self.config_check_interval}, '
            f'debug_logging: {self.debug_logging}, '
            f'decryption_enabled: {self.decryption_enabled}, '
            f'dns_analysis={self.dns_analysis}',
            f'enforce_tcp_3way_handshake: {self.enforce_tcp_3way_handshake}, '
            f'flow_id: {self.flow_id}, '
            f'hashtable_size: {self.hashtable_size}, '
            f'hostname_analysis: {self.hostname_analysis}, '
            f'https_port: {self.https_port}, '
            f'ipfix: {{{repr(self.ipfix)}}}, '
            f'latency_enabled: {self.latency_enabled}, '
            f'quality_enabled: {self.quality_enabled}, '
            f'retransmissions_enabled: {self.retransmissions_enabled}, '
            f'rtp_enabled: {self.rtp_enabled}, '
            f'rtp_packets_disabled: {self.rtp_packets_disabled}, '
            f'signaling_packet_window: {self.signaling_packet_window}, '
            f'tcp_handshake_timeout: {self.tcp_handshake_timeout}, '
            f'tcp_orphan_timeout: {self.tcp_orphan_timeout}, '
            f'tcp_packets_disabled: {self.tcp_packets_disabled}, '
            f'tcp_post_close_timeout: {self.tcp_post_close_timeout}, '
            f'tcp_wait_timeout: {self.tcp_wait_timeout}, '
            f'tls_analysis: {self.tls_analysis}, '
            f'tls_packet_window: {self.tls_packet_window}, '
            f'udp_packets_disabled: {self.udp_packets_disabled}, '
            f'udp_wait_timeout: {self.udp_wait_timeout}, '
            f'vlan_enabled: {self.vlan_enabled}, '
            f'voip_quality_percent: {self.voip_quality_percent}, '
            f'wan_mac_list: {self.wan_mac_list} ,'
            f'web_enabled: {self.web_enabled}'
        )

    def _store(self, sort: bool = False):
        props = {k: getattr(self, k) for k in LiveFlowPreferences._preferences_prop_list}
        props['encrypted_traffic_analysis'] = {
            'eta_debug_logging': self.eta_debug_logging
        }
        if self.ipfix:
            props['ipfix'] = self.ipfix._store(sort)
        props['wan_mac_list'] = [wan_mac._store() for wan_mac in self.wan_mac_list]
        return props if not sort else dict(sorted(props.items()))

    @classmethod
    def version(self):
        return 18


class LiveFlowConfiguration(object):
    """The LiveFlowConfiguration class has the attributes of LiveFlow
    configuration.
    """

    output = None
    """"LiveFlow Configuration Output."""

    preferences = None
    """LiveFlow Configuration Preferences."""

    version = 0
    """LiveFlow Configuration version."""

    def __init__(self, props):
        self.output = LiveFlowConfiguration.output
        self.preferences = LiveFlowConfiguration.preferences
        self.version = LiveFlowConfiguration.version
        self._load(props)

    def __repr__(self):
        return (
            f'{self.__class__.__name__}({{'
            f'output: {{{repr(self.output)}}}, '
            f'preferences: {{{repr(self.preferences)}}}, '
            f'version: {self.version}'
            f'}})'
        )

    def __str__(self):
        return (
            f'{self.__class__.__name__}('
            f'output: {{{repr(self.output)}}}, '
            f'preferences: {{{repr(self.preferences)}}}, '
            f'version: {self.version}'
            f')'
        )

    def _load(self, props):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            version = props.get('version')
            if version is not None:
                self.version = int(version)
            if self.version == 18:
                output = props.get('output')
                self.output = LiveFlowConfigurationOutput(output)
                preferences = props.get('preferences')
                self.preferences = LiveFlowPreferences(preferences)

    def _store(self, sort: bool = False):
        props = {
            'version': getattr(self, 'version')
        }
        if self.output is not None:
            props['output'] = self.output._store(sort)
        if self.preferences is not None:
            props['preferences'] = self.preferences._store(sort)
        return props if not sort else dict(sorted(props.items()))


class LiveFlowLicense(object):
    """The LiveFlowLicense class has the attributes of LiveFlow
    licenses.
    """

    active_flow_count_limit = 0
    """The number of active flows that can be tracked at one time for a
    LiveFlow capture (0 = unlimited).
    """

    custom_settings_count = 0
    """The custom settings (0 = none)"""

    liveflow_enabled = False
    """Whether the Capture Engine supports LiveFlow."""

    threateye_enabled = False
    """Whether the Capture Engine supports ThreatEye."""

    _license_dict = {
        'activeFlowCountLimit': 'active_flow_count_limit',
        'customSettings': 'custom_settings_count',
        'liveFlowEnabled': 'liveflow_enabled',
        'threatEyeEnabled': 'threateye_enabled'
    }

    def __init__(self, props):
        self.active_flow_count_limit = LiveFlowLicense.active_flow_count_limit
        self.custom_settings_count = LiveFlowLicense.custom_settings_count
        self.liveflow_enabled = LiveFlowLicense.liveflow_enabled
        self.threateye_enabled = LiveFlowLicense.threateye_enabled
        self._load(props)

    def __repr__(self):
        return (
            f'{self.__class__.__name__}({{'
            f'active_flow_count_limit: {self.active_flow_count_limit}, '
            f'custom_settings_count: {self.custom_settings_count}, '
            f'liveflow_enabled: {self.liveflow_enabled} ',
            f'threateye_enabled: {self.threateye_enabled}'
            f'}})'
        )

    def __str__(self):
        return (
            f'{self.__class__.__name__}('
            f'active_flow_count_limit: {self.active_flow_count_limit}, '
            f'custom_settings_count: {self.custom_settings_count}, '
            f'liveflow_enabled: {self.liveflow_enabled} ',
            f'threateye_enabled: {self.threateye_enabled}'
            f')'
        )

    def _load(self, props):
        """Set attributes from a dictionary."""
        load_props_from_dict(self, props, LiveFlowLicense._license_dict)

    def _store(self):
        props = {}
        props['activeFlowCountLimit'] = self.active_flow_count_limit
        props['customSettings'] = self.custom_settings_count
        props['liveFlowEnabled'] = self.liveflow_enabled
        props['threatEyeEnabled'] = self.threateye_enabled


class LiveFlowContextAnalysis(object):
    decryption_enabled = False
    """Whether LiveFlow performs TLS (<= v1.2) Decryption"""

    dhcp_enabled = False
    """Whether LiveFlow performs DHCP analysis."""

    dns_enabled = False
    """Whether LiveFlow performs DNS analysis."""

    eta_distribution_entropy_enabled = False
    """Whether LiveFlow performs ETA byte distribution and
    entropy analysis.
    """

    hostname_enabled = False
    """Whether LiveFlow performs hostname analysis."""

    latency_enabled = False
    """Whether LiveFlow performs latency analysis."""

    mpls_vlan_vxlan_enabled = False
    """Whether LiveFlow performs MPLS/VLAN/VXLAN analysis."""

    rtp_enabled = False
    """Whether LiveFlow performs RTP analysis"""

    tcp_3way_handshake_enabled = False
    """Whether LiveFlow requires TCP flows to have a 3-way handshake."""

    tcp_quality_enabled = False
    """Whether LiveFlow performs TCP quality analysis."""

    tcp_retransmissions_enabled = False
    """Whether LiveFlow performs TCP retransmissions analysis."""

    tls_enabled = False
    """Whether LiveFlow performs TLS analysis."""

    web_enabled = False
    """Whether LiveFlow performs HTTP/1.N web analysis."""

    _context_analysis_dict = {
        'decryption': 'decryption_enabled',
        'dhcp': 'dhcp_enabled',
        'dns': 'dns_enabled',
        'etaEntropyBD': 'eta_distribution_entropy_enabled',
        'hostname': 'hostname_enabled',
        'latency': 'latency_enabled',
        'mplsVlanVxlan': 'mpls_vlan_vxlan_enabled',
        'rtp': 'rtp_enabled',
        'tcp3WayHandshakeEnforcement': 'tcp_3way_handshake_enabled',
        'tcpQuality': 'tcp_quality_enabled',
        'tcpRetransmissions': 'tcp_retransmissions_enabled',
        'tls': 'tls_enabled',
        'web': 'web_enabled'
    }

    def __init__(self, props: dict):
        self.decryption_enabled = LiveFlowContextAnalysis.decryption_enabled
        self.dhcp_enabled = LiveFlowContextAnalysis.dhcp_enabled
        self.dns_enabled = LiveFlowContextAnalysis.dns_enabled
        self.eta_distribution_entropy_enabled = (
            LiveFlowContextAnalysis.eta_distribution_entropy_enabled)
        self.hostname_enabled = LiveFlowContextAnalysis.hostname_enabled
        self.latency_enabled = LiveFlowContextAnalysis.latency_enabled
        self.mpls_vlan_vxlan_enabled = LiveFlowContextAnalysis.mpls_vlan_vxlan_enabled
        self.rtp_enabled = LiveFlowContextAnalysis.rtp_enabled
        self.tcp_3way_handshake_enabled = LiveFlowContextAnalysis.tcp_3way_handshake_enabled
        self.tcp_quality_enabled = LiveFlowContextAnalysis.tcp_quality_enabled
        self.tcp_retransmissions_enabled = LiveFlowContextAnalysis.tcp_retransmissions_enabled
        self.tls_enabled = LiveFlowContextAnalysis.tls_enabled
        self.web_enabled = LiveFlowContextAnalysis.web_enabled
        self._load(props)

    def _load(self, props: dict):
        load_props_from_dict(self, props, LiveFlowContextAnalysis._context_analysis_dict)


class LiveFlowContextOutput(object):
    avc_enabled = False
    """Whether LiveFlow generates AVC records."""

    sna_enabled = False
    """Whether LiveFlow generates Cisco SNA records."""

    financial_services_enabled = False
    """Whether LiveFlow generates Financial Services records."""

    fnf_enabled = False
    """Whether LiveFlow generates FNF records."""

    medianet_enabled = False
    """Whether LiveFlow generates MediaNet records."""

    platform_enabled = False
    """Whether LiveFlow generates Platform records."""

    signaling_dn_enabled = False
    """Whether LiveFlow generates Signaling DN records."""

    threateye_enabled = False
    """Whether LiveFlow generates ThreatEye records."""

    _context_output_dict = {
        'avc': 'avc_enabled',
        'ciscoSNA': 'sna_enabled',
        'financialServices': 'financial_services_enabled',
        'fnf': 'fnf_enabled',
        'mediaNet': 'medianet_enabled',
        'platform': 'platform_enabled',
        'signalingDN': 'signaling_dn_enabled',
        'threatEye': 'threateye_enabled'
    }

    def __init__(self, props: dict):
        self.avc_enabled = LiveFlowContextOutput.avc_enabled
        self.sna_enabled = LiveFlowContextOutput.sna_enabled
        self.financial_services_enabled = LiveFlowContextOutput.financial_services_enabled
        self.fnf_enabled = LiveFlowContextOutput.fnf_enabled
        self.medianet_enabled = LiveFlowContextOutput.medianet_enabled
        self.platform_enabled = LiveFlowContextOutput.platform_enabled
        self.signaling_dn_enabled = LiveFlowContextOutput.signaling_dn_enabled
        self.threateye_enabled = LiveFlowContextOutput.threateye_enabled
        self._load(props)

    def _load(self, props: dict):
        load_props_from_dict(self, props, LiveFlowContextOutput._context_output_dict)


class LiveFlowContext_15(object):
    """The LiveFlowContext class has the attributes of a LiveFlow
    context.
    """

    host_name_analysis = True
    """Whether LiveFlow performs hostname analysis."""

    ipfix_avc_output = True
    """Whether LiveFlow generates IPFIX AVC records."""

    ipfix_fnf_output = True
    """Whether LiveFlow generates IPFIX FNF records."""

    ipfix_medianet_output = True
    """Whether LiveFlow generates IPFIX MediaNet records."""

    ipfix_signaling_dn_output = True
    """Whether LiveFlow generates IPFIX Signaling DN records."""

    latency_analysis = True
    """Whether LiveFlow performs latency analysis."""

    license = None
    """LiveFlow license."""

    rtp_analysis = True
    """Whether LiveFlow performs RTP analysis."""

    tcp_3way_handshake_enforcement = True
    """Whether LiveFlow requires TCP flows to have a 3-way handshake."""

    tcp_quality_analysis = True
    """Whether LiveFlow performs TCP quality analysis."""

    tcp_retransmissions_analysis = True
    """Whether LiveFlow performs TCP retransmissions analysis."""

    tls_analysis = True
    """Whether LiveFlow performs TLS analysis."""

    tls_decryption = True
    """Whether LiveFlow performs TLS (<= v1.2) Decryption."""

    vlan_vxlan_mpls_analysis = True
    """Whether LiveFlow performs VLAN/VXLAN/MPLS analysis."""

    web_analysis = True
    """Whether LiveFlow performs HTTP/1.N web analysis."""

    _context_dict = {
        'hostnameAnalysis': 'host_name_analysis',
        'ipfixAVCOutput': 'ipfix_avc_output',
        'ipfixFNFOutput': 'ipfix_fnf_output',
        'ipfixMediaNetOutput': 'ipfix_medianet_output',
        'ipfixSignalingDNOutput': 'ipfix_signaling_dn_output',
        'latencyAnalysis': 'latency_analysis',
        'rtpAnalysis': 'rtp_analysis',
        'tcp3WayHandshakeEnforcement': 'tcp_3way_handshake_enforcement',
        'tcpQualityAnalysis': 'tcp_quality_analysis',
        'tcpRetransmissionsAnalysis': 'tcp_retransmissions_analysis',
        'tlsAnalysis': 'tls_analysis',
        'tlsDecryption': 'tls_decryption',
        'vlanVxlanMplsAnalysis': 'vlan_vxlan_mpls_analysis',
        'webAnalysis': 'web_analysis'
    }

    def __init__(self, props: dict):
        self.host_name_analysis = LiveFlowContext_15.host_name_analysis
        self.ipfix_avc_output = LiveFlowContext_15.ipfix_avc_output
        self.ipfix_fnf_output = LiveFlowContext_15.ipfix_fnf_output
        self.ipfix_medianet_output = LiveFlowContext_15.ipfix_medianet_output
        self.ipfix_signaling_dn_output = LiveFlowContext_15.ipfix_signaling_dn_output
        self.latency_analysis = LiveFlowContext_15.latency_analysis
        self.rtp_analysis = LiveFlowContext_15.rtp_analysis
        self.tcp_3way_handshake_enforcement = LiveFlowContext_15.tcp_3way_handshake_enforcement
        self.tcp_quality_analysis = LiveFlowContext_15.tcp_quality_analysis
        self.tcp_retransmissions_analysis = LiveFlowContext_15.tcp_retransmissions_analysis
        self.tls_analysis = LiveFlowContext_15.tls_analysis
        self.tls_decryption = LiveFlowContext_15.tls_decryption
        self.vlan_vxlan_mpls_analysis = LiveFlowContext_15.vlan_vxlan_mpls_analysis
        self.web_analysis = LiveFlowContext_15.web_analysis
        self._load(props)

    def __repr__(self):
        return f'{self.__class__.__name__}({{{self._render()}}})'

    def __str__(self):
        return f'{self.__class__.__name__}({self._render()})'

    def _load(self, props):
        """Set attributes from a dictionary."""
        load_props_from_dict(self, props, LiveFlowContext_15._context_dict)
        if isinstance(props, dict):
            license = props['license'] if 'license' in props.keys() else None
            if isinstance(license, dict):
                self.license = LiveFlowLicense(license)

    def _render(self) -> str:
        return (
            f'host_name_analysis: {self.host_name_analysis}, '
            f'ipfix_avc_output: {self.ipfix_avc_output}, '
            f'ipfix_fnf_output: {self.ipfix_fnf_output}, '
            f'ipfix_medianet_output: {self.ipfix_medianet_output}, '
            f'ipfix_signaling_dn_output: {self.ipfix_signaling_dn_output}, '
            f'latency_analysis: {self.latency_analysis}, '
            f'license: {{{repr(self.license)}}}, '
            f'rtp_analysis: {self.rtp_analysis}, '
            f'tcp_3way_handshake_enforcement: {self.tcp_3way_handshake_enforcement}, '
            f'tcp_retransmissions_analysis: {self.tcp_retransmissions_analysis}, '
            f'tls_analysis: {self.tls_analysis}, '
            f'tls_decryption: {self.tls_decryption}, '
            f'vlan_vxlan_mpls_analysis: {self.vlan_vxlan_mpls_analysis}, '
            f'web_analysis: {self.web_analysis}'
        )

    def _store(self):
        """Store attributes in a dictionary."""
        props = {}
        for k, v in LiveFlowContext_15._license_dict.items():
            props[k] = getattr(self, v)
        return props


class LiveFlowContext(object):
    """The LiveFlowContext class has the attributes of a LiveFlow
    context.
    """

    analysis = None

    license = None

    output = None

    target_count = 0
    """The number of output targets."""

    def __init__(self, props: dict):
        self.analysis = LiveFlowContext.analysis
        self.license = LiveFlowContext.license
        self.output = LiveFlowContext.output
        self.target_count = LiveFlowContext.target_count
        self._load(props)

    def _load(self, props):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            count = props.get('targetCount')
            if count is not None:
                self.target_count = int(count)
            analysis = props.get('analysis')
            self.analysis = LiveFlowContextAnalysis(analysis)
            license = props.get('license')
            self.license = LiveFlowLicense(license)
            output = props.get('output')
            self.output = LiveFlowContextOutput(output)


class HashTable(object):
    """The HashTable class has the attributes of a LiveFlow hash
    table.
    """

    active_flow_count_limit = 0
    """The number of active flows that are currently being tracked by
    the hash table.
    """

    capacity = 0
    """The capacity of the hash table."""

    collisions = 0
    """The number of collisions for the hash table."""

    deletions = 0
    """The number of deletions for the hash table."""

    dropped_insertions = 0
    """The number of dropped insertions for the hash table."""

    id = 0
    """The id for the hash table."""

    insertions = 0
    """The number of insertions for the hash table."""

    max_contiguous_filled_buckets = 0
    """The number of max contiguous filled buckets for the hash table.
    """

    rtp_insertions = 0
    """The number of RTP insertions for the hash table."""

    size = 0
    """The size of the hash table."""

    _hash_tables_dict = {
        'activeFlowCountLimit': 'active_flow_count_limit',
        'capacity': 'capacity',
        'collisions': 'collisions',
        'deletions': 'deletions',
        'droppedInsertions': 'dropped_insertions',
        'id': 'id',
        'insertions': 'insertions',
        'maxContiguousFilledBuckets': 'max_contiguous_filled_buckets',
        'rtpInsertions': 'rtp_insertions',
        'size': 'size'
    }

    def __init__(self, props):
        self._load(props)

    def __repr__(self):
        return f'{self.__class__.__name__}({{{self._render()}}})'

    def __str__(self):
        return f'{self.__class__.__name__}({self._render()})'

    def _load(self, props):
        """Set attributes from a dictionary."""
        load_props_from_dict(self, props, HashTable._hash_tables_dict)

    def _render(self) -> str:
        return (
            f'active_flow_count_limit: {self.active_flow_count_limit}, '
            f'capacity: {self.capacity}, '
            f'collisions: {self.collisions}, '
            f'deletions: {self.deletions}, '
            f'dropped_insertions: {self.dropped_insertions}, '
            f'id: {self.id}, '
            f'insertions: {self.insertions}, '
            f'max_contiguous_filled_buckets: {self.max_contiguous_filled_buckets}, '
            f'rtp_insertions: {self.rtp_insertions}, '
            f'size: {self.size}'
        )

    def _store(self):
        """Store attributes in a dictionary."""
        props = {}
        for k, v in HashTable._hash_tables_dict.items():
            props[k] = getattr(self, v)
        return props


class RecordStatistics(object):
    """The RecordStatistics class has the attributes of LiveFlow
    records.
    """

    avc_count = 0
    """The number of AVC records sent."""

    dropped_ipfix_count = 0
    """The number of IPFIX records dropped."""

    dropped_message_pack_count = 0
    """The number of Message Pack records dropped."""

    financial_servies_count = 0
    """The number of Financial Services records sent."""

    fnf_count = 0
    """The number of FNF records sent."""

    medianet_count = 0
    """The number of MediaNet records sent."""

    message_pack_count = 0
    """The number of Message Pack records sent."""

    platform_count = 0
    """The number of Platform records sent."""

    signaling_dn_ipv4_count = 0
    """The number of Signaling DN IPv4 records sent."""

    signaling_dn_ipv6_count = 0
    """The number of Signaling DN IPv6 records sent."""

    sna_count = 0
    """The number of Cisco SNA records sent."""

    _stats_dict = {
        'avc': 'avc_count',
        'ciscoSNA': 'sna_count',
        'droppedIpfix': 'dropped_ipfix_count',
        'droppedMessagePack': 'dropped_message_pack_count',
        'financialServies': 'financial_services_count',
        'fnf': 'fnf_count',
        'mediaNet': 'medianet_count',
        'messagePack': 'message_pack_count',
        'platform': 'platform_count',
        'signalingDNIPv4': 'signaling_dn_ipv4_count',
        'signalingDNIPv6': 'signaling_dn_ipv6_count'
    }

    def __init__(self, props):
        self.ipfix_avc_count = RecordStatistics.ipfix_avc_count
        self.ipfix_fnf_count = RecordStatistics.ipfix_fnf_count
        self.ipfix_medianet_count = RecordStatistics.ipfix_medianet_count
        self.ipfix_signaling_dn_ipv4_count = RecordStatistics.ipfix_signaling_dn_ipv4_count
        self.ipfix_signaling_dn_ipv6_count = RecordStatistics.ipfix_signaling_dn_ipv6_count
        self._load(props)

    def __repr__(self):
        return (
            f'{self.__class__.__name__}({{'
            f'ipfix_avc_count: {self.ipfix_avc_count}, '
            f'ipfix_fnf_count: {self.ipfix_fnf_count}, '
            f'ipfix_medianet_count: {self.ipfix_medianet_count}, '
            f'ipfix_signaling_dn_ipv4_count: {self.ipfix_signaling_dn_ipv4_count}, '
            f'ipfix_signaling_dn_ipv6_count: {self.ipfix_signaling_dn_ipv6_count}'
            f'}})'
        )

    def __str__(self):
        return (
            f'{self.__class__.__name__}('
            f'ipfix_avc_count: {self.ipfix_avc_count}, '
            f'ipfix_fnf_count: {self.ipfix_fnf_count}, '
            f'ipfix_medianet_count: {self.ipfix_medianet_count}, '
            f'ipfix_signaling_dn_ipv4_count: {self.ipfix_signaling_dn_ipv4_count}, '
            f'ipfix_signaling_dn_ipv6_count: {self.ipfix_signaling_dn_ipv6_count}'
            f')'
        )

    def _load(self, props):
        """Set attributes from a dictionary."""
        load_props_from_dict(self, props, RecordStatistics._stats_dict)

    def _store(self):
        """Store attributes in a dictionary."""
        props = {}
        for k, v in RecordStatistics._stats_dict.items():
            props[k] = getattr(self, v)
        return props


class LiveFlowStatus(object):
    """The LiveFlowStatus class has the attributes of LiveFlow status.
    """

    active_flow_count = 0
    """The number of active flows that are currently being tracked by
    LiveFlow.
    """

    capture_start_time = ''
    """In ISO 8601 format: CCYY-MM-DDThh:mm:ss.sssssssssZ. Will be null
    if the capture has never been started.
    """

    flows_rejected = 0
    """The number of flows rejected by LiveFlow due to the active flow
    count limit.
    """

    flows_rtp_zero_packet = 0
    """The number of RTP zero packet flows detected by LiveFlow."""

    flows_seen = 0
    """The number of flows seen by LiveFlow."""

    hash_table = []
    """The LiveFlow hash table status"""

    records = None
    """The array of records sent by LiveFlow."""

    packets_accepted = 0
    """The number of packets accepted and analyzed by LiveFlow."""

    packets_rejected = 0
    """The number of packets rejected by LiveFlow."""

    packets_seen = 0
    """The number of packets seen by LiveFlow."""

    _status_dict = {
        'activeFlowCount': 'active_flow_count',
        'captureStartTime': 'capture_start_time',
        'flowsRejected': 'flows_rejected',
        'flowsRTPZeroPacket': 'flows_rtp_zero_packet',
        'flowsSeen': 'flows_seen',
        'packetsAccepted': 'packets_accepted',
        'packetsRejected': 'packets_rejected',
        'packetsSeen': 'packets_seen'
    }

    def __init__(self, props):
        self.active_flow_count = LiveFlowStatus.active_flow_count
        self.capture_start_time = LiveFlowStatus.capture_start_time
        self.flows_rejected = LiveFlowStatus.flows_rejected
        self.flows_rtp_zero_packet = LiveFlowStatus.flows_rtp_zero_packet
        self.flows_seen = LiveFlowStatus.flows_seen
        self.records = LiveFlowStatus.records
        self.packets_accepted = LiveFlowStatus.packets_accepted
        self.packets_rejected = LiveFlowStatus.packets_rejected
        self.packets_seen = LiveFlowStatus.packets_seen
        self._load(props)

    def __repr__(self):
        return f'{self.__class__.__name__}({{{self._render()}}})'

    def __str__(self):
        return f'{self.__class__.__name__}({self._render()})'

    def _load(self, props):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            load_props_from_dict(self, props, LiveFlowStatus._status_dict)

            hash_table = props.get('hashTable')
            if isinstance(hash_table, list):
                self.hash_table = [HashTable(v) for v in hash_table]

            record_stats = props.get('recordsSent')
            if isinstance(record_stats, dict):
                self.records = RecordStatistics(record_stats)

    def _render(self) -> str:
        return (
            f'active_flow_count: {self.active_flow_count}, '
            f'capture_start_time: "{self.capture_start_time}", '
            f'flows_rejected: {self.flows_rejected}, '
            f'flows_rtp_zeroPacket: {self.flows_rtp_zero_packet}, '
            f'flows_seen: {self.flows_seen}, '
            f'hash_table: [{repr_array(self.hash_table)}], '
            f'packets_accepted: {self.packets_accepted}, '
            f'packets_rejected: {self.packets_rejected}, '
            f'packets_seen: {self.packets_seen}'
        )


class LiveFlow(object):
    """The LiveFlow class is an interface into LiveFlow operations."""

    engine = None
    """OmniEngine interface."""

    _version_table = {
        '24.2.0': 18,
        '24.1.1': 15,
        '24.1.0': 15
    }

    def __init__(self, engine: OmniEngine):
        self.engine = engine

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self.engine)})'

    def __str__(self):
        return '{self.__class__.__name__}({repr(self.engine)})'

    def get_liveflow_configuration(self) -> LiveFlowConfiguration:
        """Gets the LiveFlow configuration"""
        if self.engine is not None:
            command = 'liveflow/configuration/'
            pr = self.engine.perf('get_liveflow_configuration')
            resp = self.engine._issue_command(command, pr)
            if not isinstance(resp, dict):
                raise OmniError('Failed to get LiveFlow configuration.')
            return LiveFlowConfiguration(resp)
        return None

    def get_liveflow_context(self) -> LiveFlowContext:
        """Gets the LiveFlow context"""
        if self.engine is not None:
            command = 'liveflow/context/'
            pr = self.engine.perf('get_liveflow_context')
            resp = self.engine._issue_command(command, pr)
            if not isinstance(resp, dict):
                raise OmniError('Failed to get LiveFlow context.')
            return LiveFlowContext(resp)
        return None

    def get_liveflow_status(self) -> LiveFlowStatus:
        """Gets the LiveFlow status"""
        if self.engine is not None:
            command = 'liveflow/status/'
            pr = self.engine.perf('get_liveflow_status')
            resp = self.engine._issue_command(command, pr)
            if not isinstance(resp, dict):
                raise OmniError('Failed to get LiveFlow status.')
            return LiveFlowStatus(resp)
        return None

    def set_liveflow_configuration(self, config: LiveFlowConfiguration) -> bool:
        """Sets the LiveFlow configuration"""
        if self.engine is not None:
            command = 'liveflow/configuration/'
            pr = self.engine.perf('set_liveflow_configuration')
            data = json.dumps(config._store(), cls=OmniScriptEncoder)
            resp = self.engine._issue_command(
                command, pr, EO.POST, data=data)
            if not isinstance(resp, dict):
                raise OmniError('Failed to set LiveFlow Configuration.')
            reboot = resp.get('rebootRequired')
            if reboot is not None:
                return bool(reboot)
            return False
        return False
