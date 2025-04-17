"""Size Statistic class.
"""
# Copyright (c) BlueCat Networks, Inc. 2025. All rights reserved.

import six


class OmniEngine(object):
    pass


class SizeStatistic(object):
    """the Size Statistic class has the attributes of a capture's
    packet size statistic.
    """

    _range_dict = {
        '<= 64': (0, 64),
        '65-127': (65, 127),
        '128-255': (128, 255),
        '256-511': (256, 511),
        '512-1023': (512, 1023),
        '1024-1518': (1024, 1518),
        '1519-2047': (1519, 2047),
        '2048-4095': (2048, 4095),
        '4096-8191': (4096, 8291),
        '8192-9017': (8192, 9017),
        '9018-9022': (9018, 9022),
        '>= 9023': (None, 9023),
    }

    _size_prop_dict = {
        'category': 'name',
        'packets': 'packets'
    }

    _engine = None
    """OmniEngine that generated the statistic."""

    name = ''
    """The name of the size statistic."""

    maximum = 0
    """The minimum value of the range."""

    minimum = 0
    """The minimum value of the range."""

    packets = 0
    """The number of packets in the range."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        self._engine = engine
        self.name = SizeStatistic.name
        self.packets = SizeStatistic.packets
        self._load(props)

    def __repr__(self) -> str:
        return f'SizeStatistic: {self.category} {self.packets}'

    def __str__(self) -> str:
        return f'SizeStatistic: {self.category} {self.packets}'

    def _load(self, props: dict = None):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            for k, v in props.items():
                a = SizeStatistic._size_prop_dict.get(k)
                if a is None or not hasattr(self, a):
                    continue
                if k == 'packets':
                    self.packets = int(v) if v is not None else 0
                elif a == 'name':
                    if v:
                        self.name = str(v)
                        range = SizeStatistic._range_dict.get(v)
                        if isinstance(range, tuple) and len(range) >= 2:
                            self.minimum = range[0]
                            self.maximum = range[1]
                else:
                    self._engine.logger.error(f'SizeStatistic - Unparsed property: {k}: {v}')
