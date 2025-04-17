"""Call Statistic class.
"""
# Copyright (c) LiveAction, Inc. 2024. All rights reserved.

from .peektime import PeekTime


class OmniEngine(object):
    pass


class CallStatistic(object):
    """the CAll Statistic class has the attributes of a capture's
    call statistic.
    """

    class CodecStats(object):
        def __init__(self, props):
            self.average_mos = 0
            self.calls = 0
            self.flows = 0
            self.maximum_mos = 0
            self.minimum_mos = 0
            self._load(props)

        def _load(self, props):
            if isinstance(props, dict):
                for k, v in props.items():
                    if k == 'averageMOS':
                        self.average_mos = int(v) if v else 0
                    elif k == 'calls':
                        self.calls = int(v) if v else 0
                    elif k == 'flows':
                        self.flows = int(v) if v else 0
                    elif k == 'maximumMOS':
                        self.maximum_mos = int(v) if v else 0
                    elif k == 'minimumMOS':
                        self.minimum_mos = int(v) if v else 0

    class Codec(object):
        def __init__(self, props):
            self.codec_id = 0
            self.name = ""
            self.samples = []
            self._load(props)

        def _load(self, props):
            if isinstance(props, dict):
                for k, v in props.items():
                    if k == 'codec':
                        self.codec_id = int(k) if k else 0
                    elif k == 'name':
                        self.name = str(k) if k else ''
                    elif k == 'samples':
                        if isinstance(k, list):
                            self.samples.append(CallStatistic.CodecStats(v))

    class CodecQuality(object):
        def __init__(self, props):
            self.codec_list = []
            self.interval = 0
            self.start_time = None
            self._load(props)

        def _load(self, props):
            if isinstance(props, dict):
                for k, v in props.items():
                    if k == 'interval':
                        self.interval = int(v) if v else 0
                    elif k == 'codecs' and isinstance(v, list):
                        for codec in v:
                            self.codec_list.append(CallStatistic.Codec(v))
                    elif k == 'startTime':
                        self.start_time = PeekTime(v)

    class QualityDistribution(object):
        def __init__(self, props):
            self.bad = 0
            self.fair = 0
            self.good = 0
            self.poor = 0
            self.unknown = None
            self._load(props)

        def __str__(self) -> str:
            str = f'good: {self.good}, fair: {self.fair}, poor: {self.fair}, bad: {self.bad}'
            if isinstance(self.unknown, int):
                str += f', unknown: {self.unknown}'
            return str

        def _load(self, props):
            if isinstance(props, dict):
                for k, v in props.items():
                    if k and hasattr(self, k):
                        setattr(self, k, int(v) if v else 0)

    class Quality(object):
        def __init__(self, props):
            self.interval = 0
            self.sample_list = None
            self.start_time = None
            self._load(props)

        def _load(self, props):
            if isinstance(props, dict):
                for k, v in props.items():
                    if k == 'interval':
                        self.interval = int(v) if v else 0
                    elif k == 'samples' and isinstance(v, list):
                        self.sample_list = self._create_quality_distribution_list(v)
                    elif k == 'startTime':
                        self.start_time = PeekTime(v)

        def _create_quality_distribution_list(self, props):
            quality_list = []
            if isinstance(props, list):
                for prop in props:
                    if isinstance(prop, dict):
                        quality_list.append(CallStatistic.QualityDistribution(prop))
            return quality_list

    class Utilization(object):
        def __init__(self, props):
            self.interval = 0
            self.sample_list = []
            self.start_time = None
            self._load(props)

        def _load(self, props):
            if isinstance(props, dict):
                for k, v in props.items():
                    if k == 'interval':
                        self.interval = int(v) if v else 0
                    elif k == 'samples' and isinstance(v, list):
                        for sample in v:
                            self.sample_list.append(float(sample))
                    elif k == 'startTime':
                        self.start_time = PeekTime(v)

    class UtilizationList(object):
        def __init__(self, props):
            self.utilization_list = []
            self._load(props)

        def _load(self, props):
            if isinstance(props, list):
                for prop in props:
                    if isinstance(prop, dict):
                        self.utilization_list.append(CallStatistic.Utilization(prop))

    _call_prop_dict = {
        'allCalls': 'all_quality_distribution',
        'callCodecQuality': 'codec_quality',
        'callQuality': 'call_quality',
        'openCalls': 'open_quality_distribution',
        'qualityDistribution': 'quality_distribution',
        'utilization': 'utilization'
    }

    _engine = None
    """OmniEngine that generated the statistic."""

    all_quality_distribution = None
    """Call quality distribution of all calls."""

    codec_quality_list = None
    """Quality of the call codec."""

    open_quality_distribution = None
    """Call quality distribution of all open calls."""

    quality_utilization_list = None
    """The call quality."""

    utilization_list = None
    """List of Call Utilization objects."""

    def __init__(self, engine: OmniEngine, props: dict = None):
        self._engine = engine
        self.all_quality_distribution = CallStatistic.all_quality_distribution
        self.codec_quality_list = []
        self.open_quality_distribution = CallStatistic.open_quality_distribution
        self.quality_utilization_list = []
        self.utilization_list = CallStatistic.utilization_list
        self._load(props)

    def __repr__(self) -> str:
        return f'CallStatistic: {self.name}'

    def __str__(self) -> str:
        return f'CallStatistic: {self.name}'

    def _create_codec_quality_list(self, props):
        quality_list = []
        if isinstance(props, list):
            for prop in props:
                if isinstance(prop, dict):
                    quality_list.append(CallStatistic.CodecQuality(prop))
        return quality_list

    def _create_quality_list(self, props):
        quality_list = []
        if isinstance(props, list):
            for prop in props:
                if isinstance(prop, dict):
                    quality_list.append(CallStatistic.Quality(prop))
        return quality_list

    def _create_utilization_list(self, props):
        utilization_list = []
        if isinstance(props, list):
            for prop in props:
                if isinstance(prop, dict):
                    utilization_list.append(CallStatistic.Utilization(prop))
        return utilization_list

    def _load(self, props: dict = None):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            for k, v in props.items():
                a = CallStatistic._call_prop_dict.get(k)
                if a == 'quality_distribution' and isinstance(v, dict):
                    ac = v.get('allCalls')
                    if isinstance(ac, dict):
                        self.all_quality_distribution = CallStatistic.QualityDistribution(ac)
                    oc = v.get('openCalls')
                    if isinstance(oc, dict):
                        self.open_quality_distribution = CallStatistic.QualityDistribution(oc)
                elif a == 'call_quality':
                    self.quality_utilization_list = self._create_quality_list(v)
                elif a == 'codec_quality':
                    self.codec_quality_list = self._create_codec_quality_list(v)
                elif a == 'utilization' and isinstance(v, list):
                    self.utilization_list = self._create_utilization_list(v)
                else:
                    self._engine.logger.error(f'Unparsed property: {k}: {v}')
