"""Protocol Statistic class.
"""
# Copyright (c) LiveAction, Inc. 2024. All rights reserved.

import six
from .mediaspecification import MediaSpecification
from .omniid import OmniId
from .peektime import PeekTime


class OmniEngine(object):
    pass


class ProtocolStatistic(object):
    """the Protocol Statistic class has the attributes of a capture's
    Protocol statistic.
    """

    _protocol_prop_dict = {
        'bytes': 'bytes',
        'color': 'color',
        'duration': 'duration',
        'firstTime': 'first_time',
        'id': 'id_code',
        'lastTime': 'last_time',
        'mediaSpec': 'media_spec',
        'name': 'name',
        'packets': 'packets',
        'protocol': 'protocol'
    }

    _engine = None
    """OmniEngine that generated the statistic."""

    bytes = 0
    """Number bytes in the packets."""

    color = ''
    """Color code for this Snapshot"""

    duration = None
    """Duration of this snapshot."""

    first_time = None
    """First time a packet with the protocol was collected."""

    id_code = 0
    """Identification code of the protocol."""

    last_time = None
    """Last time a packet with the protocol was collected."""

    media_spec = None
    """The MediaSpec of the traffic."""

    name = ""
    """Name of this Snapshot"""

    packets = 0
    """Number of packets collected."""

    protocol = ''
    """Name of the protocol."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        self._engine = engine
        self.bytes = ProtocolStatistic.bytes
        self.color = ProtocolStatistic.color
        self.duration = ProtocolStatistic.duration
        self.first_time = ProtocolStatistic.first_time
        self.id_code = ProtocolStatistic.id_code
        self.last_time = ProtocolStatistic.last_time
        self.media_spec = ProtocolStatistic.media_spec
        self.name = ProtocolStatistic.name
        self.packets = ProtocolStatistic.packets
        self.protocol = ProtocolStatistic.protocol
        self._load(props)

    def __repr__(self) -> str:
        return 'ProtocolStatistic:'

    def __str__(self) -> str:
        return 'ProtocolStatistic:'

    def _load(self, props: dict = None):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            for k, v in props.items():
                a = ProtocolStatistic._protocol_prop_dict.get(k)
                if a is None or not hasattr(self, a):
                    continue
                if isinstance(getattr(self, a), int):
                    setattr(self, a, int(v) if v else 0)
                elif isinstance(getattr(self, a), six.string_types):
                    setattr(self, a, v if v else '')
                elif getattr(self, a) is None:
                    if a in ('first_time', 'last_time'):
                        setattr(self, a, PeekTime(v))
                    elif a in ('media_spec'):
                        setattr(self, a, MediaSpecification(v))
                else:
                    self._engine.logger.error(f'ProtocolStatistic - Unparsed property: {k}: {v}')
