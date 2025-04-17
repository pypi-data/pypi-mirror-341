"""Statistic Set class.
"""
# Copyright (c) LiveAction, Inc. 2024. All rights reserved.

from .applicationflowstatistic import ApplicationFlowStatistic
from .applicationstatistic import ApplicationStatistic
from .callstatistic import CallStatistic
from .conversationstatistic import ConversationStatistic
from .countrystatistic import CountryStatistic
from .errorstatistic import ErrorStatistic
from .historystatistic import HistoryStatistic
from .networkstatistic import NetworkStatistic, NetworkChannelStatistic
from .nodestatistic import NodeStatistic
from .omniid import OmniId
from .protocolstatistic import ProtocolStatistic
from .sizestatistic import SizeStatistic
from .summarystatistic import SummaryStatistic


class OmniEngine(object):
    pass


def get_id(props: dict, name: str) -> OmniId:
    id = props.get(name)
    if id:
        return OmniId(id)
    return None


class StatisticSet(object):
    """Statistic Set base class."""
    _statset_prop_dict = {
        'duration': 'duration',
        'totalBytes': 'total_bytes',
        'totalPackets': 'total_packets'
    }

    _engine = None
    """OmniEngine that generated the Statistic Set."""

    duration = 0
    """Duration of the Statistic Set."""

    total_bytes = 0
    """Number of bytes in all the packets."""

    total_packets = 0
    """Number of packets."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        self._engine = engine
        self.duration = StatisticSet.duration
        self.total_bytes = StatisticSet.total_bytes
        self.total_packets = StatisticSet.total_packets
        self._load_set(props)

    def _load_set(self, props: dict):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            for k, v in props.items():
                a = StatisticSet._statset_prop_dict.get(k)
                if a is None or not hasattr(self, a):
                    continue
                elif isinstance(getattr(self, a), int):
                    setattr(self, a, int(v) if v else 0)
                else:
                    self._engine.logger.error(f'Unparsed property: {k}: {v}')


class ApplicationFlowStatisticSet(StatisticSet):
    """ApplicationFlowStatisticSet
    """
    _appflowset_prop_dict = {
        'applicationFlows': 'application_flow_stats',
    }

    application_flow_stats = []
    """A list of ApplicationFlowStatistic."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        StatisticSet.__init__(self, engine, props)
        self.application_flow_stats = []
        self._load(props)

    def _load(self, props: dict):
        if isinstance(props, dict):
            for k, v in props.items():
                if k == 'applicationFlows':
                    self.application_flow_stats.clear()
                    for stat in v:
                        if isinstance(stat, dict):
                            self.application_flow_stats.append(
                                ApplicationFlowStatistic(self._engine, stat))
                elif k == 'clsid':
                    continue
                else:
                    self._engine.logger.error(
                        f'ApplicationFlowStatisticSet - Unparsed property: {k}: {v}')


# ApplicationHistoryStatistics
# ApplicationResponseTimesStatistics


class ApplicationStatisticSet(StatisticSet):
    """ApplicationStatisticSet
    """
    _appset_prop_dict = {
        'applications': 'application_stats',
        'resetCount': 'reset_count',
        'timeLimitReached': 'time_limit_reached'
    }

    application_stats = []
    """A list of ApplicationStatistic."""

    reset_count = 0
    """Nuber of times the Statistic Set has been reset."""

    time_limit_reached = False
    """Has the time limit been reached."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        StatisticSet.__init__(self, engine, props)
        self.application_stats = []
        self.reset_count = ApplicationStatisticSet.reset_count
        self.time_limit_reached = ApplicationStatisticSet.time_limit_reached
        self._load(props)

    def _load(self, props: dict):
        if isinstance(props, dict):
            for k, v in props.items():
                a = ApplicationStatisticSet._appset_prop_dict.get(k)
                if a is None or not hasattr(self, a):
                    continue
                if isinstance(getattr(self, a), int):
                    setattr(self, a, int(v) if v else 0)
                elif isinstance(getattr(self, a), list):
                    self.application_stats.clear()
                    for stat in v:
                        if isinstance(stat, dict):
                            self.application_stats.append(ApplicationStatistic(self._engine, stat))
                else:
                    self._engine.logger.error(
                        f'ApplicationStatisticSet - Unparsed property: {k}: {v}')


class CallStatisticSet(StatisticSet):
    """CallStatisticSet
    The only Statistic Set that is not based on the StatisticSet class.
    """
    _callset_prop_dict = {
        'call': 'call_stats'
    }

    call_stats = []
    """A list of CallStatistic."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        StatisticSet.__init__(self, engine, props)
        self.call_stats = []
        self._load(props)

    def _load(self, props: dict):
        if isinstance(props, dict):
            call = props.get('call')
            if isinstance(call, dict):
                self.call_stats.clear()
                self.call_stats.append(CallStatistic(self._engine, call))
            else:
                self._engine.logger.error('Unparsed property in CallStatisticSet.')


class ConversationStatisticSet(StatisticSet):
    """ConversationStatisticSet
    """
    _conversationset_prop_dict = {
        'conversations': 'conversation_stats',
        'duration': 'duration',
        'resetCount': 'reset_count',
        'timeLimitReached': 'time_limit_reached',
        'totalBytes': 'total_bytes',
        'totalPackets': 'total_packets'
    }

    conversation_stats = []
    """A list of ConversationStatistic."""

    reset_count = 0
    """Nuber of times the statistic has been reset."""

    time_limit_reached = False
    """Has the time limit been reached."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        StatisticSet.__init__(self, engine, props)
        self.conversation_stats = []
        self.reset_count = ConversationStatisticSet.reset_count
        self.time_limit_reached = ConversationStatisticSet.time_limit_reached
        self._load(props)

    def _load(self, props: dict):
        if isinstance(props, dict):
            for k, v in props.items():
                a = ConversationStatisticSet._conversationset_prop_dict.get(k)
                if a is None or not hasattr(self, a):
                    continue
                if isinstance(getattr(self, a), int):
                    setattr(self, a, int(v) if v else 0)
                elif isinstance(getattr(self, a), bool):
                    setattr(self, a, bool(v) if v else False)
                elif isinstance(getattr(self, a), list):
                    self.conversation_stats.clear()
                    for stat in v:
                        if isinstance(stat, dict):
                            self.conversation_stats.append(
                                ConversationStatistic(self._engine, stat))
                else:
                    self._engine.logger.error(
                        f'ConversationStatisticSet - Unparsed property: {k}: {v}')


class CountryStatisticSet(StatisticSet):
    """CountryStatisticSet
    """
    _countryset_prop_dict = {
        'countries': 'country_stats'
    }

    country_stats = []
    """A list of CountryStatistic."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        StatisticSet.__init__(self, engine, props)
        self.country_stats = []
        self._load(props)

    def _load(self, props: dict):
        if isinstance(props, dict):
            countries = props.get('countries')
            if isinstance(countries, list):
                self.country_stats.clear()
                for stat in countries:
                    if isinstance(stat, dict):
                        self.country_stats.append(CountryStatistic(self._engine, stat))


class ErrorStatisticSet(StatisticSet):
    """ErrorStatisticSet
    """

    error_stats = []
    """A list of ErrorStatistic objects."""

    last_value = 0.0
    """The value of the last sample."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        StatisticSet.__init__(self, engine, props)
        self.error_stats = []
        self.last_value = ErrorStatisticSet.last_value
        self._load(props)

    def _load(self, props: dict):
        if isinstance(props, dict):
            errors = props.get('error')
            if isinstance(errors, dict):
                last = errors.get('lastSampleValue')
                if last is not None:
                    self.last_value = float(last)
                error_stats = errors.get('errors')
                if isinstance(error_stats, list):
                    self.error_stats.clear()
                    for stat in error_stats:
                        if isinstance(stat, dict):
                            self.error_stats.append(ErrorStatistic(self._engine, stat))


class HistoryStatisticSet(StatisticSet):
    """HistoryStatisticSet
    """

    history_stats = []
    """A list of HistoryStatistic objects."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        StatisticSet.__init__(self, engine, props)
        self.history_stats = []
        self._load(props)

    def _load(self, props: dict):
        if isinstance(props, dict):
            history_stats = props.get('history')
            if isinstance(history_stats, list):
                self.history_stats.clear()
                for stat in history_stats:
                    if isinstance(stat, dict):
                        self.history_stats.append(HistoryStatistic(self._engine, stat))


# MPLSVLANVXLANStatistics


class NetworkStatisticSet(StatisticSet):
    """NetworStatisticSet
    """
    _networkset_prop_dict = {
        'broadcastBytes': 'broadcast_bytes',
        'broadcastPackets': 'broadcast_packets',
        'channels': 'channel_list',
        'multicastBytes': 'multicast_bytes',
        'multicastPackets': 'multicast_packets',
        'samples': 'network_stats'
    }

    broadcast_bytes = 0
    """Number of bytes in the Broadcast packets."""

    broadcast_packets = 0
    """Number of Broadcast packets."""

    channel_list = []
    """List of network channels."""

    multicast_bytes = 0
    """Number of bytes in the Multcast packets."""

    multicast_packets = 0
    """Number of Multicast packets"""

    network_stats = []
    """A list of NetworkStats objects."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        StatisticSet.__init__(self, engine, props)
        self.broadcast_bytes = NetworkStatisticSet.broadcast_bytes
        self.broadcast_packets = NetworkStatisticSet.broadcast_packets
        self.channel_list = []
        self.multicast_bytes = NetworkStatisticSet.multicast_bytes
        self.multicast_packets = NetworkStatisticSet.multicast_packets
        self.network_stats = []
        self._load(props)

    def _load(self, props: dict):
        if isinstance(props, dict):
            network = props.get('network')
            if isinstance(network, dict):
                for k, v in network.items():
                    a = NetworkStatisticSet._networkset_prop_dict.get(k)
                    if a is None or not hasattr(self, a):
                        continue
                    if isinstance(getattr(self, a), int):
                        setattr(self, a, int(v) if v else 0)
                    elif isinstance(getattr(self, a), list):
                        if a in ('network_stats'):
                            if isinstance(v, list):
                                self.network_stats.clear()
                                for stat in v:
                                    self.network_stats.append(NetworkStatistic(self._engine, stat))
                        elif a in ('channel_list'):
                            if isinstance(stat, list):
                                self.channel_list.clear()
                                for channel in v:
                                    self.network_stats.append(
                                        NetworkChannelStatistic(self._engine, channel))
                    else:
                        self._engine.logger.error(f'Unparsed property: {k}: {v}')


class NodeStatisticSet(StatisticSet):
    """NodeStatisticSet
    """
    _nodeset_prop_dict = {
        'nodes': 'node_stats',
        'resetCount': 'reset_count',
        'timeLimitReached': 'time_limit_reached'
    }

    node_stats = []
    """A list of NodeStatistic."""

    reset_count = 0
    """Nuber of times the Statistic Set has been reset."""

    time_limit_reached = False
    """Has the time limit been reached."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        StatisticSet.__init__(self, engine, props)
        self.node_stats = []
        self.reset_count = NodeStatisticSet.reset_count
        self.time_limit_reached = NodeStatisticSet.time_limit_reached
        self._load(props)

    def _load(self, props: dict):
        if isinstance(props, dict):
            for k, v in props.items():
                a = NodeStatisticSet._nodeset_prop_dict.get(k)
                if a is None or not hasattr(self, a):
                    continue
                if isinstance(getattr(self, a), int):
                    setattr(self, a, int(v) if v else 0)
                elif isinstance(getattr(self, a), bool):
                    setattr(self, a, v if v else False)
                elif isinstance(getattr(self, a), list):
                    self.node_stats.clear()
                    for stat in v:
                        if isinstance(stat, dict):
                            self.node_stats.append(NodeStatistic(self._engine, stat))
                else:
                    self._engine.logger.error(f'Unparsed property: {k}: {v}')


# NodesHierarchyStatistics


class ProtocolByIdStatisticSet(StatisticSet):
    """ProtocolByIdStatisticSet
    """
    _protocolbyidset_prop_dict = {
        'protocolsById': 'protocol_stats',
        'resetCount': 'reset_count',
        'timeLimitReached': 'time_limit_reached'
    }

    protocol_stats = []
    """A list of ProtocolStatistic."""

    reset_count = 0
    """Nuber of times the Statistic Set has been reset."""

    time_limit_reached = False
    """Has the time limit been reached."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        StatisticSet.__init__(self, engine, props)
        self.protocol_by_id_stats = []
        self.reset_count = ProtocolByIdStatisticSet.reset_count
        self.time_limit_reached = ProtocolByIdStatisticSet.time_limit_reached
        self._load(props)

    def _load(self, props: dict):
        if isinstance(props, dict):
            for k, v in props.items():
                a = ProtocolByIdStatisticSet._protocolbyidset_prop_dict.get(k)
                if a is None or not hasattr(self, a):
                    continue
                if isinstance(getattr(self, a), int):
                    setattr(self, a, int(v) if v else 0)
                elif isinstance(getattr(self, a), bool):
                    setattr(self, a, v if v else False)
                elif isinstance(getattr(self, a), list):
                    self.protocol_stats.clear()
                    for stat in v:
                        if isinstance(stat, dict):
                            self.protocol_by_id_stats.append(ProtocolStatistic(self._engine, stat))
                else:
                    self._engine.logger.error(
                        f'ProtocolByIdStatisticSet - Unparsed property: {k}: {v}')


class ProtocolStatisticSet(StatisticSet):
    """ProtocolStatisticSet
    """
    _protocolset_prop_dict = {
        'protocols': 'protocol_stats',
        'resetCount': 'reset_count',
        'timeLimitReached': 'time_limit_reached'
    }

    protocol_stats = []
    """A list of ProtocolStatistic."""

    reset_count = 0
    """Nuber of times the Statistic Set has been reset."""

    time_limit_reached = False
    """Has the time limit been reached."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        StatisticSet.__init__(self, engine, props)
        self.reset_count = ProtocolStatisticSet.reset_count
        self.protocol_stats = []
        self.time_limit_reached = ProtocolStatisticSet.time_limit_reached
        self._load(props)

    def _load(self, props: dict):
        if isinstance(props, dict):
            for k, v in props.items():
                a = ProtocolStatisticSet._protocolset_prop_dict.get(k)
                if a is None or not hasattr(self, a):
                    continue
                if isinstance(getattr(self, a), int):
                    setattr(self, a, int(v) if v else 0)
                elif isinstance(getattr(self, a), bool):
                    setattr(self, a, v if v else False)
                elif isinstance(getattr(self, a), list):
                    self.protocol_stats.clear()
                    for stat in v:
                        if isinstance(stat, dict):
                            self.protocol_stats.append(ProtocolStatistic(self._engine, stat))
                else:
                    self._engine.logger.error(f'ProtocolStatisticSet - Unparsed property: {k}: {v}')


class SizeStatisticSet(StatisticSet):
    """SizeStatisticSet
    """
    _sizeset_prop_dict = {
        'size': 'protocol_stats',
        'resetCount': 'reset_count',
        'timeLimitReached': 'time_limit_reached'
    }

    size_stats = []
    """A list of SizeStatistic."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        StatisticSet.__init__(self, engine, props)
        self.size_stats = []
        self._load(props)

    def _load(self, props: dict):
        if isinstance(props, dict):
            for k, v in props.items():
                if k == 'sizes':
                    self.size_stats.clear()
                    for stat in v:
                        if isinstance(stat, dict):
                            self.size_stats.append(SizeStatistic(self._engine, stat))
                elif k == 'clsid':
                    continue
                else:
                    self._engine.logger.error(f'SizeStatisticSet - Unparsed property: {k}: {v}')


class SummarySnapshot(object):
    """SummarySnapshot
    """

    _engine = None
    """OmniEngine that generated the Statistic Set."""

    id = None
    """Id of the snapshot."""

    name = ''
    """Name of the snapshot."""

    summary_stats = []
    """A list of SummaryStatistic"""

    def __init__(self, engine: OmniEngine, props: dict = None):
        self._engine = engine
        self.id = SummarySnapshot.id
        self.name = SummarySnapshot.name
        self.summary_stats = []
        self._load(props)

    def _load(self, props: dict):
        if isinstance(props, dict):
            self.id = get_id(props, 'id')
            self.name = props.get('name')
            stat_items = props.get('items')
            for stat in stat_items:
                if isinstance(stat, dict):
                    self.summary_stats.append(SummaryStatistic(self._engine, stat))


class SummaryStatisticSet(StatisticSet):
    """SummaryStatisticSet
    """

    current_id = None
    """"The id of the current snapshot."""

    summary_snapshots = []
    """A list of SummarySnapshot."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        StatisticSet.__init__(self, engine, props)
        self.current_id = SummaryStatisticSet.current_id
        self.summary_snapshots = []
        self._load(props)

    def _load(self, props: dict):
        if isinstance(props, dict):
            summary = props.get('summary')
            if isinstance(summary, dict):
                current_id = summary.get('currentSnapshotId')
                if current_id:
                    self.current_id = OmniId(current_id)
                snapshot_list = summary.get('snapshots')
                if isinstance(snapshot_list, list):
                    self.summary_snapshots.clear()
                    for snapshot in snapshot_list:
                        self.summary_snapshots.append(SummarySnapshot(self._engine, snapshot))

    def get_current_snapshot(self):
        return next((ss for ss in self.summary_snapshots if ss.id == self.current_id), None)


# WirelessChannelsStatistics
# WirelessNodesStatistics


def create_statistic_set(engine: OmniEngine, props: dict = None) -> StatisticSet:
    from .omniscript import get_id_class_names
    if isinstance(props, dict):
        class_id = OmniId(props['clsid'])
        id_class_names = get_id_class_names()
        class_name = id_class_names[class_id]
        if class_name == 'ApplicationFlowStats':
            return ApplicationFlowStatisticSet(engine, props)
        if class_name == 'ApplicationStats':
            return ApplicationStatisticSet(engine, props)
        if class_name == 'CallStats':
            return CallStatisticSet(engine, props)
        if class_name == 'ConversationStats':
            return ConversationStatisticSet(engine, props)
        if class_name == 'CountryStats':
            return CountryStatisticSet(engine, props)
        if class_name == 'ErrorStats':
            return ErrorStatisticSet(engine, props)
        if class_name == 'DashboardStats':  # Dashboard History Stats.
            return HistoryStatisticSet(engine, props)
        if class_name == 'NetworkStats':
            return NetworkStatisticSet(engine, props)
        if class_name == 'NodeStats':
            return NodeStatisticSet(engine, props)
        if class_name == 'ProtocolStats':
            return ProtocolStatisticSet(engine, props)
        if class_name == 'ProtocolStatsByID':
            return ProtocolByIdStatisticSet(engine, props)
        if class_name == 'SizeStats':
            return SizeStatisticSet(engine, props)
        if class_name == 'SummaryStats':
            return SummaryStatisticSet(engine, props)
        engine.logger.error(f'Unknown Statistic Set type: {class_name}')

    return None
