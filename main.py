"""
Network Investigation Tool - Main Entry Point
This tool performs network analysis given an IPv4 address and subnet mask.
It calculates network address, broadcast address, number of hosts, CIDR notation,
and determines if the network is classful or classless.
"""

import sys
import os

# Add core directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from core.utils import (
    validate_ip,
    validate_subnet_mask,
    get_network_address,
    get_broadcast_address,
    calculate_number_of_hosts,
    get_cidr_notation,
    is_classful
)

from core.output_string import (
    format_input_ip,
    format_subnet_mask,
    format_classful_status,
    format_network_address,
    format_broadcast_address,
    format_num_hosts,
    format_cidr_mask
)


def get_valid_ip():
    """
    Prompt user for IP address and validate it.

    Returns:
        Valid IP address as string
    """
    while True:
        ip = input("Enter IP address (x.x.x.x): ").strip()

        if validate_ip(ip):
            return ip
        else:
            print("Error: Invalid IP address. Please enter a valid IP in format x.x.x.x (0-255 for each octet)")


def get_valid_subnet_mask():
    """
    Prompt user for subnet mask and validate it.

    Returns:
        Valid subnet mask as string
    """
    while True:
        mask = input("Enter Subnet Mask (x.x.x.x): ").strip()

        if not validate_ip(mask):
            print("Error: Invalid subnet mask format. Please enter in format x.x.x.x (0-255 for each octet)")
            continue

        if not validate_subnet_mask(mask):
            print("Error: Invalid subnet mask. Mask must have contiguous 1s followed by 0s in binary.")
            continue

        return mask


def generate_output_file(ip_str, mask_str, student_id="123456789"):
    """
    Generate output file with network analysis results.

    Args:
        ip_str: IP address string
        mask_str: Subnet mask string
        student_id: Student ID for filename (default: "123456789")
    """
    # Calculate all network parameters
    network_addr = get_network_address(ip_str, mask_str)
    broadcast_addr = get_broadcast_address(ip_str, mask_str)
    num_hosts = calculate_number_of_hosts(mask_str)
    cidr = get_cidr_notation(mask_str)
    classful, class_name = is_classful(ip_str, mask_str)

    # Generate output lines using the provided functions
    output_lines = [
        format_input_ip(ip_str),
        format_subnet_mask(mask_str),
        format_classful_status(class_name),
        format_network_address(network_addr),
        format_broadcast_address(broadcast_addr),
        format_num_hosts(num_hosts),
        format_cidr_mask(cidr)
    ]

    # Create filename
    filename = f"subnet_info_{ip_str}_{student_id}.txt"

    # Write to file (functions already include newlines)
    with open(filename, 'w') as f:
        f.write(''.join(output_lines))

    print(f"\nOutput file generated: {filename}")

    # Also print to console
    print("\n=== Network Analysis Results ===")
    for line in output_lines:
        print(line)
    print("=" * 32)


def main():
    """
    Main function to run the network investigation tool.
    """
    print("=" * 50)
    print("Network Investigation Tool")
    print("=" * 50)
    print()

    # Get valid IP and subnet mask from user
    ip_address = get_valid_ip()
    subnet_mask = get_valid_subnet_mask()

    # Generate output file (use actual student ID here)
    # For this example, using "123456789" - replace with actual ID
    student_id = "123456789"
    generate_output_file(ip_address, subnet_mask, student_id)


if __name__ == "__main__":
    main()
