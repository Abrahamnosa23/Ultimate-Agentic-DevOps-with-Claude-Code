#!/usr/bin/env python3

import json
import re
import sys

dangerous_commands = [
    r"rm\s+-rf\s+/",
    r"rm\s+-rf\s+\*",
    r"rm\s+-rf\s+\.",
    r"sudo\s+rm\s+-rf",
    r"terraform\s+destroy",
    r"terraform\s+apply\s+-auto-approve",
    r"aws\s+s3\s+rm\s+.*--recursive",
    r"aws\s+s3\s+rb",
    r"aws\s+ec2\s+terminate-instances",
    r"aws\s+iam\s+delete-",
    r"aws\s+rds\s+delete-",
    r"git\s+push\s+--force",
    r"git\s+reset\s+--hard",
    r"chmod\s+-R\s+777"
]

try:
    data = json.load(sys.stdin)
except Exception:
    print(json.dumps({
        "decision": "block",
        "reason": "Unable to inspect tool input safely."
    }))
    sys.exit(0)

tool_name = data.get("tool_name", "")
tool_input = data.get("tool_input", {})

command = ""

if isinstance(tool_input, dict):
    command = tool_input.get("command", "")
else:
    command = str(tool_input)

command_lower = command.lower()

if tool_name.lower() == "bash":
    for pattern in dangerous_commands:
        if re.search(pattern, command_lower):
            print(json.dumps({
                "decision": "block",
                "reason": f"Blocked dangerous Bash command: {command}"
            }))
            sys.exit(0)

print(json.dumps({
    "decision": "allow"
}))