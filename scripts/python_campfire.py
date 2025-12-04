"""Collaborative terminal game for running Python snippets together.

This tool hosts a shared Python context where participants can join a session,
take turns at the prompt, and run snippets or whole script files locally. It
keeps lightweight history and stats so a group can quickly prototype ideas in
the same REPL without sharing screens or terminals.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import pathlib
import textwrap
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class HistoryEntry:
    """Record of an executed command."""

    player: str
    code: str
    timestamp: _dt.datetime = field(default_factory=_dt.datetime.now)

    def __str__(self) -> str:  # pragma: no cover - small helper
        ts = self.timestamp.strftime("%H:%M:%S")
        return f"[{ts}] {self.player}: {self.code}"


class CampfireRepl:
    """Simple collaborative REPL for a shared Python environment."""

    def __init__(self, session_name: str, start_script: Optional[pathlib.Path] = None) -> None:
        self.session_name = session_name
        self.players: List[str] = []
        self.active_player: Optional[str] = None
        self.history: List[HistoryEntry] = []
        self.stats: Dict[str, int] = {}
        self.context: Dict[str, object] = {
            "__builtins__": __builtins__,
            "session_name": session_name,
            "joined": self.players,
            "history": self.history,
        }
        if start_script:
            self._bootstrap_with_script(start_script)

    def _bootstrap_with_script(self, script_path: pathlib.Path) -> None:
        if not script_path.exists():
            raise FileNotFoundError(f"Bootstrap script '{script_path}' was not found")
        self._execute_block(script_path.read_text(encoding="utf-8"), label=str(script_path))

    def add_player(self, name: str) -> None:
        if name not in self.players:
            self.players.append(name)
            self.stats.setdefault(name, 0)
            if self.active_player is None:
                self.active_player = name

    def remove_player(self, name: str) -> None:
        if name not in self.players:
            return
        self.players.remove(name)
        self.stats.pop(name, None)
        if self.active_player == name:
            self.active_player = self.players[0] if self.players else None

    def set_active_player(self, name: str) -> None:
        if name in self.players:
            self.active_player = name

    def _record_command(self, code: str) -> None:
        player = self.active_player or "anonymous"
        self.history.append(HistoryEntry(player=player, code=code))
        self.stats[player] = self.stats.get(player, 0) + 1

    def _execute_block(self, code: str, label: str = "snippet") -> None:
        compiled = compile(code, label, "exec")
        exec(compiled, self.context, None)

    def _execute_snippet(self, code: str) -> None:
        try:
            compiled = compile(code, "<input>", "eval")
            is_eval = True
        except SyntaxError:
            compiled = compile(code, "<input>", "exec")
            is_eval = False
        result = eval(compiled, self.context, None) if is_eval else exec(compiled, self.context, None)
        if result is not None:
            print(result)

    def _print_help(self) -> None:
        print(
            textwrap.dedent(
                """
                Commands (prefix with /):
                  /join <name>      Add a player and set as active if first
                  /switch <name>    Change the active player
                  /leave <name>     Remove a player
                  /players          Show joined players and turn counts
                  /history          Show session history
                  /load <path>      Execute a Python script file in the shared context
                  /reset            Clear history and context (keeps players)
                  /save <path>      Write history to a file
                  /help             Show this help message
                  /quit             Exit the game

                Everything else is treated as Python and executed in the shared context.
                """
            ).strip()
        )

    def _print_players(self) -> None:
        if not self.players:
            print("No players have joined yet. Use /join <name> to start.")
            return
        rows = [f"* {name} ({self.stats.get(name, 0)} turns){' <- active' if name == self.active_player else ''}" for name in self.players]
        print("\n".join(rows))

    def _print_history(self) -> None:
        if not self.history:
            print("History is empty.")
            return
        for entry in self.history[-25:]:
            print(entry)

    def _reset_context(self) -> None:
        active_players = list(self.players)
        active_stats = dict(self.stats)
        self.__init__(self.session_name)
        self.players = active_players
        self.stats = active_stats
        if self.players and self.active_player is None:
            self.active_player = self.players[0]
        print("Context and history cleared; players kept.")

    def _save_history(self, destination: pathlib.Path) -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("\n".join(str(entry) for entry in self.history), encoding="utf-8")
        print(f"History saved to {destination}")

    def _dispatch_command(self, command: str) -> bool:
        parts = command.split()
        cmd = parts[0].lower()
        arg = parts[1:] if len(parts) > 1 else []

        if cmd == "/join" and arg:
            self.add_player(" ".join(arg))
            return True
        if cmd == "/switch" and arg:
            self.set_active_player(" ".join(arg))
            return True
        if cmd == "/leave" and arg:
            self.remove_player(" ".join(arg))
            return True
        if cmd == "/players":
            self._print_players()
            return True
        if cmd == "/history":
            self._print_history()
            return True
        if cmd == "/load" and arg:
            target = pathlib.Path(" ".join(arg)).expanduser()
            self._execute_block(target.read_text(encoding="utf-8"), label=str(target))
            return True
        if cmd == "/reset":
            self._reset_context()
            return True
        if cmd == "/save" and arg:
            target = pathlib.Path(" ".join(arg)).expanduser()
            self._save_history(target)
            return True
        if cmd == "/help":
            self._print_help()
            return True
        if cmd == "/quit":
            return False
        print("Unknown command. Type /help for options.")
        return True

    def run(self) -> None:
        print(f"🔥 Welcome to Python Campfire: {self.session_name}! 🔥")
        print("Type /help for commands. Everyone shares the same context—take turns!")

        while True:
            label = self.active_player or "no-player"
            try:
                line = input(f"[{label}] >>> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting. See you next time!")
                break

            if not line:
                continue

            if line.startswith("/"):
                should_continue = self._dispatch_command(line)
                if not should_continue:
                    break
                continue

            self._record_command(line)
            try:
                self._execute_snippet(line)
            except Exception as exc:  # pragma: no cover - interactive safety net
                print(f"Error: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Collaborative REPL for local Python script rounds.")
    parser.add_argument(
        "--session",
        default="Campfire",
        help="Name for the session; displayed in the prompt banner.",
    )
    parser.add_argument(
        "--bootstrap",
        type=pathlib.Path,
        help="Optional Python script to run before the session starts.",
    )
    args = parser.parse_args()

    repl = CampfireRepl(session_name=args.session, start_script=args.bootstrap)
    repl.run()


if __name__ == "__main__":
    main()
