#!/usr/bin/env python3
"""Ask a local open-weight model (Gemma via Ollama) to whisper about a shell command."""
import json
import os
import sys
import urllib.request

HOST = os.environ.get("HAUNT_HOST", "http://127.0.0.1:11434")
MODEL = os.environ.get("HAUNT_MODEL", "gemma3:4b")
PROMPT = (
    "You are the ghost living inside this user's terminal. "
    "In ONE short, eerie sentence (max 18 words), whisper a spooky comment about "
    "the shell command below and its exit status. No emojis, no quotes, no markdown.\n"
    "Command: {cmd}\nExit status: {status}"
)


def whisper(cmd: str, status: str) -> str:
    body = json.dumps({
        "model": MODEL,
        "prompt": PROMPT.format(cmd=cmd, status=status),
        "stream": False,
        "options": {"temperature": 0.9, "num_predict": 48},
    }).encode()
    req = urllib.request.Request(f"{HOST}/api/generate", body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)["response"].strip().splitlines()[0]


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: whisper.py <command> <exit-status>")
    try:
        print(f"\033[2;35m👻 {whisper(sys.argv[1], sys.argv[2])}\033[0m")
    except Exception:
        pass  # a ghost never explains itself
