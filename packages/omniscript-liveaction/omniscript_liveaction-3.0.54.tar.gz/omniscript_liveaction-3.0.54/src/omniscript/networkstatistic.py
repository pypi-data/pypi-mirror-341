"""Network Statistic class.
"""
# Copyright (c) LiveAction, Inc. 2024. All rights reserved.

from .peektime import PeekTime


class OmniEngine(object):
    pass


class ChannelStatistic:
    """the Channel Statistic class has the attributes of a capture's
    channel statistic.
    """

    _channel_prop_dict = {
        'broadcastBytes': 'broadcast_bytes',
        'broadcastPackets': 'broadcast_packets',
        'multicastBytes': 'multicast_bytes',
        'multicastPacke': 'multicast_packets',
        'time': 'time',
        'totalBytes': 'total_bytes',
        'totalPackets': 'total_packets'
    }

    _engine = None
    """OmniEngine that generated the statistic."""

    broadcast_bytes = 0
    """Number bytes in the broadcast packets."""

    broadcast_packets = 0
    """Number of broadcast packets."""

    multicast_bytes = 0
    """Number of bytes in the multicast packets."""

    multicast_packets = 0
    """Number of multicast packets."""

    time = None
    """Timestamp of the Network Statistic."""

    total_bytes = 0
    """Number of bytes."""

    total_packets = 0
    """Number of packets."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        self._engine = engine
        self.broadcast_bytes = ChannelStatistic.broadcast_bytes
        self.broadcast_packets = ChannelStatistic.broadcast_packets
        self.multicast_bytes = ChannelStatistic.multicast_bytes
        self.multicast_packets = ChannelStatistic.multicast_packets
        self.time = ChannelStatistic.time
        self.total_bytes = ChannelStatistic.total_bytes
        self.total_packets = ChannelStatistic.total_packets
        self._load(props)

    def __repr__(self) -> str:
        return 'ChannelStatistic:'

    def __str__(self) -> str:
        return 'ChannelStatistic:'

    def _load(self, props: dict = None):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            for k, v in props.items():
                a = ChannelStatistic._channel_prop_dict.get(k)
                if a is None or not hasattr(self, a):
                    continue
                if isinstance(getattr(self, a), int):
                    setattr(self, a, int(v) if v else 0)
                elif a in ('time'):
                    setattr(self, a, PeekTime(v))
                else:
                    self._engine.logger.error(f'Unparsed property: {k}: {v}')


class NetworkChannelStatistic:
    """the Network Channel Statistic class has the attributes of a
    capture's network channel statistic.
    """

    _network_channel_prop_dict = {
        'broadcastBytes': 'broadcast_bytes',
        'broadcastPackets': 'broadcast_packets',
        'channel': 'channel',
        'multicastBytes': 'multicast_bytes',
        'multicastPacke': 'multicast_packets',
        'samples': 'channel_stats',
        'totalBytes': 'total_bytes',
        'totalPackets': 'total_packets'
    }

    _engine = None
    """OmniEngine that generated the statistic."""

    broadcast_bytes = 0
    """Number bytes in the broadcast packets."""

    broadcast_packets = 0
    """Number of broadcast packets."""

    channel = 0
    """Number of Channels."""

    channel_stats = []
    """List of ChannelStatistc."""

    multicast_bytes = 0
    """Number of bytes in the multicast packets."""

    multicast_packets = 0
    """Number of multicast packets."""

    total_bytes = 0
    """Number of bytes."""

    total_packets = 0
    """Number of packets."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        self._engine = engine
        self.broadcast_bytes = NetworkStatistic.broadcast_bytes
        self.broadcast_packets = NetworkStatistic.broadcast_packets
        self.channel = NetworkStatistic.channel
        self.channel_stats = []
        self.multicast_bytes = NetworkStatistic.multicast_bytes
        self.multicast_packets = NetworkStatistic.multicast_packets
        self.total_bytes = NetworkStatistic.total_bytes
        self.total_packets = NetworkStatistic.total_packets
        self._load(props)

    def __repr__(self) -> str:
        return 'NetworkChannelStatistic:'

    def __str__(self) -> str:
        return 'NetworkChannelStatistic:'

    def _load(self, props: dict = None):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            for k, v in props.items():
                a = NetworkChannelStatistic._network_channel_prop_dict.get(k)
                if a is None or not hasattr(self, a):
                    continue
                if isinstance(getattr(self, a), int):
                    setattr(self, a, int(v) if v else 0)
                elif a in ('channel_stats'):
                    self.channel_stats.clear()
                    for stat in v:
                        if isinstance(stat, dict):
                            self.channel_stats.append(ChannelStatistic(self._engine, stat))
                else:
                    self._engine.logger.error(f'Unparsed property: {k}: {v}')


class NetworkStatistic(object):
    """the Network Statistic class has the attributes of a capture's
    network statistic.
    """

    _network_prop_dict = {
        'broadcastBytes': 'broadcast_bytes',
        'broadcastPackets': 'broadcast_packets',
        'multicastBytes': 'multicast_bytes',
        'multicastPacke': 'multicast_packets',
        'time': 'time',
        'totalBytes': 'total_bytes',
        'totalPackets': 'total_packets'
    }

    _engine = None
    """OmniEngine that generated the statistic."""

    broadcast_bytes = 0
    """Number bytes in the broadcast packets."""

    broadcast_packets = 0
    """Number of broadcast packets."""

    multicast_bytes = 0
    """Number of bytes in the multicast packets."""

    multicast_packets = 0
    """Number of multicast packets."""

    time = None
    """Timestamp of the Network Statistic."""

    total_bytes = 0
    """Number of bytes."""

    total_packets = 0
    """Number of packets."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        self._engine = engine
        self.broadcast_bytes = NetworkStatistic.broadcast_bytes
        self.broadcast_packets = NetworkStatistic.broadcast_packets
        self.multicast_bytes = NetworkStatistic.multicast_bytes
        self.multicast_packets = NetworkStatistic.multicast_packets
        self.time = NetworkStatistic.time
        self.total_bytes = NetworkStatistic.total_bytes
        self.total_packets = NetworkStatistic.total_packets
        self._load(props)

    def __repr__(self) -> str:
        return 'NetworkStatistic:'

    def __str__(self) -> str:
        return 'NetworkStatistic:'

    def _load(self, props: dict = None):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            for k, v in props.items():
                a = NetworkStatistic._network_prop_dict.get(k)
                if a is None or not hasattr(self, a):
                    continue
                if isinstance(getattr(self, a), int):
                    setattr(self, a, int(v) if v else 0)
                elif a in ('time'):
                    setattr(self, a, PeekTime(v))
                else:
                    self._engine.logger.error(f'Unparsed property: {k}: {v}')
