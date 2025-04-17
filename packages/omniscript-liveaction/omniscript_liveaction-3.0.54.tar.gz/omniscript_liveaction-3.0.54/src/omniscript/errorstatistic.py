"""Error Statistic class.
"""
# Copyright (c) LiveAction, Inc. 2024. All rights reserved.


class OmniEngine(object):
    pass


class ErrorStatistic(object):
    """the Error Statistic class has the attributes of a capture's
    Error statistic.
    """

    _engine = None
    """OmniEngine that generated the statistic."""

    category = ''
    """The category of the error statistic."""

    packets = 0
    """The number of packets in the category."""

    supported = False
    """Is this category supported."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        self._engine = engine
        self.category = ErrorStatistic.category
        self.packets = ErrorStatistic.packets
        self.supported = ErrorStatistic.supported
        self._load(props)

    def __repr__(self) -> str:
        return f'ErrorStatistic: {self.category}'

    def __str__(self) -> str:
        return f'ErrorStatistic: {self.category}'

    def _load(self, props: dict = None):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            for k, v in props.items():
                if k == 'category':
                    self.category = str(v) if v is not None else ''
                elif k == 'packets':
                    self.packets = int(v) if v is not None else 0
                elif k == 'supported':
                    self.supported = bool(v) if v is not None else False
                else:
                    self._engine.logger.error(f'Unparsed property: {k}: {v}')
