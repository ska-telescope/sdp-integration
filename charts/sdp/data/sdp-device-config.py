"""Generate SDP Tango device configuration."""

import argparse
import json

parser = argparse.ArgumentParser(description='Generate SDP Tango device configuration')
parser.add_argument('telescope', type=str, choices=['low', 'mid'], help='Telescope prefix')
parser.add_argument('nsubarray', type=int, help='Number of subarrays')

args = parser.parse_args()

# Define servers

servers = {}

# Add master to servers

device_name = args.telescope + '_sdp/elt/master'
device_config = {}
master = {'1': {'SDPMaster': {device_name: device_config}}}
servers['SDPMaster'] = master

# Add subarrays to servers

subarrays = {}
for i in range(args.nsubarray):
    subarray_id = f'{i+1}'
    device_name = args.telescope + '_sdp/elt/subarray_' + subarray_id
    device_config = {}
    subarrays[subarray_id] = {
        'SDPSubarray': {device_name: device_config}
    }
servers['SDPSubarray'] = subarrays

# Add servers to config

config = {'servers': servers}

# Output config as JSON

print(json.dumps(config, indent=2))
