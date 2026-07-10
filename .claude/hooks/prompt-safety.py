#!/usr/bin/env python3

import json
import re
import sys

dangerous_patterns = [
    r"terraform destroy",
    r"rm\s+-rf",
    r"delete production",
    r"drop database",
    r"terminate instance",
    r"delete bucket",
    r"wipe environment"
]

data = json.load(sys.stdin)

prompt = data.get("prompt", "").lower()

for pattern in dangerous_patterns:
    if re.search(pattern, prompt):
        print(json.dumps({
            "decision": "block",
            "reason": "Potentially destructive action detected."
        }))
        sys.exit(0)

print(json.dumps({
    "decision": "allow"
}))