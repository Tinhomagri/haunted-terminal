#!/usr/bin/env python3
"""Measure warm latency per model: python3 bench.py gemma3:4b gemma3:12b"""
import statistics, sys, time, os
import whisper

CASES = [("ls /nope", "2"), ("git push --force", "1"), ("rm -rf node_modules", "0"),
         ("sudo apt update", "0"), ("python3 app.py", "1")]
for model in sys.argv[1:]:
    whisper.MODEL = model
    t0 = time.time(); whisper.whisper("echo warmup", "0"); cold = time.time() - t0
    times, outs = [], []
    for cmd, st in CASES:
        t = time.time(); outs.append(whisper.whisper(cmd, st)); times.append(time.time() - t)
    print(f"## {model}: first call {cold:.1f}s | warm median {statistics.median(times):.1f}s, max {max(times):.1f}s")
    for (cmd, _), o in zip(CASES, outs):
        print(f"  $ {cmd}\n    {o}")
