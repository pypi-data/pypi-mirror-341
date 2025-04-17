import pytest
import omniscript


@pytest.fixture
def ipv4_address():
    """ List of IPv4 Addresses Fixture """
    in_addresses = ['10.8.100.65', '10.8.100.*', '10.8.*.*', '10.*.*.*', '10.8.100.65/24',
                    '10.8.100.65/16', '10.8.100.65/8', '10.8.100.65/32']
    out_addresses = ['10.8.100.65', '10.8.100.0/24', '10.8.0.0/16', '10.0.0.0/8',
                     '10.8.100.0/24', '10.8.0.0/16', '10.0.0.0/8', '10.8.100.65']
    return in_addresses, out_addresses


@pytest.mark.smoke
def test_ipv4(ipv4_address):
    """ Testing IPv4 Address parsing """
    in_addresses, out_addresses = ipv4_address
    for (in_address, out_address) in zip(in_addresses, out_addresses):
        ipv4 = omniscript.IPv4Address(in_address)
        assert str(ipv4) == out_address, f'{in_address:>15}: {ipv4}'
