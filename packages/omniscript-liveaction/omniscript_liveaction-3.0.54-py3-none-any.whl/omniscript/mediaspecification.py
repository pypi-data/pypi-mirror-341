"""MediaSpecification class.
"""
# Copyright (c) LiveAction, Inc. 2022. All rights reserved.
# Copyright (c) Savvius, Inc. 2013-2019. All rights reserved.
# Copyright (c) WildPackets, Inc. 2013-2014. All rights reserved.

import six

from .invariant import MediaSpecification_Class, MediaSpecification_Type


class MediaSpecification(object):
    """The Media Information class.
    """

    _mediaspec_prop_dict = {
        'data': 'data',
        'mask': 'mask',
        'msclass': 'media_class',
        'type': 'media_type'
    }

    _medaispec_size_table = (
        0, 8, 8, 8,  # NONE, ETHERNET_PROTOCOL, LSAP, SNAP
        8, 8, 8, 8,  # APPLETALK_LAP, APPLETALK_DDP, MAC_CONTROL, PROTOCOL_ID_HIERARCHY
        8, 8, 8, 8,  # APPLICATION_ID, PROTOCOL, ETHERNET_ADDRESS, TOKENRING_ADDRESS
        8, 8, 8, 8,  # APPLETALK_LAP_ADDRESS, WIRELESS_ADDRESS, PACE2_APPLICATION_ID
        0, 0, 0, 0, 0,  # 15 - 19 are Undefined
        8, 8, 8, 8,  # APPLETALK_ADDRESS, IP_ADDRESS, DECNET_ADDRESS, OTHER_ADDRESS
        8, 8,        # IPV6_ADDRESS,  IPX_ADDRESS
        0, 0, 0, 0, 0, 0,  # 26 - 31 are Undefined
        8, 8, 8, 8,  # ERROR, AT_PORT, IP_PORT, NETWARE_PORT
        8, 8, 8, 8,  # TCP_PORT_PAIR, WAN_PPP_PROTOCOL, WAN_FRAMERELAY_PROTOCOL, WAN_X25_PROTOCOL
        8, 8, 8, 8,  # WAN_X25E_PROTOCOL, WAN_IPARS_PROTOCOL, WAN_U200_PROTOCOL, WAN_DLCI_ADDRESS
        8            # WAN_Q931_PROTOCOL
    )

    data = ""
    """The value."""

    mask = 0
    """The mask that extracts the value from the data."""

    media_class = 0
    """Class/type of media specification."""

    media_type = 0
    """The media type."""

    def __init__(self, props=None):
        self.data = MediaSpecification.data
        self.mask = MediaSpecification.mask
        self.media_class = MediaSpecification.media_class
        self.media_type = MediaSpecification.media_type
        self._load(props)

    def __str__(self):
        return f'MediaSpecification: {self.data}'

    def _load(self, props):
        if isinstance(props, dict):
            for k, v in props.items():
                a = MediaSpecification._mediaspec_prop_dict.get(k)
                if a is None or not hasattr(self, a):
                    continue
                if isinstance(getattr(self, a), int):
                    setattr(self, a, int(v) if v else 0)
                elif isinstance(getattr(self, a), six.string_types):
                    setattr(self, a, v if v else '')
        if self.mask == 0:
            self.mask = None
        else:
            pass

    def get_value(self):
        if self.media_class == MediaSpecification_Class.ADDRESS:
            return 0
        elif self.media_class == MediaSpecification_Class.PORT:
            if self.media_type == MediaSpecification_Type.IP_PORT:
                return int(self.data, 16)
        elif self.media_class == MediaSpecification_Class.PROTOCOL:
            return 0
        return None
