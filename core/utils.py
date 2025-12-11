"""
Network calculation utilities for IP address and subnet analysis.
Contains functions for network address calculation, CIDR conversion, and class identification.
"""


def ip_to_binary(ip_str):
    """
    Convert IP address string to 32-bit binary string.

    Args:
        ip_str: IP address in dotted decimal format (e.g., "192.168.1.1")

    Returns:
        32-bit binary string
    """
    octets = ip_str.split('.')
    binary = ''.join([format(int(octet), '08b') for octet in octets])
    return binary


def binary_to_ip(binary_str):
    """
    Convert 32-bit binary string to IP address string.

    Args:
        binary_str: 32-bit binary string

    Returns:
        IP address in dotted decimal format
    """
    octets = []
    for i in range(0, 32, 8):
        octet = binary_str[i:i+8]
        octets.append(str(int(octet, 2)))
    return '.'.join(octets)


def validate_ip(ip_str):
    """
    Validate IP address format and values.

    Args:
        ip_str: IP address string to validate

    Returns:
        True if valid, False otherwise
    """
    parts = ip_str.split('.')

    # Check if exactly 4 octets
    if len(parts) != 4:
        return False

    # Check if each octet is between 0-255
    for part in parts:
        try:
            value = int(part)
            if value < 0 or value > 255:
                return False
        except ValueError:
            return False

    return True


def validate_subnet_mask(mask_str):
    """
    Validate subnet mask format and correctness.
    A valid subnet mask must have contiguous 1s followed by contiguous 0s.

    Args:
        mask_str: Subnet mask string to validate

    Returns:
        True if valid, False otherwise
    """
    if not validate_ip(mask_str):
        return False

    # Convert to binary and check if it's a valid mask (contiguous 1s)
    binary = ip_to_binary(mask_str)

    # Check if mask is contiguous (no 0s before 1s)
    found_zero = False
    for bit in binary:
        if bit == '0':
            found_zero = True
        elif found_zero and bit == '1':
            return False

    return True


def get_network_address(ip_str, mask_str):
    """
    Calculate network address by performing bitwise AND between IP and mask.

    Args:
        ip_str: IP address string
        mask_str: Subnet mask string

    Returns:
        Network address as string
    """
    ip_binary = ip_to_binary(ip_str)
    mask_binary = ip_to_binary(mask_str)

    # Perform bitwise AND
    network_binary = ''.join(['1' if ip_binary[i] == '1' and mask_binary[i] == '1' else '0'
                              for i in range(32)])

    return binary_to_ip(network_binary)


def get_broadcast_address(ip_str, mask_str):
    """
    Calculate broadcast address.
    Broadcast = Network address OR (NOT mask)

    Args:
        ip_str: IP address string
        mask_str: Subnet mask string

    Returns:
        Broadcast address as string
    """
    network_addr = get_network_address(ip_str, mask_str)
    network_binary = ip_to_binary(network_addr)
    mask_binary = ip_to_binary(mask_str)

    # Perform OR with inverted mask
    broadcast_binary = ''.join(['1' if mask_binary[i] == '0' else network_binary[i]
                                for i in range(32)])

    return binary_to_ip(broadcast_binary)


def calculate_number_of_hosts(mask_str):
    """
    Calculate number of usable hosts in the subnet.
    Formula: 2^(host_bits) - 2

    Args:
        mask_str: Subnet mask string

    Returns:
        Number of usable hosts
    """
    mask_binary = ip_to_binary(mask_str)
    host_bits = mask_binary.count('0')

    # 2^host_bits - 2 (subtract network and broadcast addresses)
    if host_bits == 0:
        return 0
    return (2 ** host_bits) - 2


def get_cidr_notation(mask_str):
    """
    Convert subnet mask to CIDR notation (number of network bits).

    Args:
        mask_str: Subnet mask string

    Returns:
        CIDR prefix length as integer
    """
    mask_binary = ip_to_binary(mask_str)
    return mask_binary.count('1')


def get_ip_class(ip_str):
    """
    Determine the class of an IP address based on first octet.
    Class A: 1-126 (first bit: 0)
    Class B: 128-191 (first bits: 10)
    Class C: 192-223 (first bits: 110)

    Args:
        ip_str: IP address string

    Returns:
        Class as string ('A', 'B', or 'C')
    """
    first_octet = int(ip_str.split('.')[0])

    if 1 <= first_octet <= 126:
        return 'A'
    elif 128 <= first_octet <= 191:
        return 'B'
    elif 192 <= first_octet <= 223:
        return 'C'
    else:
        return None


def get_default_mask_cidr(ip_class):
    """
    Get default CIDR notation for a given IP class.

    Args:
        ip_class: IP class ('A', 'B', or 'C')

    Returns:
        Default CIDR prefix length
    """
    if ip_class == 'A':
        return 8
    elif ip_class == 'B':
        return 16
    elif ip_class == 'C':
        return 24
    return None


def is_classful(ip_str, mask_str):
    """
    Determine if the network is classful or classless.
    Classful means the mask matches the default mask for the IP class.

    Args:
        ip_str: IP address string
        mask_str: Subnet mask string

    Returns:
        Tuple (is_classful, class_name)
        - is_classful: True if classful, False if classless
        - class_name: 'Class A', 'Class B', 'Class C', or 'Classless'
    """
    ip_class = get_ip_class(ip_str)

    if ip_class is None:
        return False, 'Classless'

    cidr = get_cidr_notation(mask_str)
    default_cidr = get_default_mask_cidr(ip_class)

    if cidr == default_cidr:
        return True, f'Class {ip_class}'
    else:
        return False, 'Classless'
