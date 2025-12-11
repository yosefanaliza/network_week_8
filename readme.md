# Network Investigation Tool

## Student Information
- **Name**: [Your Name]
- **Class**: [Your Class]
- **ID**: 123456789

## Project Description
This project is a Python-based network investigation tool that analyzes IPv4 addresses and subnet masks.

## Features
- IP address and subnet mask validation
- Network address calculation
- Broadcast address calculation
- Number of usable hosts calculation
- CIDR notation conversion
- Classful vs Classless network identification

## Usage
```bash
python main.py
```

Follow the prompts to enter an IP address and subnet mask.

## Project Structure
```
network_tool/
├── core/
│   ├── output_string.py  # Output formatting functions
│   └── utils.py          # Network calculation utilities
├── main.py               # Main entry point
└── readme.md             # This file
```

## Requirements
- Python 3.6 or higher
- No external libraries required

## Notes
- This implementation uses manual bit manipulation and calculations
- No ipaddress library or similar networking libraries are used
- All calculations are performed manually as per test requirements
