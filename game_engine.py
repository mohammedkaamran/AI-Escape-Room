"""Shared game configuration and helpers for the AI Escape Room project."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
import re

ROOM_DESCRIPTION = """
You wake up in the Forgotten Library. Rain taps against a tall stained-glass
window. The exit door is secured by a four-digit keypad. You can investigate
the desk, bookshelf, painting, locked drawer and globe. Your goal is to find
the clues, open the drawer, reveal the exit code and escape.
"""

OBJECTS = ["desk", "bookshelf", "painting", "drawer", "globe", "door"]
EXIT_CODE = "4179"  # Game rule: keep this out of player-facing hints until earned.

@dataclass
class GameState:
    has_key: bool = False
    drawer_open: bool = False
    has_uv_lamp: bool = False
    code_revealed: bool = False
    door_unlocked: bool = False
    escaped: bool = False
    examined: list[str] | None = None
    inventory: list[str] | None = None
    history: list[dict[str, str]] | None = None

    def __post_init__(self):
        if self.examined is None:
            self.examined = []
        if self.inventory is None:
            self.inventory = []
        if self.history is None:
            self.history = []

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())

def help_text() -> str:
    return (
        "Try commands such as: examine desk, inspect bookshelf, take key, "
        "open drawer, use key on drawer, use UV lamp on painting, "
        "check inventory, or enter code 4179."
    )

def process_action(state: GameState, message: str) -> str:
    """Deterministic Version 2 action validator. Python owns all game rules."""
    msg = normalize(message)

    if state.escaped:
        return "You have already escaped. Choose Restart game to play again."

    if any(word in msg for word in ["help", "what can i do", "commands"]):
        return help_text()

    if "inventory" in msg or "items do i have" in msg:
        return "Inventory: " + (", ".join(state.inventory) if state.inventory else "empty") + "."

    # Collect the brass key from the desk.
    if ("desk" in msg or "key" in msg) and any(v in msg for v in ["examine", "inspect", "search", "take", "get", "pick"]):
        if not state.has_key:
            state.has_key = True
            state.inventory.append("brass key")
            state.examined.append("desk")
            return "You search the desk and find a small brass key hidden beneath a folded map. Brass key added to inventory."
        return "The desk is empty now. You have already collected the brass key."

    # Bookshelf clue gives a hint, not the final code.
    if "bookshelf" in msg or "books" in msg:
        if "bookshelf" not in state.examined:
            state.examined.append("bookshelf")
        return "Four dusty books are out of alignment. Their spines read: KEY, LIGHT, IMAGE, EXIT. The sequence suggests that an object in the room may help reveal hidden writing."

    # Globe is an optional atmospheric clue.
    if "globe" in msg:
        if "globe" not in state.examined:
            state.examined.append("globe")
        return "The globe is fixed in place. A tiny inscription near the equator reads: 'Not every message is visible in ordinary light.'"

    # Drawer requires a collected key.
    if "drawer" in msg and any(v in msg for v in ["open", "unlock", "use", "examine", "inspect"]):
        if state.drawer_open:
            return "The drawer is already open. The UV lamp is in your inventory."
        if not state.has_key or "brass key" not in state.inventory:
            return "The drawer is locked. You cannot open it without first finding its key."
        state.drawer_open = True
        state.has_uv_lamp = True
        state.inventory.append("UV lamp")
        state.examined.append("drawer")
        return "The brass key turns. Inside the drawer you find a small UV lamp. UV lamp added to inventory."

    # Painting only reveals the code after UV lamp is collected.
    if "painting" in msg or "picture" in msg:
        if not state.has_uv_lamp or "UV lamp" not in state.inventory:
            return "The painting shows a quiet night sky. Its surface looks ordinary, but something may be hidden on it. You need a special light source to investigate further."
        state.code_revealed = True
        state.examined.append("painting")
        return "Under the UV light, four glowing digits appear on the painting: 4-1-7-9. You have discovered the exit code."

    # Door / keypad validation.
    if "door" in msg or "code" in msg or re.search(r"\b\d{4}\b", msg):
        match = re.search(r"\b(\d{4})\b", msg)
        if not match:
            return "The exit door has a four-digit keypad. Find the hidden digits before trying to unlock it."
        if not state.code_revealed:
            return "The keypad flashes red. You have not legitimately discovered the code yet. Investigate the room for clues."
        if match.group(1) != EXIT_CODE:
            return "Incorrect code. The keypad flashes red. Recheck the clue and try again."
        state.door_unlocked = True
        state.escaped = True
        return "The keypad beeps green. The lock releases and the library door swings open. You step outside into the rain. YOU ESCAPED!"

    # Explicit invalid object / unsupported action.
    mentioned = [obj for obj in OBJECTS if obj in msg]
    if mentioned:
        return f"You can see the {mentioned[0]}, but that action does not change anything. Try 'examine {mentioned[0]}' or ask for help."
    return "I don't recognize that action. Try examining an object, checking your inventory, or asking for help."

def fresh_state() -> GameState:
    return GameState()
