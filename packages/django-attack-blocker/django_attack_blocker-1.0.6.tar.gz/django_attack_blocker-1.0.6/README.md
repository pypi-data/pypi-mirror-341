# Django Attack Blocker

A machine learning-based IP blocking library for Django applications to detect and prevent malicious network traffic.

## Overview

Django Attack Blocker is a demonstration library that shows how trained models on the UNSW dataset can be used to protect specific routes in Django applications. The library uses machine learning to identify potentially malicious network traffic and can automatically block IP addresses based on the model's predictions.

This middleware integrates seamlessly with Django applications and can be used to protect sensitive routes from various network attacks such as DoS, DDoS, reconnaissance, and exploitation attempts.

## Features

- Machine learning-based detection of malicious network traffic
- IP address blocking and whitelisting capabilities
- Configurable blocking thresholds
- Temporary and permanent IP blocks
- Django view decorators for easy integration
- Built-in caching of block decisions for performance
- Support for trusted IP ranges
- Detailed statistics tracking
- Manual IP management functions for block/unblock operations

## Installation

```bash
pip install django_attack_blocker
```

## Required Files

The required model and encoder files can be downloaded from the repository:

- `model.pkl`: The trained machine learning model
- `encoder.pkl`: The feature encoder for preprocessing

## Usage

### Basic Setup

```python
from django_attack_blocker import MLIPBlocker
from django_attack_blocker import with_ip_blocking

# Initialize the blocker with your model
blocker = MLIPBlocker(
    model_path='path/to/model.pkl',
    encoder_path='path/to/encoder.pkl',
    block_threshold=0.5,  # Confidence threshold for blocking
    trusted_ips=['127.0.0.1', '192.168.1.0/24'],  # Always allow these IPs
    blocked_ips=['10.0.0.5']  # Always block these IPs
)

# Protect a view using decorator
@with_ip_blocking(blocker)
def my_protected_view(request):
    # Your view code here
    return JsonResponse({"status": "success"})
```

The complete list of parameters are shown in this table

| Parameter         | Type   | Default    | Description                                                                                                        |
| ----------------- | ------ | ---------- | ------------------------------------------------------------------------------------------------------------------ |
| `model_path`      | string | _Required_ | Path to the pickled ML model file (.pkl)                                                                           |
| `encoder_path`    | string | _Required_ | Path to the pickled encoder file (.pkl)                                                                            |
| `blocklist_path`  | string | None       | Path to a file with IPs to always block                                                                            |
| `block_threshold` | float  | 0.5        | Confidence threshold for blocking decisions (0.0-1.0), where higher values require more confidence before blocking |
| `block_timeout`   | int    | None       | Time duration in seconds for which an IP stays blocked. If None, blocks the IP permanently                         |
| `trusted_ips`     | list   | None       | List of IP addresses or CIDR ranges (e.g. '192.168.1.0/24') that will always be allowed                            |
| `blocked_ips`     | list   | None       | List of IP addresses or CIDR ranges that will always be blocked                                                    |

> **Note**: The model and encoder files (`model.joblib` and `encoder.pkl`) can be found in the `weights` directory of the repository.

### Using Different Block Types

The blocker now supports different types of IP blocking:

```python
# Use temporary blocking that relies on the cache timeout
@with_ip_blocking(blocker, type="temporary")
def temporarily_protected_view(request):
    return JsonResponse({"status": "temporary protection active"})

# Use permanent blocking that will persist until server restart
@with_ip_blocking(blocker, type="permanent")
def permanently_protected_view(request):
    return JsonResponse({"status": "permanent protection active"})
```

### Manual IP Management Functions

```python
# Import the helper functions
from django_attack_blocker import block_ip, unblock_ip, get_blocker_stats

# Block an IP temporarily
block_ip(blocker, ip='192.168.1.100', duration=3600)  # Block for 1 hour

# Block an IP permanently
block_ip(blocker, ip='192.168.1.101')  # No duration means permanent

# Unblock an IP address
unblock_ip(blocker, ip='192.168.1.100')

# Get statistics about blocked requests
stats = get_blocker_stats(blocker)
print(stats)
```

The model expects logs in a specific format, with the following columns required:

```
dur, proto, service, state, spkts, dpkts, sbytes, dbytes, rate, sttl, dttl,
sload, dload, sloss, dloss, sinpkt, dinpkt, sjit, djit, swin, stcpb, dtcpb,
dwin, tcprtt, synack, ackdat, smean, dmean, trans_depth, response_body_len,
ct_srv_src, ct_state_ttl, ct_dst_ltm, ct_src_dport_ltm, ct_dst_sport_ltm,
ct_dst_src_ltm, is_ftp_login, ct_ftp_cmd, ct_flw_http_mthd, ct_src_ltm,
ct_srv_dst, is_sm_ips_ports
```

### Sample Request Body

The request body should contain a "log" object with the network traffic features:

```json
{
  "log": {
    "dur": 0.0,
    "proto": 0,
    "service": 0,
    "state": 1,
    "spkts": 1,
    "dpkts": 0,
    "sbytes": 2048,
    "dbytes": 0,
    "rate": 0,
    "sttl": 64,
    "dttl": 64,
    "sload": 0.0,
    "dload": 0.0,
    "sloss": 0,
    "dloss": 0,
    "sinpkt": 0.0,
    "dinpkt": 0.0,
    "sjit": 0.0,
    "djit": 0.0,
    "swin": 65535,
    "dwin": 65535,
    "stcpb": 0,
    "dtcpb": 0,
    "tcprtt": 0.0,
    "synack": 0.0,
    "ackdat": 0.0,
    "smean": 2048,
    "dmean": 0,
    "trans_depth": 1,
    "response_body_len": 0,
    "ct_srv_src": 1,
    "ct_state_ttl": 1,
    "ct_dst_ltm": 1,
    "ct_src_dport_ltm": 1,
    "ct_dst_sport_ltm": 1,
    "ct_dst_src_ltm": 1,
    "ct_src_ltm": 1,
    "ct_srv_dst": 1,
    "is_ftp_login": 0,
    "ct_ftp_cmd": 0,
    "ct_flw_http_mthd": 1,
    "is_sm_ips_ports": 0
  }
}
```

## Creating an Example Django View with IP Blocking

```python
from django.http import JsonResponse
from django_attack_blocker import MLIPBlocker, with_ip_blocking, block_ip, unblock_ip

# Initialize the blocker
blocker = MLIPBlocker(
    model_path='path/to/model.pkl',
    encoder_path='path/to/encoder.pkl',
    block_threshold=0.7
)

# Protected view with temporary blocking
@with_ip_blocking(blocker, type="temporary")
def process_traffic(request):
    # Process the request
    return JsonResponse({"status": "processed"})

# Admin view for manual IP management
def manage_ips(request):
    action = request.GET.get('action')
    ip = request.GET.get('ip')
    duration = request.GET.get('duration')

    if action == 'block':
        if duration:
            block_ip(blocker, ip=ip, duration=int(duration))
            return JsonResponse({"status": f"Blocked {ip} for {duration} seconds"})
        else:
            block_ip(blocker, ip=ip)
            return JsonResponse({"status": f"Blocked {ip} permanently"})
    elif action == 'unblock':
        unblock_ip(blocker, ip=ip)
        return JsonResponse({"status": f"Unblocked {ip}"})
    else:
        return JsonResponse({"error": "Invalid action"}, status=400)
```

## UNSW Dataset

This library is designed to work with models trained on the UNSW-NB15 dataset, which contains a wide range of network attacks such as:

- Fuzzers
- Analysis
- Backdoors
- DoS
- Exploits
- Generic
- Reconnaissance
- Shellcode
- Worms

The library can block IP addresses either permanently or temporarily:

- Permanent blocking: The IP is added to the blocklist and stays there until the server restarts or the IP is manually unblocked.
- Temporary blocking: The IP address is cached for the specified block time (set via `block_timeout`).

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
