"""Country Statistic class.
"""
# Copyright (c) LiveAction, Inc. 2024. All rights reserved.

import six
from .peektime import PeekTime


class OmniEngine(object):
    pass


class CountryStatistic(object):
    """the Country Statistic class has the attributes of a capture's
    node statistic.
    """

    _country_prop_dict = {
        'bytesFrom': 'bytes_from',
        'bytesTo': 'bytes_to',
        'code': 'code',
        'duration': 'duration',
        'firstTimeFrom': 'first_time_from',
        'firstTimeTo': 'first_time_to',
        'lastTimeFrom': 'last_time_from',
        'lastTimeTo': 'last_time_to',
        'name': 'name',
        'packetsFrom': 'packets_from',
        'packetsTo': 'packets_to',
    }

    _engine = None
    """OmniEngine that generated the statistic."""

    bytes_from = 0
    """ """

    bytes_to = 0
    """ """

    code = ''
    """ """

    duration = 0
    """Duration of this statistic."""

    first_time_from = None
    """ """

    first_time_to = None
    """ """

    last_time_from = None
    """ """

    last_time_to = None
    """ """

    name = ''
    """ """

    packets_from = 0
    """ """

    packets_to = 0
    """ """

    def __init__(self, engine: OmniEngine, props: dict = None):
        self._engine = engine
        self.bytes_from = CountryStatistic.bytes_from
        self.bytes_to = CountryStatistic.bytes_to
        self.code = CountryStatistic.code
        self.duration = CountryStatistic.duration
        self.first_time_from = CountryStatistic.first_time_from
        self.first_time_to = CountryStatistic.first_time_to
        self.last_time_from = CountryStatistic.last_time_from
        self.last_time_to = CountryStatistic.last_time_to
        self.name = CountryStatistic.name
        self.packets_from = CountryStatistic.packets_from
        self.packets_to = CountryStatistic.packets_to
        self._load(props)

    def __repr__(self) -> str:
        return 'CountryStatistic:'

    def __str__(self) -> str:
        return 'CountryStatistic:'

    def _load(self, props: dict = None):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            for k, v in props.items():
                a = CountryStatistic._country_prop_dict.get(k)
                if a is None or not hasattr(self, a):
                    continue
                if isinstance(getattr(self, a), int):
                    setattr(self, a, int(v) if v else 0)
                elif isinstance(getattr(self, a), six.string_types):
                    setattr(self, a, v if v else '')
                elif getattr(self, a) is None:
                    if a in ('first_time_from', 'first_time_to',
                             'last_time_from', 'last_time_to'):
                        setattr(self, a, PeekTime(v))
                else:
                    self._engine.logger.error(f'Unparsed property: {k}: {v}')
