---
title: A ghost in my shell, powered by a local Gemma
published: false
tags: devchallenge, hf26challenge, ai, opensource
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge: Week 4](https://dev.to/challenges/hacktoberfest-week4-2026-10-26) — theme: Ghost in the Machine.*

## What I built

**Haunted Terminal**: a ghost that lives in your shell. Every few commands (1 in 4 by default), it whispers one eerie sentence about what you just ran and whether it failed.

```
$ rm -rf node_modules
👻 A clean sweep… but something vital vanished with those modules, didn't it?
```

It is about 80 lines: a Bash hook (`haunt.sh`) on `PROMPT_COMMAND` and a stdlib-only Python script (`whisper.py`) that calls Ollama's `/api/generate`. No dependencies, no API key, no account.

Code: https://github.com/Tinhomagri/haunted-terminal

## Why open-weight matters here

- **Your shell history is private.** Commands carry hostnames, paths, tokens pasted by mistake. A ghost that reads them must not be a cloud API. Here the prompt never leaves `127.0.0.1`.
- **It works with the lights off.** No internet, no outage, no rate limit. If Ollama is down the ghost just stays silent (`except Exception: pass`) and the prompt is never blocked, because the call runs in a background subshell.
- **I can swap the model with one env var** (`HAUNT_MODEL`). That let me compare two sizes honestly instead of trusting a spec sheet.
- **Costs nothing per command.** A hook that fires on every few keystrokes would be absurd to bill per token.

## Gemma 3 4B vs 12B (measured, not guessed)

Same prompt, 5 commands, 16 cores, no GPU, 14 GB RAM (warm = model already loaded):

| Model | First call | Warm median | Warm max |
|---|---|---|---|
| gemma3:4b | 9.5 s | 2.2 s | 2.3 s |
| gemma3:12b | 5.5 s (pre-warmed) | 8.2 s | 9.3 s |

Two things I learned:

1. **12B writes slightly better lines, but 4B is the right default.** The ghost runs in the background, but a whisper that shows up 9 s after the command feels disconnected; 2 s feels like it is watching you.
2. **Cold start can silence the ghost.** My first 12B run timed out: loading ~8 GB of weights exceeded the 20 s request timeout, and the "never explain yourself" error handling hid it. When it loaded first, the same call took 5.5 s. If you use a bigger model, keep it resident (`OLLAMA_KEEP_ALIVE`) or raise the timeout.

Sample 4B lines:

- `git push --force` → *The past resists your forceful rewrite, forever staining its digital echoes.*
- `sudo apt update` → *The system whispers of updates, but something else is being quietly installed.*

## Try it

```bash
ollama pull gemma3:4b
git clone https://github.com/Tinhomagri/haunted-terminal && cd haunted-terminal
echo "source $PWD/haunt.sh" >> ~/.bashrc
```

Env: `HAUNT_ODDS`, `HAUNT_MODEL`, `HAUNT_HOST`.

## Limits

Small models sometimes repeat "echoes" and "something unseen". Bash only (zsh needs `precmd`). Latencies above are CPU-only on one machine.
