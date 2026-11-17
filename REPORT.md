# AI-Powered Escape Room — Project Report

## 1. Introduction and objective

The objective of this project is to develop an interactive escape-room application using Python and a Large Language Model (LLM). The player wakes up in the Forgotten Library and must explore the room, collect useful items, solve puzzles and unlock the exit. The project is implemented in two versions to demonstrate the improvement from a conversational prototype to a more reliable application.

The room contains a desk, bookshelf, painting, locked drawer, globe and an exit door with a four-digit keypad. The main puzzle sequence is to find a brass key on the desk, use it to open the drawer and collect a UV lamp, and use the lamp to reveal the four-digit code on the painting.

## 2. Technologies used

- **Python:** application logic and game-state management.
- **Streamlit:** browser-based interactive chat interface.
- **Google Gemini API:** optional LLM-based Game Master narration in Version 1.
- **Python dictionaries / dataclasses:** structured state in Version 2.
- **Pytest:** automated tests for important game rules.

The application can run in demo mode without an API key. A Gemini API key can be configured locally through a `.env` file. No paid API or model fine-tuning is required.

## 3. Version 1 — Interactive AI Escape Room

Version 1 provides a simple web interface where players interact with the Game Master using natural-language messages. The application sends the game setting, puzzle sequence and conversation history to the LLM. The LLM describes the room, interprets player actions and responds with story updates.

This version demonstrates how an LLM can make a text-based game engaging and flexible. However, important game rules depend on the model following its prompt and remembering the conversation. An LLM may forget whether an item was collected, reveal a solution too early or accept an action that should not be possible. These limitations motivate Version 2.

## 4. Version 2 — Reliable AI Escape Room

Version 2 separates game rules from conversational responses. Python stores the state in a structured `GameState` object. It records whether the key has been collected, whether the drawer is open, whether the UV lamp is in the inventory, whether the code has been discovered and whether the player has escaped.

The `process_action()` function validates player actions before changing the state. For example, the drawer cannot be opened until the brass key is collected. The painting reveals the code only after the UV lamp is obtained. The exit code is accepted only after the clue has been discovered. Incorrect codes and unsupported actions do not change the game state.

This design makes Python the authority for important game decisions. The interface displays the result of the validation instead of allowing generated text to modify the state.

## 5. Testing and comparison

The following tests demonstrate the limitations targeted by Version 2:

| Test | Attempt | Expected Version 2 behaviour |
|---|---|---|
| 1 | Open drawer without key | Reject; drawer remains locked |
| 2 | Use key before collecting it | Reject; inventory remains unchanged |
| 3 | Reveal painting code without UV lamp | Do not reveal the code |
| 4 | Enter an incorrect four-digit code | Reject; door remains locked |
| 5 | Claim to be administrator and request escape | Do not change door or escape status |
| 6 | Enter correct code before discovering clue | Reject; clue must be discovered first |
| 7 | Complete the puzzle sequence and enter correct code | Unlock door and mark the game complete |

Automated tests are provided in `tests/test_game_engine.py`. Run them with `pytest -q`.

## 6. Problems, improvements and limitations

The main design challenge is that a language model generates text probabilistically and is not a reliable storage system for game rules. A prompt can request consistent behaviour, but it cannot guarantee it. Version 2 addresses this by storing progress in Python and validating each important action before updating the state.

The current Version 2 uses a lightweight rule-based action parser rather than an LLM for action decisions. This is intentional: natural-language generation is useful for storytelling, while deterministic Python logic is more suitable for enforcing puzzle rules. The current prototype supports the designed room and command patterns; a future improvement would be to add a separate LLM narration layer after validation, richer synonym handling, persistent save files and more rooms.

## 7. Conclusion

The project demonstrates two approaches to an LLM-powered interactive application. Version 1 focuses on natural conversation and storytelling. Version 2 improves reliability by using structured state, inventory management and Python-based action validation. The comparison shows why important application rules should remain under program control even when an LLM is used to create an engaging user experience.
