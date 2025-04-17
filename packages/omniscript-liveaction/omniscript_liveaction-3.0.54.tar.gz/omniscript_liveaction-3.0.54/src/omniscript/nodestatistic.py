"""Node Statistic class.
"""
# Copyright (c) LiveAction, Inc. 2024. All rights reserved.

import six
from .mediaspecification import MediaSpecification
from .omniid import OmniId
from .peektime import PeekTime


class OmniEngine(object):
    pass


class NodeStatistic(object):
    """the Node Statistic class has the attributes of a capture's
    node statistic.
    """

    _node_prop_dict = {
        'broadcastBytes': 'broadcast_bytes',
        'broadcastPackets': 'broadcast_packets',
        'bytesReceived': 'bytes_received',
        'bytesSent': 'bytes_sent',
        'color': 'color',
        'city': 'city',
        'country': 'country',
        'countryCode': 'country_code',
        'duration': 'duration',
        'firstTimeReceived': 'first_time_received',
        'firstTimeSent': 'first_time_sent',
        'lastTimeReceived': 'last_time_received',
        'lastTimeSent': 'last_time_sent',
        'latitude': 'latitude',
        'longitude': 'longitude',
        'maximumPacketSizeReceived': 'maximum_packet_size_received',
        'maximumPacketSizeSent': 'maximum_packet_size_sent',
        'mediaSpec': 'media_spec',
        'minimumPacketSizeReceived': 'minimum_packet_size_received',
        'minimumPacketSizeSent': 'minimum_packet_size_sent',
        'multicastBytes': 'multicast_bytes',
        'multicastPacke': 'multicast_packets',
        'name': 'name',
        'node': 'node',
        'packetsReceived': 'packets_received',
        'packetsSent': 'packets_sent',
        'trust': 'trust'
    }

    _engine = None
    """OmniEngine that generated the statistic."""

    broadcast_bytes = 0
    """Number bytes in the broadcast packets."""

    broadcast_packets = 0
    """Number of broadcast packets."""

    bytes_received = 0
    """Number of bytes in the packets received."""

    bytes_sent = 0
    """Number of bytes in the packets sent."""

    color = ''
    """Color code for this Snapshot"""

    city = ""
    """Name of the city."""

    country = ''
    """Name of the country"""

    country_code = ''
    """Country code"""

    duration = None
    """Duration of this snapshot."""

    first_time_received = None
    """First time a packet was received."""

    first_time_sent = None
    """First time a packet was sent."""

    last_time_received = None
    """Last time a packet was received."""

    last_time_sent = None
    """Last time a packet was sent."""

    latitude = 0.0
    """Latitude the traffic's origination or destination"""

    longitude = 0.0
    """Longitude the traffic's origination or destination"""

    maximum_packet_size_received = 0
    """Number of bytes in the largest packet received."""

    maximum_packet_size_sent = 0
    """Number of bytes in the largest packet sent."""

    media_spec = None
    """The MediaSpec of the traffic."""

    minimum_packet_size_received = 0
    """Number of bytes in the smallest packet received."""

    minimum_packet_size_sent = 0
    """Number of bytes in the smallest packet sent."""

    multicast_bytes = 0
    """Number of bytes in the multicast packets."""

    multicast_packets = 0
    """Number of multicast packets."""

    name = ''
    """Name of this Snapshot"""

    packets_received = 0
    """Number of packets received."""

    packets_sent = 0
    """Number of bytes in the packets received."""

    trust = ''
    """Trust level/label."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        self._engine = engine
        self.broadcast_bytes = NodeStatistic.broadcast_bytes
        self.broadcast_packets = NodeStatistic.broadcast_packets
        self.bytes_received = NodeStatistic.bytes_received
        self.bytes_sent = NodeStatistic.bytes_sent
        self.color = NodeStatistic.color
        self.city = NodeStatistic.city
        self.country = NodeStatistic.country
        self.country_code = NodeStatistic.country_code
        self.duration = NodeStatistic.duration
        self.first_time_received = NodeStatistic.first_time_received
        self.first_time_sent = NodeStatistic.first_time_sent
        self.last_time_received = NodeStatistic.last_time_received
        self.last_time_sent = NodeStatistic.last_time_sent
        self.latitude = NodeStatistic.latitude
        self.longitude = NodeStatistic.longitude
        self.maximum_packet_size_received = NodeStatistic.maximum_packet_size_received
        self.maximum_packet_size_sent = NodeStatistic.maximum_packet_size_sent
        self.media_spec = NodeStatistic.media_spec
        self.minimum_packet_size_received = NodeStatistic.minimum_packet_size_received
        self.minimum_packet_size_sent = NodeStatistic.minimum_packet_size_sent
        self.multicast_bytes = NodeStatistic.multicast_bytes
        self.multicast_packets = NodeStatistic.multicast_packets
        self.name = NodeStatistic.name
        self.packets_received = NodeStatistic.packets_received
        self.packets_sent = NodeStatistic.packets_sent
        self.trust = NodeStatistic.trust
        self._load(props)

    def __repr__(self) -> str:
        return 'NodeStatistic:'

    def __str__(self) -> str:
        return 'NodeStatistic:'

    def _load(self, props: dict = None):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            for k, v in props.items():
                a = NodeStatistic._node_prop_dict.get(k)
                if a is None or not hasattr(self, a):
                    continue
                if isinstance(getattr(self, a), int):
                    setattr(self, a, int(v) if v else 0)
                elif isinstance(getattr(self, a), six.string_types):
                    setattr(self, a, v if v else '')
                elif isinstance(getattr(self, a), float):
                    setattr(self, a, float(v) if v else 0.0)
                elif getattr(self, a) is None:
                    if a in ('first_time_received', 'first_time_sent',
                             'last_time_received', 'last_time_sent'):
                        setattr(self, a, PeekTime(v))
                    elif a in ('media_spec'):
                        setattr(self, a, MediaSpecification(v))
                else:
                    self._engine.logger.error(f'NodeStatistic - Unparsed property: {k}: {v}')
