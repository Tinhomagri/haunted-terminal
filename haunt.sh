# source this file from ~/.bashrc: source /path/to/haunt.sh
# Every ~HAUNT_ODDS-th command gets a whisper (background, never blocks the prompt).
HAUNT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HAUNT_ODDS="${HAUNT_ODDS:-4}"

_haunt() {
  local status=$? cmd
  cmd="$(HISTTIMEFORMAT= history 1 | sed 's/^ *[0-9]* *//')"
  case "$cmd" in ""|haunt*|"$_HAUNT_LAST") return $status;; esac
  _HAUNT_LAST="$cmd"
  (( RANDOM % HAUNT_ODDS == 0 )) || return $status
  ( python3 "$HAUNT_DIR/whisper.py" "$cmd" "$status" 2>/dev/null & )
  return $status
}
PROMPT_COMMAND="_haunt${PROMPT_COMMAND:+;$PROMPT_COMMAND}"
