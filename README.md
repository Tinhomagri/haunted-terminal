# Haunted Terminal

A ghost lives in your shell. Every few commands, a local open-weight model (Gemma 3 via Ollama) whispers an eerie one-liner about what you just ran. Fully offline.

## Setup
```bash
ollama pull gemma3:4b
echo "source $PWD/haunt.sh" >> ~/.bashrc
```
Env: `HAUNT_ODDS` (1 in N commands, default 4), `HAUNT_MODEL`, `HAUNT_HOST`.

## How it works
`haunt.sh` hooks `PROMPT_COMMAND`, picks the last command + exit status, and runs `whisper.py` in the background so the prompt never blocks. `whisper.py` calls Ollama's `/api/generate` with stdlib only. If the model is down, the ghost stays silent.
