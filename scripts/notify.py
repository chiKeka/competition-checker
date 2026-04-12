#!/usr/bin/env python3
"""Dispatch a competition-checker notification to configured channels.

Usage: notify.py <notifications-config.json> <preset-name> <title> <body>

Channels handled here (deterministic IO):
  - stdout
  - slack (webhook POST)
  - desktop (osascript on macOS, notify-send on Linux)

Channels not handled here:
  - email (drafted by Claude via Gmail MCP; this script is not Claude-aware)

Exit codes:
  0  - at least one channel succeeded
  2  - invalid arguments
  3  - config file not readable
  4  - preset not found
  5  - all enabled channels failed
"""
from __future__ import annotations

import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path


def notify_stdout(title: str, body: str) -> bool:
    print(f"\n=== {title} ===")
    print(body)
    print("=" * (len(title) + 8))
    return True


def notify_slack(webhook_url: str, title: str, body: str) -> bool:
    payload = {
        "text": f"*{title}*\n{body}",
        "mrkdwn": True,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return 200 <= resp.status < 300
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        sys.stderr.write(f"Slack notify failed: {e}\n")
        return False


def notify_desktop(title: str, body: str) -> bool:
    if sys.platform == "darwin":
        safe_body = body.replace('"', '\\"').replace("\n", " ")
        safe_title = title.replace('"', '\\"')
        script = f'display notification "{safe_body}" with title "{safe_title}"'
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    if sys.platform.startswith("linux"):
        result = subprocess.run(
            ["notify-send", title, body],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    sys.stderr.write(f"Desktop notifications not supported on {sys.platform}\n")
    return False


def main() -> int:
    if len(sys.argv) != 5:
        sys.stderr.write(
            "Usage: notify.py <notifications-config.json> <preset-name> <title> <body>\n"
        )
        return 2

    config_path = Path(sys.argv[1])
    preset_name = sys.argv[2]
    title = sys.argv[3]
    body = sys.argv[4]

    if not config_path.is_file():
        sys.stderr.write(f"Config not found: {config_path}\n")
        return 3

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Invalid JSON in config: {e}\n")
        return 3

    preset = config.get("presets", {}).get(preset_name)
    if not preset:
        sys.stderr.write(f"Preset '{preset_name}' not found\n")
        return 4

    any_success = False
    all_attempted_failed = True

    if preset.get("stdout", True):
        any_success |= notify_stdout(title, body)
        all_attempted_failed = False

    slack_cfg = preset.get("slack") or {}
    if slack_cfg.get("enabled") and slack_cfg.get("webhook_url"):
        ok = notify_slack(slack_cfg["webhook_url"], title, body)
        any_success |= ok
        all_attempted_failed = all_attempted_failed and not ok

    desktop_cfg = preset.get("desktop") or {}
    if desktop_cfg.get("enabled"):
        ok = notify_desktop(title, body)
        any_success |= ok
        all_attempted_failed = all_attempted_failed and not ok

    if any_success:
        return 0
    if all_attempted_failed:
        return 5
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
