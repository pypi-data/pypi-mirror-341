"""Application Statistic class.
"""
# Copyright (c) LiveAction, Inc. 2024. All rights reserved.

import six
from .mediaspecification import MediaSpecification
from .peektime import PeekTime


class OmniEngine(object):
    pass


class ApplicationStatistic(object):
    """the Application Statistic class has the attributes of a capture's
    application statics.
    """

    _app_prop_dict = {
        'bytes': 'bytes',
        'color': 'color',
        'duration': 'duration',
        'firstTime': 'first_time',
        'id': 'id_code',
        'lastTime': 'last_time',
        'mediaSpec': 'media_spec',
        'name': 'name',
        'packets': 'packets',
    }

    _engine = None
    """OmniEngine that generated the statistic."""

    bytes = 0
    """Number of bytes in the packets of the application captured."""

    color = 0
    """The application's display color."""

    duration = 0
    """Duration of this snapshot."""

    first_time = None
    """First time the application was captured."""

    id_code = None
    """Identifing code of the application."""

    last_time = None
    """Last time the application was captured."""

    media_spec = None
    """The Media Specification of the traffic."""

    name = ''
    """The name of the application."""

    packets = 0
    """Number of packets of the application captured."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        self._engine = engine
        self.bytes = ApplicationStatistic.bytes
        self.color = None  # Need to parse the value
        self.duration = ApplicationStatistic.duration
        self.first_time = ApplicationStatistic.first_time
        self.id_code = ApplicationStatistic.id_code
        self.last_time = ApplicationStatistic.last_time
        self.media_spec = ApplicationStatistic.media_spec
        self.name = ApplicationStatistic.name
        self.packets = ApplicationStatistic.packets
        self._load(props)

    def __repr__(self) -> str:
        return f'ApplicationStatistic: {self.name}'

    def __str__(self) -> str:
        return f'ApplicationStatistic: {self.name}'

    def _load(self, props: dict = None):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            for k, v in props.items():
                a = ApplicationStatistic._app_prop_dict.get(k)
                if a is None or not hasattr(self, a):
                    continue
                if isinstance(getattr(self, a), int):
                    setattr(self, a, int(v) if v else 0)
                elif isinstance(getattr(self, a), six.string_types):
                    setattr(self, a, v if v else '')
                elif isinstance(getattr(self, a), float):
                    setattr(self, a, float(v) if v else 0.0)
                elif getattr(self, a) is None:
                    if a in ('id_code'):
                        if isinstance(v, str):
                            setattr(self, a, six.string_types(v))
                        elif isinstance(v, int):
                            setattr(self, a, int(v) if v else 0)
                        else:
                            self._engine.logger.error(f'Invalue Id Code value: {v}')
                    elif a in ('first_time', 'last_time'):
                        setattr(self, a, PeekTime(v))
                    elif a in ('color'):
                        self.color = int(v.strip('#'), 16)
                    elif a in ('media_spec'):
                        self.media_spec = MediaSpecification(v)
                    else:
                        self._engine.logger.error(f'Unparsed property Type: {k}: {v}')
                else:
                    self._engine.logger.error(f'Unparsed property: {k}: {v}')
            if self.color is None:
                self.color = 0
