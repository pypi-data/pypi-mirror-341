"""History Statistic class.
"""
# Copyright (c) LiveAction, Inc. 2024. All rights reserved.

from .peektime import PeekTime


class OmniEngine(object):
    pass


class HistoryStatistic(object):
    """the History Statistic class has the attributes of a capture's
    History statistic.
    """

    _history_prop_dict = {
        'interval': 'interval',
        'samples': 'sample_list',
        'startTime': 'start_time'
    }

    _engine = None
    """OmniEngine that generated the statistic."""

    interval = 0
    """The interval of the history statistic."""

    sample_list = None
    """The history sample list."""

    start_time = None
    """The timestamp of the first packet."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        self._engine = engine
        self.interval = HistoryStatistic.interval
        self.sample_list = []
        self.start_time = HistoryStatistic.start_time
        self._load(props)

    def __repr__(self) -> str:
        return 'HistoryStatistic:'

    def __str__(self) -> str:
        return 'HistoryStatistic:'

    def _load(self, props: dict = None):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            for k, v in props.items():
                a = HistoryStatistic._history_prop_dict.get(k)
                if a == 'interval':
                    self.interval = int(v) if v is not None else 0
                elif a == 'sample_list':
                    if isinstance(v, list):
                        for sample in v:
                            self.sample_list.append(float(sample) if sample is not None else 0.0)
                elif a == 'start_time':
                    self.start_time = PeekTime(v) if v is not None else PeekTime()
                else:
                    self._engine.logger.error(f'Unparsed property: {k}: {v}')
