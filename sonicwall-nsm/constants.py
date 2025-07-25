"""
Copyright start
MIT License
Copyright (c) 2025 Fortinet Inc
Copyright end
"""

FILTER_TYPE = {
    "Source Zone to Destination Zone": 1,
    "Source Address to Destination Address": 2,
    "Source Port to Destination Port": 3
}

RULE_TYPE = {
    "Access Rules": "access_rules",
    "Security Policies": "security_policies"
}

OBJECT_TYPE = {
    "Host (Single IP Address)": "host",
    "Network (IP/Subnet)": "network",
    "Range (Start IP - End IP)": "range",
    "FQDN (Domain Name)": "fqdn",
    "MAC Address": "mac"
}
