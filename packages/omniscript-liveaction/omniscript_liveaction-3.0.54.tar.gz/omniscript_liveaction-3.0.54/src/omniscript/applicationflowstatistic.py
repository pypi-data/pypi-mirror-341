"""Application Flow Statistic class.
"""
# Copyright (c) BlueCat Networks, Inc. 2025. All rights reserved.
# Copyright (c) LiveAction, Inc. 2024. All rights reserved.

import six


class OmniEngine(object):
    pass


class ApplicationFlowStatistic(object):
    """the Application Flow Statistic class has the attributes of a capture's
    Application Flow statistic.
    """

    _appflow_prop_dict = {
        'color': 'color',
        'flows': 'flow_count',
        'id': 'id',
        'name': 'name'
    }

    _engine = None
    """OmniEngine that generated the statistic."""

    color = 0
    """Color assigned to the application."""

    flow_count = 0
    """Number of flows."""

    id_code = 0
    """Identification code of the protocol."""

    id_name = ''
    """Identification name of the protocol."""

    name = ''
    """Name of this Application Flow."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        self._engine = engine
        self.color = ApplicationFlowStatistic.color
        self.flow_count = ApplicationFlowStatistic.flow_count
        self.id_code = ApplicationFlowStatistic.id_code
        self.id_name = ApplicationFlowStatistic.id_name
        self.name = ApplicationFlowStatistic.name
        self._load(props)

    def __repr__(self) -> str:
        return 'ApplicationFlowStatistic:'

    def __str__(self) -> str:
        return 'ApplicationFlowStatistic:'

    def _load(self, props: dict = None):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            for k, v in props.items():
                a = ApplicationFlowStatistic._appflow_prop_dict.get(k)
                if a is None or not hasattr(self, a):
                    continue
                if a == 'color':
                    self.color = int(v.strip('#'), 16)
                elif a == 'flow_count':
                    self.flow_count = int(v) if v else 0
                elif a == 'id':
                    if isinstance(v, int):
                        self.id_code = v
                    elif isinstance(v, six.string_types):
                        self.id_name = v
                elif a == 'name':
                    self.name = str(v) if v else ''
                else:
                    self._engine.logger.error(
                        f'ApplicationFlowStatistic - Unparsed property: {k}: {v}')
