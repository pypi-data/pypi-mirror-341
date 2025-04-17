"""Conversation Statistic class.
"""
# Copyright (c) BlueCat Networks, Inc. 2025. All rights reserved.

import six
from .mediaspecification import MediaSpecification
from .peektime import PeekTime


class OmniEngine(object):
    pass


class NodeInformation(object):
    """Node Information class has the attributes of a conversation's
    origin and end points.
    """

    address = ''
    """The address."""

    city = ''
    """Name of the city."""

    color = ''
    """Color"""

    country = ''
    """Country name"""

    country_code = ''
    """Country code."""

    latitude = 0.0
    """Latitude."""

    longitude = 0.0
    """Longitude"""

    name = ''
    """Name"""

    media_spec = None
    """Media Specification"""

    def __init__(self, node_dict, engine: OmniEngine, props: dict = None):
        self._engine = engine
        self.address = NodeInformation.address
        self.city = NodeInformation.city
        self.color = NodeInformation.color
        self.country = NodeInformation.country
        self.country_code = NodeInformation.country_code
        self.latitude = NodeInformation.latitude
        self.longitude = NodeInformation.longitude
        self.name = NodeInformation.name
        self.media_spec = NodeInformation.media_spec
        self._load(node_dict, props)

    def __repr__(self) -> str:
        return 'NodeInformation:'

    def __str__(self) -> str:
        return 'NodeInformation:'

    def _load(self, node_dict, props: dict = None):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            for k, v in props.items():
                a = node_dict.get(k)
                if a is None or not hasattr(self, a):
                    continue
                if isinstance(getattr(self, a), int):
                    setattr(self, a, int(v) if v else 0)
                elif isinstance(getattr(self, a), six.string_types):
                    setattr(self, a, v if v else '')
                elif isinstance(getattr(self, a), float):
                    setattr(self, a, float(v) if v else 0.0)
                elif getattr(self, a) is None:
                    if a in ('media_spec'):
                        setattr(self, a, MediaSpecification(v))


class ConversationStatistic(object):
    """the Conversation Statistic class has the attributes of a
    capture's conversation statistic.
    """
    _conversation_prop_dict = {
        'bytes': 'bytes',
        'duration': 'duration',
        'firstTime': 'first_time',
        'hierarchy': 'hierarchy',
        'lastTime': 'last_time',
        'maximumPacketSize': 'maximum_packet_size',
        'minimumPacketSize': 'minimum_packet_size',
        'packets': 'packets',
        'protocol': 'protocol',
        'protocolId': 'protocol_id',
        'protocolColor': 'protocol_color',
        'protocolName': 'protocol_name',
        'protocolMediaSpec': 'protocol_media_spec'
    }

    _destination_prop_dict = {
        'destination': 'address',
        'destinationCity': 'city',
        'destinationColor': 'color',
        'destinationCountry': 'country',
        'destinationCountryCode': 'country_code',
        'destinationLatitude': 'latitude',
        'destinationLongitude': 'longitude',
        'destinationName': 'name',
        'destinationMediaSpec': 'media_spec',
    }

    _source_prop_dict = {
        'source': 'address',
        'sourceCity': 'city',
        'sourceColor': 'color',
        'sourceCountry': 'country',
        'sourceCountryCode': 'country_code',
        'sourceLatitude': 'latitude',
        'sourceLongitude': 'longitude',
        'sourceName': 'name',
        'sourceMediaSpec': 'media_spec',
    }

    _engine = None
    """OmniEngine that generated the statistic."""

    bytes = 0
    """Number bytes in the packets."""

    destination = None
    """Node Information of the desination node."""

    duration = 0
    """Duration"""

    first_time = None
    """Timestampe of the first packet."""

    hierarchy = []
    """Heirarchy"""

    last_time = None
    """Timestamp of the last packet."""

    maximum_packet_size = 0
    """Size of the largest packet."""

    minimum_packet_size = 0
    """Size of the smallest packet."""

    packets = 0
    """Total number of packets."""

    protocol = ''
    """Name of the protocol"""

    protocol_id = 0
    """Id of the protocol """

    protocol_color = ''
    """Color of the protocol """

    protocol_name = ''
    """Name of the protocol."""

    protocol_media_spec = None
    """ """

    source = None
    """Node Information of the source ndoe."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        self._engine = engine
        self.bytes = ConversationStatistic.bytes
        self.destination = ConversationStatistic.destination
        self.duration = ConversationStatistic.duration
        self.first_time = ConversationStatistic.first_time
        self.hierarchy = []
        self.last_time = ConversationStatistic.last_time
        self.maximum_packet_size = ConversationStatistic.maximum_packet_size
        self.minimum_packet_size = ConversationStatistic.minimum_packet_size
        self.packets = ConversationStatistic.packets
        self.protocol = ConversationStatistic.protocol
        self.protocol_id = ConversationStatistic.protocol_id
        self.protocol_color = ConversationStatistic.protocol_color
        self.protocol_name = ConversationStatistic.protocol_name
        self.protocol_media_spec = ConversationStatistic.protocol_media_spec
        self.source = ConversationStatistic.source
        self._load(props)

    def __repr__(self) -> str:
        return 'ConversationStatistic:'

    def __str__(self) -> str:
        return 'ConversationStatistic:'

    def _load(self, props: dict = None):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            for k, v in props.items():
                a = ConversationStatistic._conversation_prop_dict.get(k)
                if a is None or not hasattr(self, a):
                    continue
                if isinstance(getattr(self, a), int):
                    setattr(self, a, int(v) if v else 0)
                elif isinstance(getattr(self, a), six.string_types):
                    setattr(self, a, v if v else '')
                elif isinstance(getattr(self, a), list):
                    setattr(self, a, v if v else [])
                elif getattr(self, a) is None:
                    if a in ('first_time', 'last_time'):
                        setattr(self, a, PeekTime(v))
                    elif a in ('protocol_media_spec'):
                        setattr(self, a, MediaSpecification(v))
                else:
                    self._engine.logger.error(
                        f'ConversationStatistic - Unparsed property: {k}: {v}')
            self.destination = NodeInformation(ConversationStatistic._destination_prop_dict,
                                               self._engine, props)
            self.source = NodeInformation(ConversationStatistic._source_prop_dict,
                                          self._engine, props)
