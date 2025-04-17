"""Summary Statistic class.
"""
# Copyright (c) LiveAction, Inc. 2024. All rights reserved.

import six

from .invariant import SummaryType
from .omniid import OmniId
from .peektime import PeekTime


class OmniEngine(object):
    pass


class SummaryStatistic(object):
    """The Summary Statistic class has the attributes of a capture's
    summary statistics.
    """

    _summary_prop_dict = {
        'flags': 'flags',
        'id': 'id',
        'label': 'name',
        'parentId': 'parent_id',
        'summary': 'stats',
        'type': 'value_type',
        'value': 'value'
    }

    class SummaryPair(object):
        bytes = 0
        packets = 0

        def __init__(self, bytes: int, packets: int):
            self.bytes = bytes
            self.packets = packets

        def __str__(self) -> str:
            return f'packets: {self.packets}, bytes: {self.bytes}'

    _engine = None
    """OmniEngine that generated the statistic."""

    flags = 0
    """Flags of the Snapshot."""

    id = None
    """Identifier of the Snapshot."""

    name = ''
    """Name of the Snapshot."""

    parent_id = None
    """Identifier of the Snapshot's parent."""

    value = None
    """The value of this Statistic."""

    value_type = 0
    """The type of data in value."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        self._engine = engine
        self.flags = SummaryStatistic.flags
        self.id = SummaryStatistic.id
        self.name = SummaryStatistic.name
        self.parent_id = SummaryStatistic.parent_id
        self.value = SummaryStatistic.value
        self.value_type = SummaryStatistic.value_type
        self._load(props)

    def __repr__(self) -> str:
        return 'SummaryStatistic:'

    def __str__(self) -> str:
        return 'SummaryStatistic:'

    def _load(self, props: dict):
        """Set attributes from a dictionary."""
        value = None
        if isinstance(props, dict):
            for k, v in props.items():
                a = SummaryStatistic._summary_prop_dict.get(k)
                if a is None or not hasattr(self, a):
                    continue
                if isinstance(getattr(self, a), six.string_types):
                    setattr(self, a, v if v else '')
                elif isinstance(getattr(self, a), bool):
                    setattr(self, a, (v != 'true') if v else False)
                elif isinstance(getattr(self, a), int):
                    setattr(self, a, int(v) if v else 0)
                elif getattr(self, a) is None:
                    if a in ('id', 'parent_id'):
                        setattr(self, a, OmniId(v))
                    elif a == 'value':
                        value = v
                else:
                    self._engine.logger.error(f'Unparsed property: {k}')
            if self.value_type and value:
                if self.value_type == SummaryType.DATE or self.value_type == SummaryType.TIME:
                    self.value = PeekTime(value)
                elif self.value_type == SummaryType.DURATION:
                    self.value = int(value)
                elif self.value_type == SummaryType.PACKETS:
                    self.value = int(value)
                elif self.value_type == SummaryType.BYTES:
                    self.value = int(value)
                elif self.value_type == SummaryType.PAIR:
                    if isinstance(value, dict):
                        self.value = SummaryStatistic.SummaryPair(
                            value.get('bytes'), value.get('packets'))
                elif self.value_type == SummaryType.INT:
                    self.value = int(value)
                elif self.value_type == SummaryType.DOUBLE:
                    self.value = float(value)
                else:
                    self._engine.logger.error(f'Unknown Summary Type: {self.value_type}')
